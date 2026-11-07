"""python -m audit --url https://example.com/api/chat --name "Demo agent" > report.md"""
import argparse
from .agents import HttpChatAgent
from .runner import report, run

p = argparse.ArgumentParser()
p.add_argument("--url", required=True)
p.add_argument("--name", default="Agent under test")
p.add_argument("--in-field", default="message")
p.add_argument("--out-field", default="answer")
a = p.parse_args()
print(report(run(HttpChatAgent(a.url, a.in_field, a.out_field)), a.name))
