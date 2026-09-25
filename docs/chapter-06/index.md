---
tags:
  - Chapter 6
  - Supply Chain
---

# Chapter 6 — Supply Chain Attacks in AI

<ul class="caisp-meta">
  <li>Level: Intermediate → Advanced</li>
  <li>Reading: ~2 hrs</li>
  <li>Labs: 5</li>
  <li>Exam weight: ~12%</li>
</ul>

Chapter 4 touched the supply chain from the DevOps angle. This chapter goes deep on the part that is
genuinely unique to AI: **the model itself as an untrusted artefact.** You will learn how models are
tampered with, why you cannot inspect your way to trust, and the discipline — vetting, SBOMs,
provenance, and signing — that actually works.

The through-line of the whole chapter is one idea you already met in Lab 2.9 and Lab 4.3:

!!! danger "The chapter in one sentence"
    **You cannot review a model the way you review code, so trust in a model must come from
    *provenance*, not *inspection*.**

    Everything here follows from that. If you could open a model and read it, this chapter would be
    unnecessary. You cannot, so it is essential.

!!! objective "What you will be able to do after this chapter"
    - Explain the AI supply chain and how it differs from a software supply chain
    - Describe data-, model-, and infrastructure-based supply chain attacks
    - Explain conceptually how models are edited (ROME) and trojanized — and why detection is hard
    - Build a **vetting process** for third-party AI components
    - Apply **SLSA** and **SCVS** to an AI project
    - Generate an **SBOM** and understand **MLBOMs** and **model cards**
    - **Sign and verify** a model with real tooling

---

## Handling the offensive material honestly

The syllabus lists several model-tampering labs (ROME editing, trojanized models, trojanized neural
networks). Here is how this course handles them, and why.

!!! note "Detection-and-defence framing for the tampering labs"
    Labs 6.1 and 6.2 teach how model editing and trojanizing **work** — at a conceptual and
    detection level, using tiny non-weaponized examples — rather than shipping tools that produce
    distributable malicious models.

    This is deliberate and costs you nothing on the exam or the job:

    - The assessed skill is **recognising, detecting, and defending against** tampered models, not
      manufacturing them.
    - You already built and detected a backdoor in Lab 2.9 — that is the offensive intuition, in a
      contained form.
    - The genuinely valuable, genuinely hands-on work in this chapter is **defensive**: vetting,
      SBOMs, scanning, and signing (Labs 6.3–6.5), and those are fully runnable.

    You will finish this chapter able to defend against model-supply-chain attacks. You will not
    finish it holding a weapon.

---

## Sections

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../01-overview/" markdown>
<span class="caisp-kicker">6.1</span>
### Supply Chain Security Overview
What a supply chain attack is, and why it is so effective.
</a>

<a class="caisp-card" href="../02-ai-supply-chain-attacks/" markdown>
<span class="caisp-kicker">6.2</span>
### AI Supply Chain Attacks
Data, model, and infrastructure attacks; package masquerading.
</a>

<a class="caisp-card" href="../03-vetting/" markdown>
<span class="caisp-kicker">6.3</span>
### Vetting Software Frameworks
Building and automating a vetting process; dependency pinning.
</a>

<a class="caisp-card" href="../04-frameworks/" markdown>
<span class="caisp-kicker">6.4</span>
### Supply Chain Frameworks
SLSA and the Software Component Verification Standard.
</a>

<a class="caisp-card" href="../05-transparency-integrity/" markdown>
<span class="caisp-kicker">6.5</span>
### Transparency & Integrity
SBOMs, provenance, attestations, model cards, MLBOMs, model signing.
</a>

</div>

## Labs

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../lab-01-rome/" markdown>
<span class="caisp-kicker">Lab 6.1 · Understand</span>
### Editing Models (ROME concept)
How targeted model editing works — and why it is a supply-chain threat.
</a>

<a class="caisp-card" href="../lab-02-trojanized-models/" markdown>
<span class="caisp-kicker">Lab 6.2 · Detect</span>
### How Trojanized Models Work
The anatomy of a trojanized model, and how to reason about detection.
</a>

<a class="caisp-card" href="../lab-03-scanning/" markdown>
<span class="caisp-kicker">Lab 6.3 · Defend</span>
### Scanning Models for Malicious Code
A multi-layer model scanner you build and run.
</a>

<a class="caisp-card" href="../lab-04-sbom/" markdown>
<span class="caisp-kicker">Lab 6.4 · Defend</span>
### Generating an SBOM
Produce a real SBOM, then extend the idea to an MLBOM.
</a>

<a class="caisp-card" href="../lab-05-signing/" markdown>
<span class="caisp-kicker">Lab 6.5 · Defend</span>
### Signing & Verifying Models
Cryptographic provenance — the defence that scales.
</a>

</div>

---

!!! danger "Rules of engagement"
    The tampering concepts in this chapter are taught for defence. Do not create or distribute
    malicious models. The [rules of engagement](../start-here/index.md) apply with particular force
    here — a trojanized model is malware.
