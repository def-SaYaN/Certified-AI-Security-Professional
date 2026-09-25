---
tags:
  - Chapter 3
  - OWASP
---

# LLM09 — Overreliance

!!! objective "In this section"
    - What hallucination is and why it is intrinsic, not a bug
    - Why fluency and confidence are actively misleading signals
    - Real categories of overreliance harm
    - Mitigations — mostly human and procedural, not technical

---

## What is it?

> **Overreliance** is humans (or systems) trusting LLM output more than its reliability justifies,
> and acting on it without adequate verification.

This is the unusual entry in the Top 10: **the vulnerability is partly in the human, not the
software.** That does not make it less real. Some of the most damaging AI incidents to date have
been overreliance failures.

---

## Understanding hallucinations

> A **hallucination** is model output that is fluent, confident, and factually wrong or entirely
> fabricated.

!!! danger "Hallucination is intrinsic, not a bug to be patched"
    From section 2.2: an LLM generates *statistically plausible continuations*. It does not look
    facts up; it has no internal database to consult and no mechanism that distinguishes "I know
    this" from "this is a likely-sounding sequence of words".

    **Producing fluent-and-correct text and fluent-and-wrong text use the identical mechanism.**
    There is no internal signal separating them. This is why hallucination cannot simply be
    engineered away, and why LLM09 sits in the "architectural, managed not solved" group alongside
    LLM01.

### Why hallucinations are so convincing

<dl class="caisp-terms" markdown>

<dt>Fluency is decoupled from accuracy</dt>
<dd>Humans use fluency, coherence, and confident phrasing as proxies for competence — a heuristic
that works reasonably well for people and fails completely for LLMs. A model is exactly as
articulate when wrong as when right.</dd>

<dt>Plausible detail</dt>
<dd>Hallucinations come with specifics: invented case citations with realistic numbering, fake API
methods with sensible names, fabricated statistics with decimal places. Detail reads as
credibility.</dd>

<dt>No uncertainty signalling</dt>
<dd>A well-calibrated expert says "I'm not sure". Models typically do not — and when they express
confidence, that expression is generated text, not a genuine measure of reliability. (Even
numerical confidence scores are certainty, not correctness — Lab 2.8.)</dd>

<dt>Mostly right, which is worse</dt>
<dd>If models were usually wrong, nobody would trust them. They are usually right, which trains
users to stop checking — precisely when the occasional confident error does the most damage.</dd>

</dl>

---

## Overreliance in practice

<dl class="caisp-terms" markdown>

<dt>Fabricated citations and references</dt>
<dd>Models invent plausible-looking sources — legal cases, academic papers, standards clauses —
with realistic formatting. Professionals have been sanctioned for submitting work containing
AI-fabricated citations they did not verify.</dd>

<dt>Insecure or incorrect generated code</dt>
<dd>Developers accept AI-suggested code that compiles, passes a quick look, and contains a
vulnerability. The code learned from public examples, including insecure ones.</dd>

<dt>Package hallucination</dt>
<dd>From section 2.4: the model invents a library name, an attacker has pre-registered it, and the
trusting developer installs malicious code. Overreliance becomes a supply-chain compromise.</dd>

<dt>Fabricated policy and commitments</dt>
<dd>A customer-facing assistant invents a refund policy, discount, or guarantee. Organisations have
been held to commitments their chatbot made.</dd>

<dt>Automation bias in analysis</dt>
<dd>An analyst accepts a model's triage verdict without independent checking. The clean label and
confident tone suppress the scepticism a raw data dump would have triggered.</dd>

<dt>Compounding errors in chained systems</dt>
<dd>One model's output feeds another's input. An early hallucination is treated as established fact
downstream and amplified.</dd>

</dl>

!!! warning "Overreliance is the multiplier on every other AI weakness"
    A hallucination that nobody acts on is harmless. A hallucination that a human or downstream
    system acts on without verification is the incident.

    Note the structural parallel with LLM08: **agency determines the impact of an attack;
    overreliance determines the impact of an error.** Both are about what happens *after* the
    model produces something bad.

---

## Mitigating overreliance

The mitigations here are unusually human and procedural — which is exactly why technical teams
neglect them.

<dl class="caisp-terms" markdown>

<dt>Ground outputs in verifiable sources (RAG with citations)</dt>
<dd>Retrieval reduces fabrication and, crucially, gives users something to check. Citations turn an
unverifiable claim into a verifiable one — but only if users actually follow them.</dd>

<dt>Communicate uncertainty in the interface</dt>
<dd>Design the UI to signal that output is AI-generated and may be wrong. Persistent, specific
labelling beats a one-time disclaimer users dismiss.</dd>

<dt>Human verification proportional to stakes</dt>
<dd>Define which decisions require independent verification. Low stakes: spot-check. High stakes
(legal, medical, financial, security): mandatory independent confirmation, every time.</dd>

<dt>Automated cross-checking</dt>
<dd>Where the domain allows it, verify programmatically: does the cited case exist? does the
package exist on the registry? does the API method exist in the docs? do the numbers reconcile?
This catches a large fraction of hallucinations cheaply.</dd>

<dt>Treat generated code as untrusted third-party code</dt>
<dd>Review it, scan it, and test it exactly as you would code from an unvetted external
contributor — because that is a fair description of its provenance.</dd>

<dt>Train users on the actual failure mode</dt>
<dd>People need to understand <em>why</em> models hallucinate, not merely that they sometimes do.
Users who understand it is fluent pattern-completion, not retrieval, calibrate far better.</dd>

<dt>Measure your own hallucination rate</dt>
<dd>Do not guess. Build an evaluation set with known answers and measure how often your specific
deployment fabricates. <strong>Lab 3.4</strong> does exactly this. A measured rate lets you make an
informed risk decision; an assumption does not.</dd>

</dl>

!!! tip "The framing that lands with non-technical stakeholders"
    An LLM is a **brilliant, fast, confident intern who never says "I don't know"**.

    Extremely useful. Never left unsupervised on anything that matters. Everything it produces gets
    checked before it goes out the door.

    That analogy communicates the right operating posture in one sentence, to an audience who will
    never read the OWASP list.

---

!!! question "Check your understanding"
    ??? success "Why is hallucination intrinsic rather than a fixable bug?"
        LLMs generate statistically plausible continuations rather than retrieving verified facts.
        Correct and incorrect output are produced by the identical mechanism, with no internal
        signal distinguishing them — so there is nothing to patch.

    ??? success "Why is a model that is usually right more dangerous than one that is usually wrong?"
        Because reliability trains users to stop verifying. A frequently-wrong model keeps people
        sceptical; a mostly-right model builds trust that is then misapplied to the occasional
        confident error.

    ??? success "Compare LLM08 and LLM09 structurally."
        Both govern what happens after the model produces something bad. Excessive agency (LLM08)
        determines the impact of a successful *attack*; overreliance (LLM09) determines the impact
        of an unforced *error*. Both are mitigated by constraining what follows the model's output.

---

<div class="caisp-cards">
<a class="caisp-card" href="10-model-theft.md">
  <span class="caisp-kicker">Next · LLM10</span>
  <span class="caisp-card-title">Model Theft</span>
  <span class="caisp-card-text">The model as the asset being stolen.</span>
</a>
</div>
