---
tags:
  - Chapter 6
  - Lab
---

# Lab 6.3 — Scanning Models and Detecting Malicious Code

<ul class="caisp-meta">
  <li>Difficulty: Intermediate</li>
  <li>Time: 50–60 min</li>
  <li>Internet: Not required</li>
  <li>Defensive lab</li>
</ul>

!!! lab "What you will do"
    Build and run a **five-layer model scanner**, then confront its most important property: the
    layer that matters most is the one that does not examine the file at all.

!!! objective "By the end you will be able to"
    - Implement format, opcode, structure, integrity, and provenance checks
    - Explain what each layer catches and what it cannot
    - Explain why **provenance outranks scanning**
    - Wire model scanning into a pipeline as a blocking control

---

## Run it

```bash
python labs/chapter-06/model_scanner.py --scan-all
```

This builds four sample artefacts and scans each through all five layers.

---

## The five layers

### Layer 1 — Format

```text
  [OK      ] format     '.safetensors' cannot execute code on load. Good choice.
  [WARNING ] format     '.pkl' is a code-executing format. Prefer .safetensors.
```

The cheapest and most valuable check. **The format alone tells you whether code execution is even
possible** (section 1.4). Before any deep analysis, ask what kind of file this is.

### Layer 2 — Opcode analysis

```text
  [CRITICAL] opcode     malicious_model.pkl: dangerous import(s) ['system']
                        combined with a call opcode. This file executes code
                        on load. DO NOT LOAD.
```

This is Lab 4.3's technique, generalised: disassemble the pickle stream **without executing it**,
and flag dangerous imports combined with call opcodes.

Note the scanner also handles **ZIP-based PyTorch files** — `.pt` and `.pth` are usually archives
containing a pickle, so a naive scanner that only looks at raw bytes misses them entirely.

!!! tip "Note the honest INFO on the clean model"
    ```text
    [INFO] opcode  clean_model.pkl: object-construction opcodes present
                   (normal for many models, but it is the mechanism
                   attackers use).
    ```

    Good tooling distinguishes *"this is suspicious"* from *"this is how the format works"*. A
    scanner that screams CRITICAL at every `REDUCE` opcode will be ignored within a week.

### Layer 3 — Structure

Model archives should contain model things. An executable, script, or shared library inside a model
archive is a strong signal:

```python
if low.endswith((".py", ".sh", ".exe", ".dll", ".so", ".bat")):
    findings.append(Finding("structure", "CRITICAL",
        f"Executable/script file inside model archive: {n}"))
```

### Layer 4 — Integrity

```text
  [WARNING ] integrity  No expected hash recorded. sha256=5dc6672e02c9ef39...
                        Pin this in your manifest.
```

Compares the file against a **pinned hash** from your manifest. This detects substitution — the
attack where the registry serves you a different artefact than the one you vetted.

If you have no pinned hash, you cannot detect substitution at all, which is why the scanner warns.

### Layer 5 — Provenance

```text
  [CRITICAL] provenance NO SIGNATURE. You cannot establish who produced this
                        file. This is the finding that matters most.
  [WARNING ] provenance No model card. Training data, intended use and
                        limitations are undocumented.
```

!!! danger "Note which layer is rated CRITICAL"
    A missing signature outranks almost everything else, because it means **you cannot answer the
    only trust question that is answerable** for an artefact you cannot inspect (section 6.5).

    Most teams' model "security" stops at layer 2. Layer 5 is where the real assurance lives.

---

## Reading the results

```text
  REJECT   clean_model.pkl
  REVIEW   documented_model.safetensors
  REJECT   malicious_model.pkl
  REJECT   safe_model.safetensors
```

Study why `clean_model.pkl` is **REJECT** despite containing no malicious code:

- It is a pickle (code-executing format)
- It has no pinned hash
- **It has no signature**
- It has no model card

The model is benign, and you have **no way to establish that**. Rejecting it is correct.

And `documented_model.safetensors` is only **REVIEW** rather than ACCEPT — it has a safe format, a
model card, and signature material present, but the scanner explicitly notes:

```text
  [INFO] provenance  Signature material present — VERIFY it (see Lab 6.5).
                     Presence is not validity.
```

!!! tip "A signature file's *existence* proves nothing"
    Anyone can create a file called `model.safetensors.sig`. Only **verification** against an
    expected identity means anything. A scanner that treats "a .sig file exists" as a pass has
    created a trivially bypassable control.

---

## The limitation you must be able to state

```text
  Note what the scanner CAN and CANNOT tell you:
   * It caught the malicious FILE (opcode layer).
   * It flagged the missing signatures (provenance layer).
   * It CANNOT tell you whether 'clean_model.pkl' contains a
     BACKDOOR in its weights. No scanner can.
```

!!! danger "Malicious file ≠ malicious model"
    | Threat | Detectable by scanning? |
    |---|---|
    | Code execution on load | **Yes** — layer 2 |
    | Executable smuggled in an archive | **Yes** — layer 3 |
    | File substitution | **Yes** — layer 4, if pinned |
    | **Backdoor in the weights** | **No** (Lab 2.9) |
    | **Edited/poisoned behaviour** | **No** (section 6.2) |
    | Unknown origin | Flagged, resolved only by layer 5 |

    A backdoored model is a *structurally perfect* file. Correct format, no dangerous opcodes, clean
    archive, matching hash. It passes layers 1–4 completely.

    **This is why the chapter's conclusion is provenance, not scanning.** Scanning is a useful,
    cheap filter for a specific class of attack. It is not model assurance.

---

## Break it yourself

- [ ] **Evade layer 2.** Build a malicious pickle using `builtins.eval` or `importlib` instead of
      `os.system`. Does the scanner catch it? Extend `DANGEROUS_MODULES` until it does — then find
      another bypass. How many rounds before you conclude this is asymmetric?
- [ ] **Add a manifest.** Create `_samples/manifest.json` mapping filenames to their real SHA-256
      digests. Re-run and watch layer 4 turn OK. Then modify a file and watch it turn CRITICAL.
- [ ] **Add a layer 6: size and shape sanity.** Does the file size match what the model card claims?
      Is a "7B parameter model" plausibly 50 MB?
- [ ] **Scan a real model.** Point it at a genuine downloaded model. What does it say about the files
      you have been loading without thinking?
- [ ] **Make it a CI gate.** Wrap it in a script that exits non-zero on REJECT, and run it on every
      model pull. That is a production control.
- [ ] **Integrate Lab 6.5.** Replace the placeholder provenance check with real Cosign verification,
      so `REVIEW` can become a genuine `ACCEPT`.

---

## What you learned

- A model scanner has layers: **format, opcode, structure, integrity, provenance** — each catching a
  different class of problem.
- **Format is the cheapest and most valuable check** — SafeTensors eliminates whole categories.
- Opcode analysis inspects **without executing**, and must handle ZIP-based PyTorch archives.
- Good tooling distinguishes *suspicious* from *normal*, or it gets ignored.
- **A signature file existing is not verification.**
- **Scanning catches malicious files, never malicious models** — which is why provenance is rated
  CRITICAL and why Lab 6.5 is the chapter's conclusion.

---

<div class="caisp-cards">
<a class="caisp-card" href="lab-04-sbom.md">
  <span class="caisp-kicker">Next · Lab 6.4</span>
  <span class="caisp-card-title">Generating an SBOM</span>
  <span class="caisp-card-text">Know what you have, before you try to verify it.</span>
</a>
</div>
