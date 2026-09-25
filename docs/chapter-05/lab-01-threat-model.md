---
tags:
  - Chapter 5
  - Lab
---

# Lab 5.1 — Threat Modeling an AI System

<ul class="caisp-meta">
  <li>Difficulty: Intermediate</li>
  <li>Time: 90–120 min</li>
  <li>Internet: Not required</li>
  <li>The capstone exercise</li>
</ul>

!!! lab "What you will do"
    Produce a **complete threat model** for an AI system — DFD, trust boundaries, STRIDE analysis,
    framework cross-references, risk ratings, and an action plan — using a scaffold that makes sure
    nothing is missed.

!!! objective "By the end you will be able to"
    - Work through the four threat modeling questions systematically
    - Apply STRIDE per element and cross-reference OWASP and ATLAS
    - Rate risks and choose treatments defensibly
    - Run a **coverage check** on your own model to find its gaps
    - Produce a report an engineering team can act on

!!! tip "This is the most transferable lab in the course"
    Tools and attack techniques change. The ability to look at an unfamiliar AI system and produce a
    ranked, justified risk assessment does not. This is what senior AI security work actually looks
    like day to day.

---

## Part 1 — Study the worked example

```bash
python labs/chapter-05/threat_model.py --example
```

This walks the four questions against the ACME support assistant from section 5.4.

!!! warning "The tool does not find threats for you"
    No tool can, and any product claiming to should be treated sceptically. This scaffold **holds
    structure** — elements, boundaries, the STRIDE grid, the rating arithmetic, the coverage check.

    **The thinking is yours.** That is not a limitation of the tool; it is the nature of the
    discipline.

### Step 1 output — what are we building?

```text
  PROCESS
    P4   Prompt assembly            [App]  -- Merges system prompt +
                                              retrieved chunks + user input
    P5   Tool orchestrator          [App]  -- Calls lookup_order and issue_refund

  DATA_STORE
    D2   Document corpus            [Data] -- Wiki pages AND customer-submitted tickets
    D4   Prompt logs                [Data] -- Every prompt and response
```

```text
  TB2  Untrusted content -> Prompt
       crosses: d, g
       User input AND retrieved chunks enter the prompt. USUALLY UNMARKED.
```

Note what the element *annotations* do. `D2` says "wiki pages **AND customer-submitted tickets**" —
that single clause is the entire T-01 vulnerability, visible before any threat analysis began.

!!! tip "Write honest annotations"
    The temptation is to write "Document corpus". The value is in writing "wiki pages **and
    customer-submitted tickets**", because that is where the finding lives.

    When you model a real system, push for specificity: *who can write to this? whose identity does
    this run as? what actually gets logged here?*

### Step 3 output — rated threats

```text
  ID      L  I  Score  Band      STRIDE OWASP              Element
  ----------------------------------------------------------------------
  T-01    4  5     20  CRITICAL  T  LLM01,LLM03,LLM08  D2 -> P4 -> P5
  T-02    4  4     16  HIGH      I  LLM06              D1 / P4
  T-03    4  4     16  HIGH      E  LLM07,LLM08        P5 -> D3
  T-04    5  3     15  HIGH      I  LLM06,LLM01        P4
  T-05    3  4     12  HIGH      I  LLM06              D4
```

Observe that T-04 has the **highest likelihood** (5) — extracting a system prompt is trivial — but
lands below T-01 because its impact is lower. That is the formula doing useful work: it separates
"easy" from "important".

### Step 4 output — the action plan

```text
  ID     Treatment  Score -> Resid  Owner        Action
  T-01   Avoid         20 -> 6      Eng lead     Model PROPOSES refunds; human appr...
  T-04   Avoid         15 -> 3      Eng lead     Remove all secrets from the prompt...

  Aggregate risk: 115 -> 43 (63% reduction)

  NOTE: 2 threat(s) treated by AVOIDANCE (removing the capability):
    T-01: 20 -> 6  (-14)
    T-04: 15 -> 3  (-12)
```

!!! success "The conclusion the process reaches on its own"
    The two **largest** risk reductions both come from **avoidance** — removing a capability rather
    than guarding it.

    This is exactly what Lab 3.1 levels 7 and 8 demonstrated experimentally. A completely different
    method, arriving independently at the same answer.

    **When a hands-on experiment and a structured process agree, you have found a real principle.**
    Removing the data and the capability beats filtering.

---

## Part 2 — The coverage check

The fourth question — *did we do a good job?* — is the one everyone skips.

```bash
python labs/chapter-05/threat_model.py --gaps
```

```text
  Elements with no recorded threat:
    [!] E1  Customer
    [!] E2  Attacker
    [!] P3  Guardrails
    [!] P7  Embedding model

  STRIDE categories used:
    S Spoofing                 NO  <-- consider why
    T Tampering                yes
```

The worked example, which looks thorough, has **gaps**:

- **P3 (Guardrails) has no threats.** But Lab 4.6 proved guardrails achieve ~58% recall and can be
  evaded. "Guardrail bypass" belongs in this model.
- **P7 (Embedding model) has no threats.** It is a model too — it has supply-chain provenance
  questions (LLM05) and can be manipulated to skew retrieval.
- **Spoofing is entirely unused.** Yet Lab 3.2 showed users can forge system-message delimiters.

!!! danger "This is the most valuable feature of the lab"
    A threat model that *looks* complete usually is not. The coverage check turns "I think we
    covered everything" into a specific, checkable list.

    **Always run it, and always resolve each gap explicitly** — either add the threat, or record why
    the element is genuinely low-risk. An implicit gap is indistinguishable from an oversight.

---

## Part 3 — Build your own

Now the real work. Choose a system:

<div class="caisp-cards">
<div class="caisp-card caisp-card--static">
  <span class="caisp-kicker">Option A · Easiest</span>
  <span class="caisp-card-title">A lab you built</span>
  <span class="caisp-card-text">The RAG system (Lab 2.6) or the vulnerable app (Lab 4.2). You know it completely.</span>
</div>
<div class="caisp-card caisp-card--static">
  <span class="caisp-kicker">Option B · Best practice</span>
  <span class="caisp-card-title">A product you use</span>
  <span class="caisp-card-text">Any AI feature — a coding assistant, an email summariser, a support bot. Model it <strong>on paper only</strong>; do not test without authorisation.</span>
</div>
<div class="caisp-card caisp-card--static">
  <span class="caisp-kicker">Option C · Most valuable</span>
  <span class="caisp-card-title">A system at work</span>
  <span class="caisp-card-text">If you have a real AI project, model that. Do it <em>with</em> the engineers who built it.</span>
</div>
</div>

### The procedure

**1. Draw the DFD.** On paper or a whiteboard first. Aim for 10–15 elements. Use the checklist:

```bash
python labs/chapter-05/threat_model.py --checklist
```

Confirm you included the elements people always forget:

- [ ] Prompt assembly (where system prompt + context + user input merge)
- [ ] The retrieval corpus **and its write path**
- [ ] Every tool the model can call
- [ ] What happens to model output
- [ ] Logs
- [ ] The model registry / where weights come from
- [ ] Any training or feedback loop

**2. Mark trust boundaries.** Be generous. For every flow ask: *does trust change here?* Explicitly
check for the three AI-specific ones (TB2, TB3, TB4 from section 5.4).

**3. Run STRIDE per element.** Use the generated grid. Tedious by design.

**4. Cross-reference.** For each threat, tag OWASP LLM categories and ATLAS tactics. This is where
Chapters 2 and 3 pay off.

**5. Rate.** Likelihood × Impact, using the tables in section 5.6. Remember:

!!! warning "The two AI-specific rating adjustments"
    - **Rate injection-class likelihood at 4+** if the interface is public. The payload is English;
      ease, not sophistication, drives likelihood.
    - **Rate impact by agency**, not by attack cleverness. What can the system *do*?

**6. Choose treatments.** Mitigate / Transfer / Accept / Avoid. Always ask whether **Avoid** is
available — it usually produces the biggest reduction.

**7. Run the coverage check.** Resolve every gap explicitly.

**8. Write it up.**

```bash
python labs/chapter-05/threat_model.py --report > my_threat_model.md
```

Edit `build_example()` in the script to hold your own elements and threats, then regenerate.

---

## Part 4 — Present it

Threat modeling is a communication exercise as much as a technical one. Practise the summary:

> *"We modelled the [system]. It has [N] elements across [M] trust boundaries. We identified [X]
> threats, of which [Y] are Critical or High. The top risk is [T-01], because [ease] and
> [consequence]. Our strongest recommendation is [avoidance action], which reduces aggregate risk by
> [Z]%. We are accepting [N] low risks, recorded with rationale."*

!!! tip "Lead with the decision, not the analysis"
    Executives want: *what should we do, how bad is it, what will it cost?*

    Engineers want: *what exactly is broken and how do I fix it?*

    Keep the STRIDE grid in an appendix. Put the ranked recommendations on page one.

---

## Break it yourself

- [ ] **Close the gaps in the worked example.** Add threats for P3, P7, E1, E2 and at least one
      Spoofing threat. Re-run `--gaps` until clean.
- [ ] **Model the vulnerable app from Lab 4.2.** You already enumerated its capabilities in Lab 4.4 —
      turn that into a full threat model. How does its aggregate risk compare to ACME's?
- [ ] **Challenge the ratings.** Do you agree T-01 is a 4×5? Argue the other side. Rating disputes
      are where the real analysis happens.
- [ ] **Model the same system twice** — once assuming the model has tool access, once assuming it
      does not. Quantify the aggregate risk difference. That number *is* the cost of agency.
- [ ] **Add an ATLAS narrative.** Write the attack chain for T-01 as a sequence of ATLAS tactics
      (section 2.5). This is the paragraph that impresses in a report.
- [ ] **Do it as a group.** Threat model with two or three others and compare with your solo attempt.
      Group models are consistently better — notice specifically *what* you missed alone.

---

## What you learned

- Threat modeling is four questions: **what are we building, what can go wrong, what will we do, did
  we do a good job.**
- **Honest element annotations** ("wiki pages *and customer tickets*") often contain the finding.
- STRIDE per element produces coverage that inspiration misses; **tedium is the feature**.
- Cross-referencing **OWASP and ATLAS** makes threats precise and communicable.
- **Rating separates easy from important** — and AI needs two adjustments: high likelihood for
  language-based attacks, impact driven by agency.
- **Avoidance produces the largest risk reductions** — independently confirming Lab 3.1.
- **Always run a coverage check.** A model that looks complete usually is not.

---

<div class="caisp-cards">
<a class="caisp-card" href="review.md">
  <span class="caisp-kicker">Next</span>
  <span class="caisp-card-title">Chapter 5 Review &amp; Quiz</span>
  <span class="caisp-card-text">Consolidate the process that ties the course together.</span>
</a>
</div>
