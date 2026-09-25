---
hide:
  - navigation
  - toc
---

<div class="caisp-hero" markdown>

# Certified AI Security Professional

**Learn how AI systems work, how attackers break them, and how to defend them — starting from absolute zero.**

No machine-learning background required. No maths degree required. If you can install
Python and copy-paste a command, you can finish this course.

[Start with Chapter 1 :material-arrow-right:](chapter-01/index.md){ .md-button .md-button--primary }
[Set up your lab first](start-here/lab-environment.md){ .md-button }

</div>

---

## What you will be able to do at the end

<div class="caisp-cards" markdown>

<div class="caisp-card" markdown>
<span class="caisp-kicker">Understand</span>
### Explain how AI actually works
Describe what a model, a token, an embedding and a neural network are — in plain
language, without hand-waving.
</div>

<div class="caisp-card" markdown>
<span class="caisp-kicker">Attack</span>
### Break an LLM on purpose
Run prompt injection, data-poisoning, model-theft and supply-chain attacks against
systems you build yourself, in a safe lab.
</div>

<div class="caisp-card" markdown>
<span class="caisp-kicker">Defend</span>
### Ship AI features safely
Threat-model an AI application, scan models for malicious payloads, sanitise prompts,
and wire guardrails into a CI/CD pipeline.
</div>

<div class="caisp-card" markdown>
<span class="caisp-kicker">Govern</span>
### Speak the compliance language
Map your work to OWASP LLM Top 10, MITRE ATLAS, NIST AI RMF, ISO/IEC 42001 and the
EU AI Act.
</div>

</div>

---

## The course at a glance

| # | Chapter | You will learn | Labs |
|---|---------|----------------|:----:|
| 1 | [Introduction to AI Security](chapter-01/index.md) | AI/ML/DL fundamentals, RAG, why AI security is different | 1 |
| 2 | Understanding and Attacking LLMs | How LLMs work, MITRE ATLAS, offensive tooling | 10 |
| 3 | LLM Top 10 Vulnerabilities | OWASP LLM Top 10, in depth | 4 |
| 4 | AI Attacks and Defenses Using DevOps | Pipeline attacks, scanning, AI firewalls | 6 |
| 5 | Threat Modeling AI Systems | STRIDE, DFDs, AI threat libraries, risk rating | 1 |
| 6 | Supply Chain Attacks in AI | Trojanised models, SBOM, signing, SLSA | 5 |
| 7 | Emerging Threats, Governance & Compliance | Model worms, NIST RMF, ISO 42001, EU AI Act | 2 |

!!! tip "New here? Read this first"
    Go to **[Start Here](start-here/index.md)** before Chapter 1. It explains how the
    course is structured, how to prepare for the certification, and — most importantly —
    how to get your lab environment working so the hands-on exercises actually run.

---

## How this course is different

**Everything is hands-on.** Every concept you read about, you then attack or defend in a
lab on your own machine. You do not need cloud credits, a GPU, or a paid API key —
every lab has a free, offline-capable path.

**It assumes nothing.** When we say "tokenizer", we explain what a tokenizer is. When we
show Python, we explain what each line does. There is a
[glossary](start-here/glossary.md) you can keep open in a second tab.

**It is honest about risk.** You will learn real attack techniques. Chapter by chapter we
repeat the rules of engagement: these techniques are for systems **you own** or have
**written permission** to test.
