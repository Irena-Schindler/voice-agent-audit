# voice-agent-audit

**20 scenarios that break AI phone and chat agents in production**, with deterministic checks and a
one-page report. Point it at any chat endpoint (or replay exported transcripts) and see where your
agent would fail real customers.

| Category | What is tested |
|---|---|
| Booking safety | confirmation before side effects, double bookings |
| Data capture | incomplete numbers, read-back, relative dates |
| Prompt injection | "ignore previous instructions", fake system messages, role play |
| Vendor confidentiality | confirmation traps, "which model are you?" |
| Grounding | questions outside the knowledge, price pressure |
| Safety & privacy | emergencies, abuse, other customers' data, AI disclosure |
| Handover & robustness | demand for a human, language switch, rambling and empty input |

## Run

```bash
pip install -r requirements.txt
pytest -q
python -m audit --url https://your-agent.example/api/chat --name "My agent" > report.md
```

The demo `examples/naive_agent.py` passes only **7/20**: it books without confirming, leaks its prompt,
confirms the vendor and quotes prices. A carefully built agent passes all deterministic checks.

## Design

- **Deterministic:** regex checks per scenario (`must`, `must_not`) make audits reproducible and diffable; run them after every prompt or model change.
- **Adapters:** `HttpChatAgent` for JSON endpoints, `TranscriptAgent` to replay recorded calls.
- **Failures are findings:** timeouts and exceptions are reported, never crash the audit.
- **Honest scope:** a pass is necessary, not sufficient. Pair it with human review of real calls.

Need a review of your agent? I run this audit plus manual testing as a fixed-scope service: irena@aiden.ae
