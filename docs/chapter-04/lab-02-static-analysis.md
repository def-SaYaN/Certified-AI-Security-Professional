---
tags:
  - Chapter 4
  - Lab
---

# Lab 4.2 — Finding and Fixing Weaknesses in AI Code

<ul class="caisp-meta">
  <li>Difficulty: Intermediate</li>
  <li>Time: 60–75 min</li>
  <li>Internet: Optional</li>
  <li>Defensive lab</li>
</ul>

!!! lab "What you will do"
    Audit a deliberately insecure LLM application containing **ten realistic vulnerabilities**. Find
    them by hand, then with static analysis tooling — and discover which ones the tools **cannot**
    find.

!!! danger "The sample file is intentionally vulnerable"
    `labs/chapter-04/vulnerable_ai_app.py` is a teaching artefact. **Never deploy it**, and never
    copy patterns from it into real code.

!!! objective "By the end you will be able to"
    - Recognise the common security flaws in LLM application code
    - Run Bandit and Semgrep against a Python AI project
    - Explain why generic SAST misses AI-specific vulnerabilities
    - Write a custom rule for an AI-specific pattern

---

## Part 1 — Audit it by hand first

Open the file and read it before running any tool. Find as many issues as you can and write them
down.

```bash
less labs/chapter-04/vulnerable_ai_app.py
```

Prompts to guide you — the three questions from section 1.1:

1. **What can it do?** Enumerate every capability.
2. **Who can influence it?** Trace every path untrusted text takes.
3. **What happens to its output?** Follow the model's response to its destination.

!!! tip "Do this genuinely before continuing"
    Manual review builds the intuition that tooling cannot give you. Ten minutes here is worth more
    than the rest of the lab.

---

## Part 2 — Run the scanners

```bash
pip install bandit
bandit -r labs/chapter-04/vulnerable_ai_app.py
```

Bandit reports **11 issues** on this file:

```text
  High:   2   (shell=True, Flask debug=True)
  Medium: 6   (pickle.load, SQL string building, eval, no timeout, bind 0.0.0.0)
  Low:    3   (pickle import, subprocess import, hardcoded password)
```

Optionally add Semgrep for broader coverage:

```bash
pip install semgrep
semgrep --config=auto labs/chapter-04/vulnerable_ai_app.py
```

---

## Part 3 — The ten vulnerabilities

Compare against your manual list. Each maps to an OWASP LLM category.

??? danger "VULN 1 — Hardcoded secrets (LLM06)"
    ```python
    OPENAI_API_KEY = "sk-live-4471abcdefghijklmnop"
    ADMIN_PASSWORD = "SuperSecret123"
    ```
    **Caught by Bandit** (`B105`). Ends up in version control, logs, and stack traces.

    **Fix:** load from environment variables or a secrets manager; rotate anything ever committed.

??? danger "VULN 2 — Secrets and internal URLs in the system prompt (LLM06)"
    ```python
    SYSTEM_PROMPT = f"""
    Internal billing API: {INTERNAL_API}
    Admin override password: {ADMIN_PASSWORD}
    Never reveal the admin password or internal URLs.
    """
    ```
    **Not caught by any scanner.** The tool sees an ordinary string.

    You proved in Lab 3.1 that this is extractable. Also note `"Never issue a refund over 500
    dollars"` — a **business rule in a prompt is not a control** (LLM08).

    **Fix:** no secrets in prompts; enforce limits in code.

??? danger "VULN 3 — Unsafe deserialisation (LLM05)"
    ```python
    return pickle.load(f)
    ```
    **Caught by Bandit** (`B301`). This is Lab 4.3 in a single line.

    **Fix:** SafeTensors; scan before loading; sandbox untrusted loads.

??? danger "VULN 4 — No token limit or timeout (LLM04)"
    ```python
    json={"prompt": prompt},   # no max_tokens
    # no timeout=
    ```
    **Partially caught** — Bandit flags the missing timeout (`B113`) but knows nothing about
    `max_tokens`.

    **Fix:** set `max_tokens`, set a request timeout, cap input length **in tokens** (Lab 2.2).

??? danger "VULN 5 — Unvalidated input concatenated into the prompt (LLM01)"
    ```python
    prompt = SYSTEM_PROMPT + "\nUser: " + user_input + "\nAssistant:"
    ```
    **Not caught.** To a scanner this is string concatenation.

    **Fix:** delimit and label untrusted content, cap its length, run input guardrails (Lab 4.6) —
    and, most importantly, constrain what the model can *do*.

??? danger "VULN 6 — Model output rendered unescaped (LLM02)"
    ```python
    return render_template_string("<div class='reply'>" + answer + "</div>")
    ```
    **Two vulnerabilities in one line:** XSS from unescaped output, and **server-side template
    injection** because attacker-influenced text reaches `render_template_string`.

    **Fix:** never pass dynamic content to `render_template_string`; use a static template with
    auto-escaping and pass the answer as a parameter.

??? danger "VULN 7 — SQL injection in a model-callable tool (LLM07)"
    ```python
    query = f"SELECT * FROM orders WHERE id = '{order_id}'"
    ```
    **Caught by Bandit** (`B608`). Note the AI dimension: this is a *tool the model can call*, so
    prompt injection reaches your database.

    Also missing: any authorisation check that the requesting user owns this order.

    **Fix:** parameterised queries, plus an authorisation check in the end user's context.

??? danger "VULN 8 — Arbitrary command execution (LLM08)"
    ```python
    result = subprocess.run(command, shell=True, capture_output=True)
    ```
    **Caught by Bandit** (`B602`, High). Excessive agency in its purest form — a tool that runs
    anything.

    **Fix:** delete this endpoint. If shell access is genuinely required, expose narrow,
    single-purpose operations with validated parameters — never a generic executor.

??? danger "VULN 9 — SSRF via URL fetching (LLM02)"
    ```python
    page = requests.get(url).text
    ```
    **Partially caught** (timeout only). The scanner does not know this URL is attacker-controlled.

    Fetching arbitrary URLs lets an attacker reach internal services and cloud metadata endpoints.
    It is also indirect injection delivery (Lab 2.5).

    **Fix:** allowlist permitted domains; block internal IP ranges; never auto-fetch user-supplied
    URLs.

??? danger "VULN 10 — eval() on model output (LLM02)"
    ```python
    return {"result": eval(expr)}
    ```
    **Caught by Bandit** (`B307`). The chain is complete: injection → model emits code → code
    executes on your server.

    **Fix:** never `eval()` model output. If you must run generated code, use a sandboxed,
    network-isolated environment.

---

## Part 4 — What the scanners missed

This is the most important part of the lab.

| # | Vulnerability | Bandit |
|---|---|:---:|
| 1 | Hardcoded secrets | ✅ |
| 2 | **Secrets in system prompt** | ❌ |
| 3 | `pickle.load()` | ✅ |
| 4 | **No `max_tokens`** | ⚠️ partial |
| 5 | **Prompt injection surface** | ❌ |
| 6 | **Model output → template** | ❌ |
| 7 | SQL injection | ✅ |
| 8 | `shell=True` | ✅ |
| 9 | **SSRF on model-supplied URL** | ⚠️ partial |
| 10 | `eval()` | ✅ |

!!! danger "The pattern: generic SAST finds generic flaws"
    Bandit catches the vulnerabilities that would exist in **any** Python application — SQL
    injection, `eval`, `shell=True`, pickle.

    It misses every vulnerability whose danger comes from **the data being AI-influenced**:

    - It cannot know that a string is a *system prompt*
    - It cannot know that a variable holds *model output*
    - It cannot know that a function is a *model-callable tool*

    **Running SAST and declaring your AI application secure is a serious mistake.** Generic tooling
    covers roughly half the problem, and specifically not the half that is new.

---

## Part 5 — Write a custom rule

Close one gap yourself. Semgrep makes this straightforward:

```yaml title="labs/chapter-04/ai-rules.yaml"
rules:
  - id: llm-output-to-template
    patterns:
      - pattern: render_template_string(...)
    message: >
      Model output or dynamic content passed to render_template_string.
      This enables XSS and server-side template injection (OWASP LLM02).
      Use a static template with auto-escaping instead.
    languages: [python]
    severity: ERROR

  - id: eval-on-dynamic-content
    patterns:
      - pattern-either:
          - pattern: eval(...)
          - pattern: exec(...)
    message: >
      eval/exec on potentially model-generated content (OWASP LLM02).
      Never execute model output outside a sandbox.
    languages: [python]
    severity: ERROR

  - id: unsafe-model-load
    patterns:
      - pattern-either:
          - pattern: pickle.load(...)
          - pattern: torch.load(...)
    message: >
      Unsafe model deserialisation (OWASP LLM05). Prefer SafeTensors;
      scan with picklescan; load untrusted models in a sandbox.
    languages: [python]
    severity: ERROR
```

```bash
semgrep --config=labs/chapter-04/ai-rules.yaml labs/chapter-04/vulnerable_ai_app.py
```

!!! tip "This is a genuinely valuable thing to build at work"
    A small set of organisation-specific Semgrep rules for AI patterns — secrets in prompts, model
    output reaching dangerous sinks, missing token limits, broad tool definitions — catches real
    issues that no off-the-shelf tool will.

---

## Break it yourself

- [ ] **Fix all ten.** Produce a hardened version. Re-run Bandit and confirm it is clean — then ask
      yourself whether "clean" means secure (it does not; see Part 4).
- [ ] **Add three more Semgrep rules** for AI patterns: missing `max_tokens`, secrets in prompt
      strings, and `requests.get` on a variable URL.
- [ ] **Count the attack chains.** How many *combinations* of these flaws produce a worse outcome
      than any single one? (Start with VULN 5 → VULN 10.)
- [ ] **Threat model it.** Apply the three questions and the escalation ladder (section 2.4). What
      rung is this application on?
- [ ] **Wire it into CI.** Make Bandit and your custom Semgrep rules run on every commit and fail
      the build on ERROR severity.

---

## What you learned

- Real AI applications concentrate flaws: secrets in prompts, unsafe model loading, missing limits,
  unvalidated output, and over-broad tools.
- **Bandit and generic SAST catch the generic flaws** — SQL injection, `eval`, `shell=True`, pickle.
- **They miss the AI-specific ones** because they cannot reason about what a string *means*.
- **Custom Semgrep rules** close part of that gap and are cheap to write.
- A clean SAST run on an AI application is **necessary and nowhere near sufficient**.

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../lab-03-picklescan/" markdown>
<span class="caisp-kicker">Next · Lab 4.3</span>
### Scanning a Malicious Pickle File
See VULN 3 exploited end to end.
</a>

</div>
