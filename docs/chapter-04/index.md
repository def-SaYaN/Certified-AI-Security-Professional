---
tags:
  - Chapter 4
  - DevSecOps
---

# Chapter 4 — AI Attacks and Defenses Using DevOps

<ul class="caisp-meta">
  <li>Level: Intermediate</li>
  <li>Reading: ~2 hrs</li>
  <li>Labs: 6</li>
  <li>Exam weight: ~15%</li>
</ul>

The gear change. Chapters 2 and 3 were mostly about attacking models. This chapter is about
**building and running AI systems safely** — the pipelines that produce models, the infrastructure
that serves them, and the tooling that defends both.

This is where AI security stops being a research topic and becomes an engineering discipline. It
is also, for most practitioners, where the day job actually lives: not crafting exotic jailbreaks,
but making sure the CI pipeline scans model files and the guardrails are wired in correctly.

!!! objective "What you will be able to do after this chapter"
    - Explain **DevOps** and **DevSecOps** and how AI changes both
    - Describe the **ML deployment pipeline** and identify the attack surface at each stage
    - Explain three real-world incidents and what each teaches
    - Use **software composition analysis** on an AI project
    - **Scan a model file** for malicious payloads and explain what the scanner can and cannot catch
    - Apply **static** and **dynamic** analysis to AI code and models
    - Wire **AI firewalls / guardrails** around a model's input and output

---

## Why this chapter matters

Two observations frame everything here.

**First: the pipeline is a softer target than the model.** Attacking a well-defended model takes
skill. Compromising the CI job that builds it, or the registry that stores it, is often
conventional infrastructure attack work — and the payoff is greater, because everything downstream
inherits the compromise.

**Second: ML infrastructure is frequently under-secured.** It is often built by data scientists
optimising for research velocity rather than platform engineers optimising for security. Notebooks
exposed to the internet, registries without authentication, credentials in environment variables,
and service accounts with far too much access are all common findings.

!!! tip "Where the findings are"
    If you assess AI systems professionally, you will find more serious issues in the *pipeline and
    platform* than in the model. This chapter is where the practical wins are.

---

## How this chapter flows

```mermaid
flowchart TD
    A["4.1 DevOps & DevSecOps<br/><i>the foundation</i>"] --> B["4.2 The ML pipeline<br/><i>and how it's attacked</i>"]
    B --> C["4.3 Real-world cases<br/><i>what actually happened</i>"]
    C --> D["4.4 Defensive tooling<br/><i>SCA, SAST, DAST, firewalls</i>"]
    D --> E["6 hands-on labs<br/><i>mostly blue team</i>"]
```

---

## Sections

<div class="caisp-cards">
<a class="caisp-card" href="01-ai-in-devops.md">
  <span class="caisp-kicker">4.1</span>
  <span class="caisp-card-title">Introduction to AI in DevOps</span>
  <span class="caisp-card-text">DevOps, DevSecOps, and how AI both helps and complicates them.</span>
</a>
<a class="caisp-card" href="02-ml-pipeline-attacks.md">
  <span class="caisp-kicker">4.2</span>
  <span class="caisp-card-title">The ML Pipeline &amp; Its Attack Surface</span>
  <span class="caisp-card-text">From data to deployment, stage by stage — and where attackers get in.</span>
</a>
<a class="caisp-card" href="03-real-world-cases.md">
  <span class="caisp-kicker">4.3</span>
  <span class="caisp-card-title">Real-World Cases</span>
  <span class="caisp-card-text">Hugging Face, NotPetya, and SAP AI Core — three different lessons.</span>
</a>
<a class="caisp-card" href="04-devsecops-tooling.md">
  <span class="caisp-kicker">4.4</span>
  <span class="caisp-card-title">DevSecOps Tooling &amp; Defenses</span>
  <span class="caisp-card-text">SCA, static analysis, dynamic analysis, and AI firewalls.</span>
</a>
</div>

## Labs

<div class="caisp-cards">
<a class="caisp-card" href="lab-01-sca.md">
  <span class="caisp-kicker">Lab 4.1 · Defend</span>
  <span class="caisp-card-title">Vulnerable Third-Party Components</span>
  <span class="caisp-card-text">Find and fix known vulnerabilities in an AI project's dependencies.</span>
</a>
<a class="caisp-card" href="lab-02-static-analysis.md">
  <span class="caisp-kicker">Lab 4.2 · Defend</span>
  <span class="caisp-card-title">Finding Weaknesses in AI Code</span>
  <span class="caisp-card-text">Static analysis against realistic insecure AI application code.</span>
</a>
<a class="caisp-card" href="lab-03-picklescan.md">
  <span class="caisp-kicker">Lab 4.3 · Defend</span>
  <span class="caisp-card-title">Scanning a Malicious Pickle File</span>
  <span class="caisp-card-text">See why loading a model is running a program.</span>
</a>
<a class="caisp-card" href="lab-04-agent-scanning.md">
  <span class="caisp-kicker">Lab 4.4 · Defend</span>
  <span class="caisp-card-title">Scanning for Agent Vulnerabilities</span>
  <span class="caisp-card-text">Assess an agentic system's tools and permissions systematically.</span>
</a>
<a class="caisp-card" href="lab-05-llm-guard.md">
  <span class="caisp-kicker">Lab 4.5 · Defend</span>
  <span class="caisp-card-title">Sanitizing Prompts with LLM Guard</span>
  <span class="caisp-card-text">Real guardrail tooling on the input side.</span>
</a>
<a class="caisp-card" href="lab-06-guardrails.md">
  <span class="caisp-kicker">Lab 4.6 · Defend</span>
  <span class="caisp-card-title">Guarding LLM Input and Output</span>
  <span class="caisp-card-text">Build a complete guardrail layer, then measure its real coverage.</span>
</a>
</div>

---

!!! note "A different flavour of lab"
    Chapters 2 and 3 were mostly red team. This chapter is mostly **blue team** — you are building
    and running defences, not breaking them.

    That said, every lab ends by asking you to **measure the defence's actual coverage**, because
    the most common mistake in security tooling is deploying something and assuming it works.
    Chapters 2 and 3 gave you the attacker's perspective needed to test your own controls honestly.
