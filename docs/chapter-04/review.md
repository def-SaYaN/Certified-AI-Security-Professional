---
tags:
  - Chapter 4
  - Review
---

# Chapter 4 — Review & Quiz

<ul class="caisp-meta">
  <li>Time: 35 min</li>
  <li>20 questions</li>
  <li>Self-assessed</li>
</ul>

---

## The one-page summary

### DevOps → DevSecOps → MLOps

- **DevOps**: automation, CI/CD, IaC, monitoring, shared ownership.
- **DevSecOps**: security integrated at every stage — **shift left**, because fixing a flaw early
  costs a fraction of fixing it in production.
- **MLOps is harder**: you must version code **+ data + models**; the primary artefact **cannot be
  reviewed**; failures are **silent degradations**, not crashes.

### The pipeline is the softer target

| | Attack the model | Attack the pipeline |
|---|---|---|
| Skills | AI-specific | Conventional infra |
| Defences faced | Guardrails, filters | Often minimal |
| Persistence | Per-session | **Durable in the artefact** |
| Reach | One conversation | **Every deployment** |
| Detection | Moderate | **Low** |

**The model registry is the highest-leverage target** — everything downstream inherits what you
put there, and nobody can code-review a model.

### The three cases

| Case | Root cause | Lesson |
|---|---|---|
| **Hugging Face** | Code-executing format + misplaced trust | Models are executable content |
| **NotPetya** | Compromised trusted update channel | Your security = your dependencies' security |
| **SAP AI Core** | Weak isolation of untrusted workloads | ML platforms run hostile code by design |

### The defensive stack

| Layer | Answers | Tools |
|---|---|---|
| **SCA** | Are my dependencies vulnerable? | `pip-audit`, Trivy, Snyk |
| **Static (code)** | Is my code dangerous? | Bandit, Semgrep |
| **Static (model)** | Is this *file* malicious? | `picklescan` |
| **Dynamic** | How does it behave? | TextAttack, injection suites, eval harnesses |
| **Guardrails** | Filter runtime input/output | LLM Guard, NeMo, hand-built |

### Sentences to remember

> **Scanning catches malicious files. It does not catch malicious models.**

> **A guardrail is a filter, not a boundary.**

> **Generic SAST finds generic flaws — and misses everything AI-specific.**

> **Test LLM systems statistically: report rates, not pass/fail.**

---

## Quiz

??? question "1. What does 'shift left' mean and why does it work economically?"
    Moving security activities earlier in the lifecycle. It works because the cost of fixing a flaw
    rises steeply the later it is found — minutes during coding versus incident response, emergency
    patching, and customer impact in production.

??? question "2. Name three ways MLOps is harder to secure than traditional DevOps."
    You must version and protect data and models as well as code; the primary artefact (weights)
    cannot be reviewed like source; and failures are silent degradations rather than loud crashes.

??? question "3. Why is the model registry the highest-leverage pipeline target?"
    It is the single point through which every model reaches production. A substituted backdoored
    model propagates automatically to all downstream deployments, and because weights cannot be
    reviewed, the substitution is unlikely to be detected.

??? question "4. Why does a production-to-training feedback loop create risk?"
    It creates a direct channel from any user to your next model, letting attackers inject crafted
    examples into future training data — turning a runtime interaction into training-time poisoning.

??? question "5. Why might an attacker prefer the pipeline to the model?"
    Conventional skills suffice, defences are weaker, persistence is durable in the artefact, reach
    extends to every deployment, and detection likelihood is low.

??? question "6. Why is NotPetya on an AI security syllabus?"
    It shows that compromising a trusted dependency defeats victims with no vulnerability of their
    own. AI is *more* exposed because model weights, unlike software binaries, cannot be
    meaningfully inspected for tampering.

??? question "7. What made malicious models on Hugging Face possible?"
    A format (pickle) that executes code on load, plus a developer trust model treating model
    downloads as data rather than executables.

??? question "8. Why is isolation critical for a managed ML training platform?"
    Executing arbitrary customer code *is* the product, so every workload must be treated as
    hostile — requiring container isolation, network segmentation, and no path to the control plane
    or other tenants.

??? question "9. Why is SCA necessary but insufficient for AI projects?"
    It covers code dependencies against CVE databases, but models and datasets are also dependencies
    and appear in no such database. The AI-specific supply chain is left uncovered.

??? question "10. What is the most common failure mode of an SCA programme?"
    Treating zero findings as the goal, chasing every low-severity item, exhausting the team's
    patience, and causing the tool to be ignored — including the finding that mattered. Triage by
    exploitability.

??? question "11. Explain mechanically why loading a pickle file can execute code."
    Pickle supports reconstructing arbitrary Python objects. An object's `__reduce__` method
    specifies a callable and arguments that pickle **calls** during loading. `GLOBAL` + `REDUCE` in
    the opcode stream means "import this function and run it" — with no sandbox or confirmation.

??? question "12. Which two opcodes indicate code execution in a pickle file?"
    `GLOBAL` / `STACK_GLOBAL` (import a callable by name) followed by `REDUCE` (call it).

??? question "13. What does picklescan catch, and what does it miss?"
    It catches dangerous imports in pickle files — malicious *files* — without executing them. It
    misses backdoors in the weights, novel evasions of its pattern list, and anything about model
    *behaviour*. Malicious files and malicious models are different problems.

??? question "14. Why is SafeTensors the real fix rather than scanning?"
    It stores only numbers and metadata with no mechanism to execute code. Scanning detects known
    bad patterns; SafeTensors eliminates the capability entirely.

??? question "15. Which vulnerabilities in the Lab 4.2 app did Bandit miss, and why?"
    Secrets in the system prompt, the prompt injection surface, and model output reaching a template
    renderer. Bandit cannot know that a string is a *system prompt*, that a variable holds *model
    output*, or that a function is a *model-callable tool*.

??? question "16. Name the three dimensions of agency and how you would score the Lab 4.2 app."
    Functionality, permissions, autonomy — each 0–3. The app scores 3/3/3: a generic shell executor,
    application-level credentials with no user context, and no human approval anywhere.

??? question "17. What is the confused deputy condition in an agentic system?"
    Tools act with the *application's* identity rather than the *user's*, so any user who influences
    the model borrows the application's privileges. Fix: authorise in the end user's context on
    every tool call.

??? question "18. Why must tool output be validated before it reaches the next step?"
    Because tool output is untrusted input to the next stage. A URL-fetching tool returns
    attacker-controlled content that then influences subsequent tool calls — chained tools propagate
    indirect injection.

??? question "19. Does Unicode NFKC normalisation defeat homoglyph evasion?"
    **No.** Cyrillic `о` and Latin `o` are semantically distinct codepoints that Unicode
    deliberately keeps separate. You need an explicit homoglyph folding table. Most teams assume
    otherwise and never verify.

??? question "20. Your guardrail scores 58% recall at 100% precision. Is it worth deploying?"
    Yes — it raises attacker cost by stopping lazy attacks, and 100% precision means every alert is
    worth investigating, making it a valuable detection signal. But it is a **filter, not a
    boundary**: it reliably catches syntactic evasions and reliably misses semantic ones. The
    security still comes from minimisation (LLM06) and least privilege (LLM08).

---

## Scoring yourself

| Score | Meaning |
|---|---|
| **17–20** | Excellent. Continue to Chapter 5. |
| **13–16** | Good. Re-read the sections behind your misses. |
| **9–12** | Re-read 4.2 and 4.4, redo Labs 4.3 and 4.6. |
| **Under 9** | Rework the chapter — Chapter 6 builds directly on the supply-chain material. |

---

## Readiness checklist

- [ ] I can explain DevOps, DevSecOps, and why MLOps is harder to secure.
- [ ] I can draw the ML pipeline and name an attack at each stage.
- [ ] I can explain why the registry is the highest-leverage target.
- [ ] I can summarise all three case studies and their transferable lessons.
- [ ] I have run `pip-audit` and can triage findings by exploitability.
- [ ] **I have scanned and detonated a malicious pickle file.**
- [ ] I can explain `GLOBAL` + `REDUCE` and why `__reduce__` is the mechanism.
- [ ] I can articulate the malicious-file vs. malicious-model distinction.
- [ ] I found the vulnerabilities in the Lab 4.2 app and know which SAST missed.
- [ ] I can write a custom Semgrep rule for an AI pattern.
- [ ] I can score a system's agency across the three dimensions.
- [ ] **I have built a guardrail and measured its recall and precision.**
- [ ] I know that NFKC does not fold homoglyphs.
- [ ] I can explain why a guardrail is a filter, not a boundary.

---

<div class="caisp-cards">
<a class="caisp-card" href="index.md">
  <span class="caisp-kicker">Back</span>
  <span class="caisp-card-title">Chapter 4 Contents</span>
  <span class="caisp-card-text">Revisit any section or lab.</span>
</a>
<a class="caisp-card" href="../chapter-05/index.md">
  <span class="caisp-kicker">Next chapter</span>
  <span class="caisp-card-title">Chapter 5 — Threat Modeling AI Systems</span>
  <span class="caisp-card-text">STRIDE, data flow diagrams, AI threat libraries, and risk rating. The chapter that ties everything so far into a repeatable process.</span>
</a>
</div>
