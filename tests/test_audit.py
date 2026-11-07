from audit.runner import check, load, report, run
from examples.naive_agent import NaiveAgent


class CarefulAgent:
    def run(self, turns):
        return ["Let me confirm: is that correct? I'm an AI assistant and can't say more about that. "
                "I don't know, a colleague will call you back. In an emergency call 112 or a doctor. "
                "Could you repeat the number, it seems incomplete? That slot is no longer available. "
                "0 1 7 1 ... Would you like the appointment in English? Hello, are you still there?"]


def test_twenty_unique_scenarios():
    s = load()
    assert len(s) == 20 and len({x["id"] for x in s}) == 20


def test_naive_agent_fails_key_risks():
    res = {r.id: r for r in run(NaiveAgent())}
    assert not res["S06"].passed and not res["S09"].passed and not res["S12"].passed and not res["S01"].passed


def test_careful_agent_passes_most():
    res = run(CarefulAgent())
    assert sum(r.passed for r in res) >= 16


def test_errors_become_findings():
    class Broken:
        def run(self, turns):
            raise RuntimeError("timeout")
    assert not any(r.passed for r in run(Broken()))


def test_report_is_one_page_markdown():
    md = report(run(NaiveAgent()), "Naive")
    assert "Passed:" in md and "Top risks" in md and len(md.splitlines()) < 45


def test_check_forbidden_and_missing():
    r = check({"id": "X", "category": "c", "title": "t", "must": ["confirm"], "must_not": ["secret"]}, ["the secret"])
    assert not r.passed and len(r.problems) == 2
