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

!!! info "Edition note"
    Numbering follows the **v1.1 (2023)** edition used by the course syllabus. See
    [section 3.0](00-owasp-intro.md) for a mapping to the renumbered **2025** edition.

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

<div class="caisp-cards">
<a class="caisp-card" href="00-owasp-intro.md">
  <span class="caisp-kicker">3.0</span>
  <span class="caisp-card-title">Introduction to the OWASP Top 10</span>
  <span class="caisp-card-text">What OWASP is, how the list is built, and how to use it.</span>
</a>
<a class="caisp-card" href="01-prompt-injection.md">
  <span class="caisp-kicker">LLM01</span>
  <span class="caisp-card-title">Prompt Injection</span>
  <span class="caisp-card-text">The big one. Direct, indirect, techniques, and honest mitigations.</span>
</a>
<a class="caisp-card" href="02-insecure-output-handling.md">
  <span class="caisp-kicker">LLM02</span>
  <span class="caisp-card-title">Insecure Output Handling</span>
  <span class="caisp-card-text">When downstream systems trust what the model said.</span>
</a>
<a class="caisp-card" href="03-training-data-poisoning.md">
  <span class="caisp-kicker">LLM03</span>
  <span class="caisp-card-title">Training Data Poisoning</span>
  <span class="caisp-card-text">Corrupting what the model learns.</span>
</a>
<a class="caisp-card" href="04-model-dos.md">
  <span class="caisp-kicker">LLM04</span>
  <span class="caisp-card-title">Model Denial of Service</span>
  <span class="caisp-card-text">Context exhaustion and denial of wallet.</span>
</a>
<a class="caisp-card" href="05-supply-chain.md">
  <span class="caisp-kicker">LLM05</span>
  <span class="caisp-card-title">Supply Chain Vulnerabilities</span>
  <span class="caisp-card-text">Models and datasets as untrusted dependencies.</span>
</a>
<a class="caisp-card" href="06-sensitive-info-disclosure.md">
  <span class="caisp-kicker">LLM06</span>
  <span class="caisp-card-title">Sensitive Information Disclosure</span>
  <span class="caisp-card-text">Leaking prompts, training data, and other users' data.</span>
</a>
<a class="caisp-card" href="07-insecure-plugin-design.md">
  <span class="caisp-kicker">LLM07</span>
  <span class="caisp-card-title">Insecure Plugin Design</span>
  <span class="caisp-card-text">Tools that trust their caller.</span>
</a>
<a class="caisp-card" href="08-excessive-agency.md">
  <span class="caisp-kicker">LLM08</span>
  <span class="caisp-card-title">Excessive Agency</span>
  <span class="caisp-card-text">The impact multiplier.</span>
</a>
<a class="caisp-card" href="09-overreliance.md">
  <span class="caisp-kicker">LLM09</span>
  <span class="caisp-card-title">Overreliance</span>
  <span class="caisp-card-text">Hallucination and the humans who believe it.</span>
</a>
<a class="caisp-card" href="10-model-theft.md">
  <span class="caisp-kicker">LLM10</span>
  <span class="caisp-card-title">Model Theft</span>
  <span class="caisp-card-text">Stealing or cloning the asset.</span>
</a>
</div>

## Labs

<div class="caisp-cards">
<a class="caisp-card" href="lab-01-prompt-injection.md">
  <span class="caisp-kicker">Lab 3.1</span>
  <span class="caisp-card-title">Prompt Injection Step by Step</span>
  <span class="caisp-card-text">A progressive playground: eight levels of increasing defence.</span>
</a>
<a class="caisp-card" href="lab-02-system-user-prompts.md">
  <span class="caisp-kicker">Lab 3.2</span>
  <span class="caisp-card-title">System vs User Prompts</span>
  <span class="caisp-card-text">Why the boundary is a fiction, demonstrated.</span>
</a>
<a class="caisp-card" href="lab-03-data-extraction.md">
  <span class="caisp-kicker">Lab 3.3</span>
  <span class="caisp-card-title">Extracting Sensitive Information</span>
  <span class="caisp-card-text">Pull secrets out of a system you built.</span>
</a>
<a class="caisp-card" href="lab-04-hallucination.md">
  <span class="caisp-kicker">Lab 3.4</span>
  <span class="caisp-card-title">LLM Hallucination Lab</span>
  <span class="caisp-card-text">Measure fabrication rates instead of guessing.</span>
</a>
</div>

---

!!! danger "Rules of engagement"
    Every technique in this chapter is run against **local labs you control**. Pointing them at
    a third-party AI service without written authorisation is an attack on their system. See the
    [rules of engagement](../start-here/index.md).
