---
tags:
  - Chapter 4
  - DevSecOps
---

# 4.3 Real-World Cases

!!! objective "In this section"
    - Malicious models on the Hugging Face platform
    - NotPetya — why a non-AI incident is on an AI security syllabus
    - SAP AI Core — multi-tenant ML platform vulnerabilities
    - The transferable lessons from each

!!! note "How to study these"
    Do not memorise dates and company names. For each case, be able to answer: **what was the root
    cause, which pipeline stage failed, and what control would have prevented it?** That is what
    scenario questions test, and what actually transfers to your work.

---

## Case 1 — Malicious models on Hugging Face

### What happened

**Hugging Face** is the dominant public hub for sharing ML models — effectively the npm or PyPI of
machine learning. Anyone can create an account and upload a model.

Security researchers have repeatedly found **malicious models** hosted there. The typical pattern:

1. A model is uploaded in a **pickle-based format** (`.pkl`, `.pt`, `.bin`).
2. The pickle payload contains code that executes **when the model is loaded**.
3. The code does what malware does: opens a reverse shell, exfiltrates environment variables and
   credentials, or establishes persistence.
4. A developer downloads the model, calls `torch.load()` or similar, and is compromised.

Hugging Face has responded with security scanning (including `picklescan`, which you will use in
Lab 4.3), malware scanning, and by promoting **SafeTensors** as a safe alternative format. But the
platform's fundamental property remains: **it is an open hub where anyone can publish.**

### Root cause

Two things combined:

- **A format that executes code on load.** Pickle was never designed as a secure interchange
  format (section 1.4).
- **A trust model that does not match reality.** Developers treat downloading a model like
  downloading data, when it is closer to downloading an executable.

### The lesson

!!! danger "Say it again: downloading a model is downloading executable content"
    - Prefer **SafeTensors**, which cannot execute code on load.
    - **Scan** model files before loading them (Lab 4.3).
    - **Load untrusted models in a sandbox** — no network, no credentials, no production access.
    - Prefer **official organisation accounts** over individual re-uploads.
    - Download counts and stars are popularity metrics, **not security signals**.

This also previews Chapter 6, where you will verify and sign models properly.

---

## Case 2 — NotPetya

### Why is a 2017 non-AI attack on this syllabus?

Because it is the clearest demonstration of the principle that underpins all supply chain security,
and because AI supply chains are *more* vulnerable to exactly this pattern.

### What happened

NotPetya (June 2017) was one of the most financially destructive cyberattacks in history. The
mechanism:

1. Attackers compromised the update server for **M.E.Doc**, a Ukrainian tax accounting package used
   by most companies doing business in Ukraine.
2. They pushed a **malicious software update** through the legitimate update channel.
3. Organisations installed it — because it was a signed, expected update from their trusted vendor.
4. The malware spread aggressively across internal networks, encrypting systems irreversibly. It was
   disguised as ransomware but was designed for destruction, not payment.
5. Damage ran into billions of dollars globally, crippling multinational shipping, pharmaceutical,
   and logistics operations far beyond Ukraine.

### Root cause

**Trust in the update channel.** Every victim did exactly what security guidance told them to do:
they applied vendor updates promptly. The compromise was *upstream* of them, and their own security
posture was irrelevant.

### The lesson

!!! warning "Your security depends on the security of everything you trust"
    NotPetya's victims had no vulnerability of their own to fix. They were compromised through a
    dependency.

    Now apply that to AI:

    | NotPetya | AI equivalent |
    |---|---|
    | Compromised vendor update server | Compromised model hub or registry |
    | Malicious signed update | Trojanised model with good metrics |
    | Auto-applied by trusting customers | Auto-pulled by CI pipelines |
    | Victims could not inspect the binary | **Nobody can inspect model weights** |

    The final row is the critical difference. A determined organisation *could* have reverse
    engineered the M.E.Doc update. **Nobody can reverse engineer a set of model weights to determine
    whether it is backdoored** (Lab 2.9). AI supply chains are structurally harder to defend than
    the one that produced NotPetya.

This is the argument for **provenance, signing, and verification** — Chapter 6's entire subject.

---

## Case 3 — SAP AI Core vulnerabilities

### What happened

Researchers disclosed a set of vulnerabilities in **SAP AI Core**, a managed cloud service for
running AI workloads. The findings (reported in 2024) centred on **tenant isolation failures** in a
multi-tenant ML platform.

The general shape — which is what matters for learning:

- Customers could submit training jobs that ran as containers on shared infrastructure.
- Weaknesses in how those workloads were isolated and how network access was restricted allowed
  escape from the intended boundary.
- From there, researchers could reach internal services and cloud credentials that should have been
  unreachable.
- The potential impact included access to **other tenants'** data and models.

### Root cause

**Running attacker-controlled code with insufficient isolation.** An ML training platform, by
design, executes arbitrary customer-supplied code. That is the product. It means the platform must
treat every workload as hostile — and hardening multi-tenant container isolation to that standard is
genuinely difficult.

### The lesson

!!! tip "Two lessons, depending on which side you are on"
    **If you run an ML platform:** every training job is untrusted code execution. You need strong
    container isolation, strict network segmentation, no shared credentials, and no path from a
    workload to the control plane. Assume workloads are hostile, because some will be.

    **If you use a managed ML platform:** you are relying on your provider's isolation. That is a
    reasonable thing to do — but it is a **dependency**, and it belongs in your threat model. Ask
    about isolation architecture, understand the shared responsibility boundary, and do not assume
    "it's managed" means "it's someone else's risk".

---

## The three lessons together

| Case | Failure | Transferable lesson |
|---|---|---|
| **Hugging Face** | Unsafe format + misplaced trust in an open hub | Models are executable content — scan, sandbox, prefer SafeTensors |
| **NotPetya** | Compromised trusted update channel | Your security depends on your dependencies; AI makes inspection impossible |
| **SAP AI Core** | Insufficient isolation of untrusted workloads | ML platforms run hostile code by design; isolation is the product |

!!! tip "The pattern across all three"
    None of these were attacks on a *model's behaviour*. Nobody jailbroke anything.

    All three were attacks on **infrastructure and trust relationships** — the subject of this
    chapter. This is what real AI incidents mostly look like, and it is why the defensive tooling in
    the next section matters more than another jailbreak technique.

---

!!! question "Check your understanding"
    ??? success "Why is NotPetya relevant to AI security despite involving no AI?"
        It demonstrates that compromising a trusted dependency defeats victims who have no
        vulnerability of their own. AI supply chains are more exposed to this pattern because model
        weights — unlike software binaries — cannot be meaningfully inspected for tampering.

    ??? success "What made malicious models on Hugging Face possible?"
        A file format (pickle) that executes code on load, combined with a developer trust model
        that treats model downloads as data rather than as executables. Fixes: SafeTensors,
        scanning, sandboxed loading, and preferring verified publishers.

    ??? success "Why is isolation especially critical for a managed ML training platform?"
        Because executing arbitrary customer-supplied code *is* the product. Every workload must be
        treated as hostile, requiring strong container isolation, network segmentation, and no path
        from a workload to the control plane or other tenants.

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../04-devsecops-tooling/" markdown>
<span class="caisp-kicker">Next · 4.4</span>
### DevSecOps Tooling & Defenses
SCA, static analysis, dynamic analysis, and AI firewalls.
</a>

</div>
