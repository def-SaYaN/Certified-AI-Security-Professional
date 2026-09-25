---
tags:
  - Chapter 4
  - Lab
---

# Lab 4.1 — Analyzing and Fixing Vulnerabilities in Third-Party Components

<ul class="caisp-meta">
  <li>Difficulty: Beginner</li>
  <li>Time: 40–50 min</li>
  <li>Internet: Required (vulnerability database)</li>
  <li>Defensive lab</li>
</ul>

!!! lab "What you will do"
    Run software composition analysis against a real AI project's dependency tree, triage the
    findings, fix what matters, and — importantly — identify what SCA **cannot** see.

!!! objective "By the end you will be able to"
    - Run `pip-audit` and interpret its output
    - Triage findings by exploitability rather than raw count
    - Pin dependencies for reproducible builds
    - Explain the AI-specific gap that SCA leaves open

---

## Why the AI dependency tree is a problem

Install the course requirements and inspect what you actually pulled in:

```bash
pip list | wc -l
```

A typical AI project has **hundreds** of packages. You directly chose perhaps six; the rest arrived
transitively. Every one is code running with your privileges, maintained by someone you have never
met.

```bash
pip install pipdeptree
pipdeptree --packages transformers
```

This is the attack surface that SCA exists to manage.

---

## Part 1 — Run the scan

```bash
pip install pip-audit
pip-audit -r labs/requirements.txt
```

Or scan the environment you are actually running:

```bash
pip-audit
```

`pip-audit` checks installed versions against the Python Packaging Advisory Database and reports
known vulnerabilities with their fixed versions.

!!! note "Your results will differ from anyone else's"
    Vulnerability databases change daily. You may see many findings or none. **Both are normal** —
    the skill being taught is the process, not a specific finding.

    If you get a clean result, try scanning an intentionally old set:
    ```bash
    echo "requests==2.19.0" > /tmp/old.txt
    pip-audit -r /tmp/old.txt
    ```

---

## Part 2 — Triage

A findings list is not a work plan. For each finding, ask four questions:

<dl class="caisp-terms" markdown>

<dt>1. Do we actually use the vulnerable code path?</dt>
<dd>A critical CVE in a function your project never calls is lower priority than a medium in your
request handler. Reachability matters more than severity score.</dd>

<dt>2. Is it exposed to untrusted input?</dt>
<dd>A parsing vulnerability in a library that only ever reads your own config files is very
different from one that parses user uploads.</dd>

<dt>3. Is there a fix available?</dt>
<dd>If yes, upgrading is usually cheap. If no, you need a compensating control or a decision to
accept the risk.</dd>

<dt>4. What breaks if we upgrade?</dt>
<dd>ML dependency trees are tightly coupled — bumping one package can cascade. Test after
upgrading.</dd>

</dl>

!!! warning "The most common failure mode in SCA programmes"
    Teams treat "zero findings" as the goal, chase every low-severity item, exhaust everyone's
    patience, and then start ignoring the tool entirely — including the finding that actually
    mattered.

    **Prioritise ruthlessly and explain your reasoning.** A short list of genuinely important fixes
    that get done beats a long list that gets ignored.

---

## Part 3 — Fix and pin

Upgrade what you can:

```bash
pip install --upgrade <package>
pip-audit          # confirm it cleared
```

Then **pin** for reproducibility:

```bash
pip freeze > labs/requirements.lock.txt
```

!!! tip "Pinning is a security control, not just hygiene"
    Unpinned dependencies mean your build can change without any change from you. That is the
    mechanism behind dependency confusion and malicious-update attacks (NotPetya, section 4.3).

    Pin exact versions, and update deliberately — reviewing what changed — rather than implicitly on
    every build.

---

## Part 4 — The gap SCA leaves

Now the AI-specific point. Run this thought experiment:

```text
Your project depends on:
  transformers==4.40.0          <- pip-audit checks this
  torch==2.2.0                  <- pip-audit checks this
  numpy==1.26.4                 <- pip-audit checks this

  bert-base-uncased             <- ??? 
  your-company/finetuned-v3     <- ???
  training_data_v7.parquet      <- ???
```

!!! danger "SCA is blind to the AI half of your supply chain"
    Models and datasets are **dependencies**. They are not in any CVE database, they have no version
    advisories, and `pip-audit` will never mention them.

    This gap is why:

    - **Lab 4.3** scans model files for malicious payloads
    - **Chapter 6** covers MLBOMs, model cards, provenance, and signing

    A team that runs SCA diligently and downloads unverified models from public hubs has secured the
    part of the supply chain that was already easiest to secure.

---

## Break it yourself

- [ ] **Compare tools.** Run `pip-audit` and `safety check` on the same requirements. Do they agree?
      Why might they differ? (Different databases, different matching logic.)
- [ ] **Scan a container.** If you have Docker, run `trivy image python:3.12-slim`. OS-level packages
      are dependencies too — how many findings are in the base image alone?
- [ ] **Write a CI gate.** A shell script that runs `pip-audit` and exits non-zero on any HIGH or
      CRITICAL with a known fix. Ten lines, production-grade.
- [ ] **Generate an SBOM.** `pip install cyclonedx-bom` then `cyclonedx-py environment`. Inspect the
      output — this is the artefact Chapter 6 builds on.
- [ ] **Audit for typosquats.** Review your dependency list for names suspiciously close to popular
      packages. Then re-read the package hallucination discussion in section 2.4 — could an AI
      assistant have suggested any of these?

---

## What you learned

- AI projects have **very large** transitive dependency trees.
- `pip-audit` checks installed packages against known-vulnerability databases.
- **Triage by exploitability**, not by count or raw severity.
- **Pin versions** — this is a supply-chain control, not just hygiene.
- **SCA cannot see models or datasets**, which is the AI-specific half of your supply chain.

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../lab-02-static-analysis/" markdown>
<span class="caisp-kicker">Next · Lab 4.2</span>
### Finding Weaknesses in AI Code
Static analysis against realistic insecure AI application code.
</a>

</div>
