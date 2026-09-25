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

<div class="caisp-cards">
<a class="caisp-card" href="01-overview.md">
  <span class="caisp-kicker">6.1</span>
  <span class="caisp-card-title">Supply Chain Security Overview</span>
  <span class="caisp-card-text">What a supply chain attack is, and why it is so effective.</span>
</a>
<a class="caisp-card" href="02-ai-supply-chain-attacks.md">
  <span class="caisp-kicker">6.2</span>
  <span class="caisp-card-title">AI Supply Chain Attacks</span>
  <span class="caisp-card-text">Data, model, and infrastructure attacks; package masquerading.</span>
</a>
<a class="caisp-card" href="03-vetting.md">
  <span class="caisp-kicker">6.3</span>
  <span class="caisp-card-title">Vetting Software Frameworks</span>
  <span class="caisp-card-text">Building and automating a vetting process; dependency pinning.</span>
</a>
<a class="caisp-card" href="04-frameworks.md">
  <span class="caisp-kicker">6.4</span>
  <span class="caisp-card-title">Supply Chain Frameworks</span>
  <span class="caisp-card-text">SLSA and the Software Component Verification Standard.</span>
</a>
<a class="caisp-card" href="05-transparency-integrity.md">
  <span class="caisp-kicker">6.5</span>
  <span class="caisp-card-title">Transparency &amp; Integrity</span>
  <span class="caisp-card-text">SBOMs, provenance, attestations, model cards, MLBOMs, model signing.</span>
</a>
</div>

## Labs

<div class="caisp-cards">
<a class="caisp-card" href="lab-01-rome.md">
  <span class="caisp-kicker">Lab 6.1 · Understand</span>
  <span class="caisp-card-title">Editing Models (ROME concept)</span>
  <span class="caisp-card-text">How targeted model editing works — and why it is a supply-chain threat.</span>
</a>
<a class="caisp-card" href="lab-02-trojanized-models.md">
  <span class="caisp-kicker">Lab 6.2 · Detect</span>
  <span class="caisp-card-title">How Trojanized Models Work</span>
  <span class="caisp-card-text">The anatomy of a trojanized model, and how to reason about detection.</span>
</a>
<a class="caisp-card" href="lab-03-scanning.md">
  <span class="caisp-kicker">Lab 6.3 · Defend</span>
  <span class="caisp-card-title">Scanning Models for Malicious Code</span>
  <span class="caisp-card-text">A multi-layer model scanner you build and run.</span>
</a>
<a class="caisp-card" href="lab-04-sbom.md">
  <span class="caisp-kicker">Lab 6.4 · Defend</span>
  <span class="caisp-card-title">Generating an SBOM</span>
  <span class="caisp-card-text">Produce a real SBOM, then extend the idea to an MLBOM.</span>
</a>
<a class="caisp-card" href="lab-05-signing.md">
  <span class="caisp-kicker">Lab 6.5 · Defend</span>
  <span class="caisp-card-title">Signing &amp; Verifying Models</span>
  <span class="caisp-card-text">Cryptographic provenance — the defence that scales.</span>
</a>
</div>

---

!!! danger "Rules of engagement"
    The tampering concepts in this chapter are taught for defence. Do not create or distribute
    malicious models. The [rules of engagement](../start-here/index.md) apply with particular force
    here — a trojanized model is malware.
