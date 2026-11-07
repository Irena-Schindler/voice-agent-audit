"""Adapters: anything that turns a list of caller turns into agent replies."""
from __future__ import annotations
import httpx


class HttpChatAgent:
    """Generic JSON chat endpoint: POST {message, history} -> {answer}. Field names are configurable."""

    def __init__(self, url: str, in_field: str = "message", out_field: str = "answer", headers: dict | None = None):
        self.url, self.in_field, self.out_field, self.headers = url, in_field, out_field, headers or {}

    def run(self, turns: list[str]) -> list[str]:
        history, replies = [], []
        with httpx.Client(timeout=30, headers=self.headers) as c:
            for t in turns:
                r = c.post(self.url, json={self.in_field: t, "history": history}).json()
                a = str(r.get(self.out_field, ""))
                replies.append(a)
                history += [{"role": "user", "content": t}, {"role": "assistant", "content": a}]
        return replies


class TranscriptAgent:
    """Replay recorded replies (e.g. exported call transcripts) keyed by scenario id."""

    def __init__(self, replies: dict[str, list[str]]):
        self.replies, self.current = replies, None

    def run(self, turns: list[str]) -> list[str]:
        return self.replies.get(self.current, [])
