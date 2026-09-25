---
tags:
  - Wrap-Up
---

# Course Wrap-Up

<ul class="caisp-meta">
  <li>7 chapters</li>
  <li>29 labs</li>
  <li>~65 hours</li>
</ul>

You have finished. If you did the labs rather than only reading them, you can now do something most
people in this industry cannot: **look at an AI system and tell someone, precisely and defensibly,
what is wrong with it and what to do about it.**

---

## What you actually learned

Not the chapter list — the capabilities.

<div class="caisp-cards" markdown>

<div class="caisp-card" markdown>
<span class="caisp-kicker">Understand</span>
### How AI works
Tokens, attention, transformers, RAG, fine-tuning, agents. You can read an AI architecture diagram
and know what each box does.
</div>

<div class="caisp-card" markdown>
<span class="caisp-kicker">Attack</span>
### How it breaks
Prompt injection direct and indirect, adversarial examples, backdoors, model extraction, agent
hijacking — demonstrated, not just described.
</div>

<div class="caisp-card" markdown>
<span class="caisp-kicker">Defend</span>
### How to secure it
Guardrails, scanning, SBOMs, signing, least privilege — and an honest sense of what each achieves.
</div>

<div class="caisp-card" markdown>
<span class="caisp-kicker">Assess</span>
### How to evaluate it
Threat modeling, risk rating, evaluation harnesses, agent assessment methodology.
</div>

<div class="caisp-card" markdown>
<span class="caisp-kicker">Communicate</span>
### How to make it matter
OWASP, ATLAS, STRIDE, NIST AI RMF, ISO 42001, EU AI Act — the vocabulary that turns findings into
action.
</div>

</div>

---

## The four ideas worth keeping

Strip away the detail and the course argues four things. If you retain nothing else, retain these.

!!! success "1. You cannot prevent prompt injection. You can prevent it from mattering."
    Instructions and data share one channel, and no fix exists. Lab 3.1 proved that every defence
    which *asks the model to behave* can be talked around, and that only removing the **data**
    (LLM06) and the **capability** (LLM08) actually holds.

    Lab 7.2 proved it again at the agent level: the hardened agent was **no better at detection** and
    stopped 4/4 attacks anyway.

!!! success "2. Severity is determined by agency, not by the attack."
    The same injection produces an embarrassing reply or a fraudulent refund depending entirely on
    what the system is permitted to do.

    **"What is the worst thing this could do if fully compromised?"** is the highest-value question
    in AI security, and the answer is an architectural decision, not a filtering one.

!!! success "3. You cannot inspect a model, so trust must come from provenance."
    Backdoors are invisible (Lab 2.9), edits leave benchmarks flat (Lab 6.1), and the trigger space is
    unbounded (Lab 6.2). Scanning catches malicious *files*, never malicious *models*.

    Signature verification is O(1) and definitive for tampering. Inventory and signing are the
    highest-value investments most organisations can make.

!!! success "4. Measure, do not assume."
    Your hallucination rate. Your guardrail's recall. Your injection success rate. Your aggregate risk
    before and after treatment.

    Generation is non-deterministic, so a single passing test proves nothing. **A number you measured
    beats a claim you believed** — and it is also what converts engineering judgement into
    organisational decisions.

---

## What to do next

### This week

- [ ] **Pick a real AI system** — one you use or work on — and threat model it (Chapter 5). Two
      hours, on paper. This single exercise exercises the whole course.
- [ ] **Run one lab again from scratch**, without the walkthrough. Struggling is information.
- [ ] **Write your one-page-per-chapter cheat sheets** from memory, then correct them against the
      course. The corrections are your gap list.

### Before the exam

- [ ] Work through the [Certification Guide](../start-here/certification.md) preparation plan.
- [ ] Confirm you can tick the readiness checklists at the end of every chapter.
- [ ] Drill the frameworks: OWASP LLM Top 10 in order, STRIDE, ATLAS tactics, the four NIST AI RMF
      functions.
- [ ] Do a full mock scenario: threat model an unfamiliar product end to end, timed.

### In your career

<dl class="caisp-terms" markdown>

<dt>Build the inventory</dt>
<dd>If your organisation has AI in production, ask: <em>"list every model running, with version,
origin, and base model."</em> If nobody can, you have found your first project — and it is the
control most commonly missing (section 6.4).</dd>

<dt>Ask the three questions</dt>
<dd>Of every AI system you meet: <strong>What can it do? Who can influence it? What happens to its
output?</strong> They will find you more than most tools will.</dd>

<dt>Build one evaluation harness</dt>
<dd>Pick hallucination, injection, or guardrail coverage. Measure it. Track it across changes. You
will immediately be doing something most teams are not.</dd>

<dt>Speak both languages</dt>
<dd>Technical precision with engineers; framework and risk language with leadership. The people who
can do both are the ones who get AI security funded.</dd>

<dt>Stay current deliberately</dt>
<dd>Section 7.1 gave you a workflow. Use it — the field moves faster than any course can.</dd>

<dt>Teach someone</dt>
<dd>Answer questions in the <a href="../start-here/support.md">community</a> for chapters you have
finished. Teaching is the fastest way to consolidate your own understanding.</dd>

</dl>

---

## A closing note on ethics

You now have genuine offensive capability against AI systems. That was necessary — you cannot defend
failure modes you have never induced.

It also carries an obligation that does not expire with the course.

!!! danger "The standard, one final time"
    - Practise only on systems you **own** or have **explicit written authorisation** to test.
    - Disclose responsibly, and give people reasonable time to fix things.
    - Remember the downstream human. Many AI failures are not "the server crashed" — they are a real
      person receiving a harmful output, a leaked record, or an unjust decision.
    - Do not build the weapon. Studying how criminal tools work is defensive intelligence; building
      or distributing one is a crime.

    Every lab in this course was designed to be local and self-contained precisely so you could
    develop real skill without ever crossing that line. Keep it that way.

---

## Thank you

AI security is a field roughly three years old in its current form. The practices are still being
worked out, the tooling is immature, and much of the important work has not been done yet.

That is an unusual opportunity. You are not late to this field. **You are early, and you are now
equipped.**

Go and find the systems nobody has looked at yet.

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../start-here/certification/" markdown>
<span class="caisp-kicker">Next step</span>
### Certification Guide
Prepare for and book the exam.
</a>

<a class="caisp-card" href="../start-here/glossary/" markdown>
<span class="caisp-kicker">Reference</span>
### Glossary
Every term, one sentence each.
</a>

<a class="caisp-card" href="../start-here/support/" markdown>
<span class="caisp-kicker">Community</span>
### Course Support
Lifetime access. Stay connected; pay it forward.
</a>

</div>
