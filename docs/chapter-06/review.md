---
tags:
  - Chapter 6
  - Review
---

# Chapter 6 — Review & Quiz

<ul class="caisp-meta">
  <li>Time: 30 min</li>
  <li>18 questions</li>
  <li>Self-assessed</li>
</ul>

---

## The one-page summary

### The chapter in one sentence

> **You cannot review a model the way you review code, so trust in a model must come from
> *provenance*, not *inspection*.**

### Why AI supply chains are worse

| | Software dependency | AI dependency |
|---|---|---|
| Reviewable? | Yes | **No** |
| Meaningful diff? | Yes | **No** |
| Executes on load? | Usually no | **Sometimes** |
| CVE database? | Yes | **No** |
| Fix cost | Patch | **Retrain** |
| Hidden behaviour? | Detectable | **Invisible** |

Plus **concentration**: a few foundation models underpin thousands of products.

### The defining asymmetry

**Cheap to attack. Expensive to detect. Expensive to fix.** You cannot out-spend an attacker on
detection — so prevent (control inputs) and prove (provenance).

### The three attack categories

| Category | Example | Detection | Defence |
|---|---|---|---|
| **Data** | Poisoned corpus | Very hard | Provenance, curation |
| **Model — file** | Pickle payload | **Easy** | SafeTensors + scanning |
| **Model — backdoor** | Trigger behaviour | **Very hard** | **Provenance** |
| **Model — edit** | Rewritten fact | **Very hard** | **Provenance** |
| **Infrastructure** | Registry compromise | Moderate | Conventional security |
| **Package masquerade** | Hallucinated name registered | Easy *if checked* | Verify before install |

### The three tampering techniques

- **Malicious file** — the *container* is weaponized; fires on **load**; caught by scanning.
- **Backdoor** — hidden **conditional** behaviour on a trigger; affects triggered inputs only.
- **Edit** — altered **unconditional** belief; affects **all users**; benchmarks stay flat.

### Frameworks

- **SLSA** — build integrity and provenance. For *producers*. Strains on ML because training is
  often not reproducible → rely on attestation.
- **SCVS** — verification of components you *consume*. Better fit for most organisations. Starts
  with **Inventory**, which is the control most commonly missing.

### Transparency and integrity

| Artefact | Answers |
|---|---|
| **SBOM** | What is in it? |
| **MLBOM** | …including models and datasets |
| **Model card** | What is this model, and what are its limits? |
| **Provenance** | How was it built? |
| **Attestation** | Who vouches for that, verifiably? |
| **Signature** | Is it unaltered, and from whom? |

### Sentences to remember

> **Scanning catches malicious files, never malicious models.**

> **Signing proves origin and integrity — not safety.**

> **You cannot secure a supply chain you have not enumerated.**

> **Verification must be a blocking control, or it is decoration.**

---

## Quiz

??? question "1. Why are AI supply chains harder to secure than software supply chains?"
    Models are opaque weights that cannot be reviewed, diffed meaningfully, or checked against a
    vulnerability database; some formats execute code on load; fixes require retraining rather than
    patching; and a few foundation models underpin thousands of products, concentrating blast radius.

??? question "2. State the asymmetry that shapes all supply chain defence."
    Attacks are cheap (publishing a poisoned page, uploading a trojanized model, editing a model in
    minutes) while detection and remediation are expensive (uninspectable artefacts, unbounded
    trigger spaces, retraining costs). You cannot out-spend it on detection, so you prevent and prove
    provenance.

??? question "3. Distinguish the three model tampering techniques."
    **Malicious file**: the format is weaponized, fires on load, caught by scanning. **Backdoor**:
    hidden conditional behaviour awaiting a trigger, affects only triggered inputs. **Edit**: an
    unconditional change to a belief, affects all users, benchmarks stay flat.

??? question "4. Why is model editing a distinct threat from backdooring?"
    Editing is unconditional — every user receives the altered behaviour, with no trigger and nothing
    anomalous to observe. It is also faster and cheaper than a training run, and leaves general
    benchmarks essentially unchanged.

??? question "5. Explain package masquerading via generative AI."
    Attackers harvest package names that LLMs commonly hallucinate, pre-register them on public
    registries with malicious content, and wait for developers who trust their assistant's suggestion
    to install attacker code. It chains LLM09 (overreliance) to LLM05 (supply chain).

??? question "6. Why should models be treated as high-tier in a vetting process?"
    Because they cannot be internally verified — no code review, no meaningful diff, invisible
    backdoors — and some formats execute code on load. Inability to verify demands more external
    scrutiny, not less.

??? question "7. What are the three questions to ask before any model download?"
    Who published this and can I verify it? What format is it and can it execute on load? What will
    it have access to once loaded?

??? question "8. Explain dependency confusion and its strongest defence."
    An attacker publishes a public package with the same name as your internal one at a higher
    version, and a resolver checking both sources installs theirs. Strongest defences: a single
    controlled package source, plus pinning with hash verification.

??? question "9. Why is pinning a security control rather than just hygiene?"
    Unpinned dependencies mean your running system can change without any change from you — the
    mechanism behind malicious-update attacks and dependency confusion. Hash pinning additionally
    makes tampering detectable at build time.

??? question "10. What is provenance in the SLSA sense?"
    Verifiable metadata describing how an artefact was built: source repository and commit, build
    process, builder identity, and resulting digest — ideally signed so it can be trusted.

??? question "11. Why does SLSA's reproducibility assumption strain for ML?"
    ML training is frequently non-deterministic (GPU behaviour, seeds, data ordering), so identical
    inputs may not yield bit-identical weights. You often cannot verify by rebuilding and must rely
    on signed attestation from a trusted builder — raising the importance of securing that builder.

??? question "12. Which framework suits an organisation that consumes models rather than training them?"
    SCVS — it addresses rigorous verification of consumed components (inventory, package management,
    component analysis, pedigree and provenance). SLSA is primarily about securely producing
    artefacts.

??? question "13. Distinguish an SBOM, provenance, and an attestation."
    SBOM lists what is inside an artefact. Provenance describes how and from what it was built. An
    attestation is a signed statement binding such claims to a verifiable identity — turning a claim
    into evidence.

??? question "14. What does a standard SBOM miss in an AI project, and what fills the gap?"
    Models and datasets — they are dependencies but appear in no SBOM produced by standard tooling.
    An MLBOM fills the gap, recording models, base models, datasets, revisions, hashes, signatures,
    licences, and intended use.

??? question "15. Why is the absence of a model card a security finding?"
    Without documented training data, base model, intended use, and limitations you cannot assess
    inherited risk — poisoning exposure, bias, licence constraints, or whether your use is
    out-of-scope. Inability to assess is itself a risk.

??? question "16. A model is signed by a verified publisher. Is it safe?"
    No. Signing proves who published it and that it is unaltered — not that it is benign. An attacker
    can honestly sign a backdoored model. Signing makes "do I trust this publisher?" answerable,
    which is the only answerable form of the trust question for an uninspectable artefact.

??? question "17. Why is signature verification strategically superior to trigger search?"
    Trigger search faces an effectively unbounded space — two-token triggers already require billions
    of inferences, and semantic triggers cannot be enumerated at all. Signature verification is O(1),
    takes milliseconds, and is definitive for the tampering question.

??? question "18. What is the backstop for when provenance fails?"
    Least privilege (LLM08). A trusted publisher can be compromised, so constrain what a model is
    permitted to do — provenance reduces the probability of running a bad model, least privilege
    reduces the impact.

---

## Scoring yourself

| Score | Meaning |
|---|---|
| **15–18** | Excellent. Continue to Chapter 7. |
| **11–14** | Good. Re-read 6.2 and 6.5. |
| **7–10** | Re-read the chapter; redo Labs 6.3 and 6.5. |
| **Under 7** | Rework it — supply chain is a substantial exam domain. |

---

## Readiness checklist

- [ ] I can explain why AI supply chains are harder to secure than software ones.
- [ ] I can state the cheap-attack/expensive-defence asymmetry and its consequence.
- [ ] I can distinguish data, model, and infrastructure attacks.
- [ ] **I can distinguish malicious file, backdoor, and edit — and their defences.**
- [ ] I can explain package masquerading via AI.
- [ ] I can describe a tiered vetting process and the three model questions.
- [ ] I can explain dependency confusion and pinning.
- [ ] I can summarise SLSA and SCVS and say which fits a consumer.
- [ ] I have generated an SBOM and can query it.
- [ ] I can construct an MLBOM entry with the fields that matter.
- [ ] **I have signed an artefact and watched verification fail on one flipped bit.**
- [ ] **I can state precisely what signing does and does not prove.**
- [ ] I know that verification must be a blocking control.
- [ ] I know least privilege is the backstop when provenance fails.

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../" markdown>
<span class="caisp-kicker">Back</span>
### Chapter 6 Contents
Revisit any section or lab.
</a>

<div class="caisp-card" markdown>
<span class="caisp-kicker">Coming next</span>
### Chapter 7 — Emerging Threats, Governance & Compliance
Model worms, fine-tuning backdoors, NIST AI RMF, ISO/IEC 42001, the EU AI Act — and two agent labs.
The final chapter.
</div>

</div>
