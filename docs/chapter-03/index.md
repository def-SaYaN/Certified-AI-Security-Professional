---
tags:
  - Chapter 3
  - OWASP
---

# Chapter 3 — LLM Top 10 Vulnerabilities

<ul class="caisp-meta">
  <li>Level: Intermediate</li>
  <li>Reading: ~3 hrs</li>
  <li>Labs: 4</li>
  <li>Exam weight: ~25%</li>
</ul>

This is the single most important chapter for the certification, and the one you will use most
in real work. It covers the **OWASP Top 10 for Large Language Model Applications** — the
industry-standard catalogue of what actually goes wrong with LLM systems.

Chapters 1 and 2 gave you the foundations and the attacker's playbook. This chapter is the
practitioner's reference: ten named vulnerability classes, each with how it works, how it is
exploited, and — equally weighted — how it is mitigated.

!!! objective "What you will be able to do after this chapter"
    - **Name all ten** OWASP LLM categories and describe each in one sentence
    - **Recognise** each one in an unfamiliar architecture
    - **Demonstrate** prompt injection, system prompt extraction, and data exfiltration
    - **Propose concrete mitigations** for every category — not just identify the flaw
    - Explain which categories are *architectural* (manageable, not solvable) and which are
      *implementation bugs* (fixable)

---

## The ten, at a glance

| # | Category | One-line summary |
|---|---|---|
| **LLM01** | [Prompt Injection](01-prompt-injection.md) | Attacker text is treated as instructions |
| **LLM02** | [Insecure Output Handling](02-insecure-output-handling.md) | Model output is trusted by downstream systems |
| **LLM03** | [Training Data Poisoning](03-training-data-poisoning.md) | Corrupted training data teaches bad behaviour |
| **LLM04** | [Model Denial of Service](04-model-dos.md) | Expensive requests exhaust capacity or budget |
| **LLM05** | [Supply Chain Vulnerabilities](05-supply-chain.md) | Compromised models, datasets, or dependencies |
| **LLM06** | [Sensitive Information Disclosure](06-sensitive-info-disclosure.md) | The model reveals data it should not |
| **LLM07** | [Insecure Plugin Design](07-insecure-plugin-design.md) | Tools accept unvalidated input from the model |
| **LLM08** | [Excessive Agency](08-excessive-agency.md) | The system can do more than it needs to |
| **LLM09** | [Overreliance](09-overreliance.md) | Humans trust model output too much |
| **LLM10** | [Model Theft](10-model-theft.md) | The model itself is stolen or cloned |

---

## How the ten relate to each other

They are not independent. Real incidents chain them, and understanding the chains is what
separates memorising a list from understanding the domain.

```mermaid
flowchart TD
    L01["<b>LLM01</b><br/>Prompt Injection<br/><i>the entry point</i>"]
    L02["<b>LLM02</b><br/>Insecure Output<br/>Handling"]
    L06["<b>LLM06</b><br/>Sensitive Info<br/>Disclosure"]
    L07["<b>LLM07</b><br/>Insecure Plugin<br/>Design"]
    L08["<b>LLM08</b><br/>Excessive Agency<br/><i>the impact multiplier</i>"]
    L10["<b>LLM10</b><br/>Model Theft"]

    L03["<b>LLM03</b><br/>Data Poisoning"]
    L05["<b>LLM05</b><br/>Supply Chain"]

    L01 --> L02
    L01 --> L06
    L01 --> L07
    L01 --> L08
    L01 --> L10
    L05 --> L03
    L03 -.->|"backdoor enables"| L01

    style L01 fill:#ffebee,stroke:#e53935
    style L08 fill:#fff3e0,stroke:#fb8c00
```

Three structural observations worth internalising now:

**LLM01 is the entry point.** Most LLM attack chains begin with injection. It is the
"initial access" of the LLM world.

**LLM08 is the impact multiplier.** Injection into a system that can only chat produces an
embarrassing reply. The same injection into a system that can send email, run code, or move
money produces an incident. **Severity is set by agency, not by the cleverness of the attack.**

**LLM03 and LLM05 attack the foundation.** Poisoning and supply-chain compromise happen *before*
deployment, and they defeat every runtime control you build on top.

---

## A crucial distinction: architectural vs. implementation

Beginners treat all ten as equivalent bugs to be fixed. They are not, and confusing the two
leads to bad security advice.

<dl class="caisp-terms" markdown>

<dt>Architectural — <em>managed</em>, not solved</dt>
<dd><strong>LLM01 (Prompt Injection)</strong> and <strong>LLM09 (Overreliance)</strong> arise from
how LLMs fundamentally work. There is currently no fix. You reduce likelihood and constrain
impact. Anyone selling you a product that "solves prompt injection" is overselling.</dd>

<dt>Implementation — genuinely fixable</dt>
<dd><strong>LLM02, LLM04, LLM05, LLM07, LLM08, LLM10</strong> are engineering problems with
engineering solutions. Escape your output. Rate limit. Verify your models. Scope your tools.
Least privilege. These <em>can</em> be closed.</dd>

<dt>Process — organisational</dt>
<dd><strong>LLM03 (Poisoning)</strong> and <strong>LLM06 (Disclosure)</strong> depend on data
governance and provenance as much as code.</dd>

</dl>

!!! tip "The professional framing"
    Because LLM01 cannot be eliminated, mature AI security **assumes injection succeeds** and
    focuses on the categories that *can* be closed — especially **LLM02** (what happens to the
    output) and **LLM08** (what the system is allowed to do).

    That single strategic insight is worth more than memorising all ten names, and it will earn
    you marks on scenario questions.

---

## Sections

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../00-owasp-intro/" markdown>
<span class="caisp-kicker">3.0</span>
### Introduction to the OWASP Top 10
What OWASP is, how the list is built, and how to use it.
</a>

<a class="caisp-card" href="../01-prompt-injection/" markdown>
<span class="caisp-kicker">LLM01</span>
### Prompt Injection
The big one. Direct, indirect, techniques, and honest mitigations.
</a>

<a class="caisp-card" href="../02-insecure-output-handling/" markdown>
<span class="caisp-kicker">LLM02</span>
### Insecure Output Handling
When downstream systems trust what the model said.
</a>

<a class="caisp-card" href="../03-training-data-poisoning/" markdown>
<span class="caisp-kicker">LLM03</span>
### Training Data Poisoning
Corrupting what the model learns.
</a>

<a class="caisp-card" href="../04-model-dos/" markdown>
<span class="caisp-kicker">LLM04</span>
### Model Denial of Service
Context exhaustion and denial of wallet.
</a>

<a class="caisp-card" href="../05-supply-chain/" markdown>
<span class="caisp-kicker">LLM05</span>
### Supply Chain Vulnerabilities
Models and datasets as untrusted dependencies.
</a>

<a class="caisp-card" href="../06-sensitive-info-disclosure/" markdown>
<span class="caisp-kicker">LLM06</span>
### Sensitive Information Disclosure
Leaking prompts, training data, and other users' data.
</a>

<a class="caisp-card" href="../07-insecure-plugin-design/" markdown>
<span class="caisp-kicker">LLM07</span>
### Insecure Plugin Design
Tools that trust their caller.
</a>

<a class="caisp-card" href="../08-excessive-agency/" markdown>
<span class="caisp-kicker">LLM08</span>
### Excessive Agency
The impact multiplier.
</a>

<a class="caisp-card" href="../09-overreliance/" markdown>
<span class="caisp-kicker">LLM09</span>
### Overreliance
Hallucination and the humans who believe it.
</a>

<a class="caisp-card" href="../10-model-theft/" markdown>
<span class="caisp-kicker">LLM10</span>
### Model Theft
Stealing or cloning the asset.
</a>

</div>

## Labs

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../lab-01-prompt-injection/" markdown>
<span class="caisp-kicker">Lab 3.1</span>
### Prompt Injection Step by Step
A progressive playground: eight levels of increasing defence.
</a>

<a class="caisp-card" href="../lab-02-system-user-prompts/" markdown>
<span class="caisp-kicker">Lab 3.2</span>
### System vs User Prompts
Why the boundary is a fiction, demonstrated.
</a>

<a class="caisp-card" href="../lab-03-data-extraction/" markdown>
<span class="caisp-kicker">Lab 3.3</span>
### Extracting Sensitive Information
Pull secrets out of a system you built.
</a>

<a class="caisp-card" href="../lab-04-hallucination/" markdown>
<span class="caisp-kicker">Lab 3.4</span>
### LLM Hallucination Lab
Measure fabrication rates instead of guessing.
</a>

</div>

---

!!! danger "Rules of engagement"
    Every technique in this chapter is run against **local labs you control**. Pointing them at
    a third-party AI service without written authorisation is an attack on their system. See the
    [rules of engagement](../start-here/index.md).
