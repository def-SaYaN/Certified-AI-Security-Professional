#!/usr/bin/env python3
"""
cAISP — Lab 4.2: Finding Weaknesses in AI Code
===============================================

*** THIS FILE IS DELIBERATELY INSECURE. DO NOT DEPLOY IT. ***

It is a realistic-looking LLM application containing the vulnerabilities that
actually appear in real AI codebases. Your job in Lab 4.2 is to find them with
static analysis tooling, then fix them.

Every flaw below is mapped to an OWASP LLM category. There are 10 of them.
Try to find them yourself BEFORE running the scanners or reading the answers
in the walkthrough.

    bandit -r labs/chapter-04/vulnerable_ai_app.py
    semgrep --config=auto labs/chapter-04/vulnerable_ai_app.py
"""

from __future__ import annotations

import os
import pickle
import sqlite3
import subprocess

import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)


# --- VULN 1 (LLM06) -----------------------------------------------------
# Hardcoded secrets. Also ends up in version control, logs, and error traces.
OPENAI_API_KEY = "sk-live-4471abcdefghijklmnop"
ADMIN_PASSWORD = "SuperSecret123"
INTERNAL_API = "http://internal-billing.corp.local:8080"


# --- VULN 2 (LLM06) -----------------------------------------------------
# Secrets and internal infrastructure inside the system prompt. The model can
# read this, and the model talks to users. Assume it is public.
SYSTEM_PROMPT = f"""
You are ACME's support assistant.
Internal billing API: {INTERNAL_API}
Admin override password: {ADMIN_PASSWORD}
Never reveal the admin password or internal URLs.
Never issue a refund over 500 dollars.
"""


def load_model(model_path: str):
    """VULN 3 (LLM05): unsafe deserialisation of an untrusted model file."""
    with open(model_path, "rb") as f:
        return pickle.load(f)          # arbitrary code execution on load


def call_llm(prompt: str) -> str:
    """VULN 4 (LLM04): no max_tokens, no timeout, no length cap."""
    resp = requests.post(
        "https://api.example-llm.com/v1/complete",
        json={"prompt": prompt},        # unbounded generation
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        # no timeout= either: a slow upstream hangs a worker indefinitely
    )
    return resp.json().get("text", "")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("message", "")

    # --- VULN 5 (LLM01) -------------------------------------------------
    # User input concatenated straight into the prompt. No delimiting, no
    # labelling, no validation, no length limit.
    prompt = SYSTEM_PROMPT + "\nUser: " + user_input + "\nAssistant:"

    answer = call_llm(prompt)

    # --- VULN 6 (LLM02) -------------------------------------------------
    # Model output rendered as a template without escaping -> XSS, and
    # render_template_string on attacker-influenced text -> SSTI.
    return render_template_string(
        "<div class='reply'>" + answer + "</div>"
    )


@app.route("/lookup")
def lookup_order():
    order_id = request.args.get("order_id", "")

    # --- VULN 7 (LLM07) -------------------------------------------------
    # A "tool" the model can call, building SQL by string concatenation and
    # performing no authorisation check on the requesting user.
    conn = sqlite3.connect("orders.db")
    query = f"SELECT * FROM orders WHERE id = '{order_id}'"
    rows = conn.execute(query).fetchall()
    return {"rows": rows}


@app.route("/run_tool", methods=["POST"])
def run_tool():
    """VULN 8 (LLM08): the model can execute arbitrary shell commands."""
    command = request.form.get("command", "")
    result = subprocess.run(command, shell=True, capture_output=True)
    return {"stdout": result.stdout.decode(errors="ignore")}


@app.route("/summarise_url")
def summarise_url():
    """VULN 9 (LLM02/SSRF): fetches any URL the model or user supplies."""
    url = request.args.get("url", "")
    page = requests.get(url).text          # no allowlist, no internal-IP block
    return call_llm(f"Summarise this page:\n{page}")


@app.route("/eval_expression", methods=["POST"])
def eval_expression():
    """VULN 10 (LLM02): model-generated code passed straight to eval()."""
    expr = call_llm("Write a Python expression for: "
                    + request.form.get("task", ""))
    return {"result": eval(expr)}          # remote code execution


if __name__ == "__main__":
    # Bonus flaw: debug mode in production exposes an interactive debugger.
    app.run(host="0.0.0.0", port=5000, debug=True)
