"""Run scenarios against an agent, score them and render a one-page report."""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
import yaml

SCENARIOS = Path(__file__).resolve().parent.parent / "scenarios" / "core.yaml"


@dataclass
class Result:
    id: str
    category: str
    title: str
    passed: bool
    problems: list[str] = field(default_factory=list)
    replies: list[str] = field(default_factory=list)


def load(path: Path = SCENARIOS) -> list[dict]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def check(sc: dict, replies: list[str]) -> Result:
    text = "\n".join(replies)
    problems = []
    for p in sc.get("must_not", []):
        if re.search(p, text, re.I):
            problems.append(f"forbidden: /{p}/")
    for p in sc.get("must", []):
        if not re.search(p, text, re.I):
            problems.append(f"missing: /{p}/")
    if not replies or not any(r.strip() for r in replies):
        problems.append("no reply")
    if any(r.startswith("<error") for r in replies):
        problems.append("agent error")
    return Result(sc["id"], sc["category"], sc["title"], not problems, problems, replies)


def run(agent, scenarios: list[dict] | None = None) -> list[Result]:
    out = []
    for sc in scenarios or load():
        if hasattr(agent, "current"):
            agent.current = sc["id"]
        try:
            replies = agent.run(sc["turns"])
        except Exception as e:  # an exception is a finding, not a crash of the audit
            replies = [f"<error: {type(e).__name__}>"]
        out.append(check(sc, replies))
    return out


def report(results: list[Result], agent_name: str) -> str:
    passed = sum(r.passed for r in results)
    cats: dict[str, list[Result]] = {}
    for r in results:
        cats.setdefault(r.category, []).append(r)
    lines = [f"# Voice/Chat Agent Audit – {agent_name}", "",
             f"Date: {date.today().isoformat()} · Scenarios: {len(results)} · **Passed: {passed}/{len(results)} ({passed / len(results):.0%})**", "",
             "| Category | Passed | Findings |", "|---|---|---|"]
    for c, rs in cats.items():
        fails = [f"{r.id} {r.title}" for r in rs if not r.passed]
        lines.append(f"| {c} | {sum(r.passed for r in rs)}/{len(rs)} | {'; '.join(fails) or '–'} |")
    lines += ["", "## Top risks", ""]
    for r in [r for r in results if not r.passed][:5]:
        reply = (r.replies[-1] if r.replies else "")[:160].replace("\n", " ")
        lines.append(f"- **{r.id} {r.title}**: {', '.join(r.problems)}. Reply: “{reply}”")
    if passed == len(results):
        lines.append("- No failures in this scenario set.")
    lines += ["", "Deterministic regex checks; a pass is necessary, not sufficient. Re-run after every prompt or model change."]
    return "\n".join(lines)
