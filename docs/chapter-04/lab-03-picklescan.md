---
tags:
  - Chapter 4
  - Lab
---

# Lab 4.3 — Scanning a Malicious Pickle File

<ul class="caisp-meta">
  <li>Difficulty: Beginner → Intermediate</li>
  <li>Time: 45–60 min</li>
  <li>Internet: Optional</li>
  <li>Defensive lab</li>
</ul>

!!! lab "What you will do"
    Build two model files that look identical, disassemble them **without executing them**, scan
    both, and then prove that loading one runs arbitrary code — with a deliberately harmless
    payload.

!!! danger "Why the payload is harmless by design"
    Our "malicious" model writes a marker file and prints a message. That is sufficient to prove
    arbitrary code executed, which is the entire lesson.

    Swap the payload for a reverse shell or a credential stealer and you have real malware — and
    that is precisely the point you should take away. **The difference between this lab and an
    actual attack is one string.**

!!! objective "By the end you will be able to"
    - Explain *mechanically* why pickle executes code on load
    - Read pickle opcodes and spot the dangerous pattern
    - Use `picklescan` and interpret its output
    - Explain what model scanning catches and — crucially — what it misses

---

## Run the whole walkthrough

```bash
pip install picklescan
python labs/chapter-04/pickle_demo.py --all
```

---

## Step 1 — Two files that look identical

```text
[*] Created labs/chapter-04/_samples/benign_model.pkl    (165 bytes)
[*] Created labs/chapter-04/_samples/malicious_model.pkl (184 bytes)

    Note: both are just '.pkl' files. Nothing about the name, the
    extension, or the size distinguishes them.
```

In a model registry these would sit side by side. Same extension, similar size, both loadable with
`pickle.load()`. There is no visual signal.

---

## Step 2 — Inspect without executing

`pickletools.dis()` disassembles the pickle bytecode the way a disassembler reads a binary — it
**reads** the opcodes rather than **running** them. This distinction is essential: unpickling to
inspect would execute the payload, which is the problem you are trying to avoid.

**The benign file:**

```text
     11: SHORT_BINUNICODE '__main__'
     22: SHORT_BINUNICODE 'BenignModel'
     36: STACK_GLOBAL   <== imports a callable
     39: NEWOBJ         <== object construction
     90: BINFLOAT   0.21
     99: BINFLOAT   -0.44
```

Ordinary: build a `BenignModel`, fill in some floats.

**The malicious file:**

```text
     11: SHORT_BINUNICODE 'posix'
     19: SHORT_BINUNICODE 'system'
     28: STACK_GLOBAL   <== imports a callable
     30: SHORT_BINUNICODE 'python3 -c "open(...).write(...)"'
    ...: REDUCE         <== CALLS it
```

There it is, in plain text: **import `posix.system`, then call it with a command string.**

!!! info "The two opcodes that matter"
    | Opcode | Meaning |
    |---|---|
    | `GLOBAL` / `STACK_GLOBAL` | Import a callable by name (e.g. `os.system`) |
    | `REDUCE` | **Call** it with the supplied arguments |

    `GLOBAL` + `REDUCE` together means *"import this function and run it"*. The benign file has no
    such pair. The malicious one does.

### How the attacker did it

The entire mechanism is one method:

```python
class SuspiciousModel:
    def __reduce__(self):
        return (os.system, ("<any command>",))
```

`__reduce__` tells pickle **how to rebuild this object**. Pickle calls whatever callable
`__reduce__` returns, with the arguments it specifies. There is no sandbox, no allowlist, and no
confirmation prompt.

!!! danger "This is not a bug in pickle"
    Pickle is working exactly as designed. It is a serialisation format for reconstructing arbitrary
    Python objects, and reconstruction means calling code.

    The vulnerability is not in the library — it is in **using a code-execution format as a data
    interchange format for untrusted files**. That design decision propagated into PyTorch, and
    from there into the entire ML ecosystem.

---

## Step 3 — Scan

```text
--- Scanning benign_model.pkl ---
  picklescan: issues=0
    - __main__.BenignModel   [SafetyLevel.Suspicious]
  VERDICT: no known-dangerous imports found.

--- Scanning malicious_model.pkl ---
  picklescan: issues=1
    - posix.system   [SafetyLevel.Dangerous]
  VERDICT: DANGEROUS — do not load this file.
```

`picklescan` walks the opcodes, collects every import, and classifies it. `posix.system` is
unambiguously Dangerous.

Note the benign file is flagged **Suspicious** rather than Safe — because `__main__.BenignModel` is
a custom class the scanner cannot vouch for. That is appropriate caution, and it also illustrates
that these tools produce findings requiring judgement, not simple pass/fail.

!!! tip "Run it directly too"
    ```bash
    picklescan --path labs/chapter-04/_samples/malicious_model.pkl
    ```
    This is the command you would wire into CI.

---

## Step 4 — Prove it executes

```text
--- Loading malicious_model.pkl with pickle.load() ---
  Marker file before load: exists=False
  Loaded object: int
  Marker file after load : exists=True
  Marker contents        : 'arbitrary code executed at load time'

  *** ARBITRARY CODE EXECUTED. You only called pickle.load(). ***
```

The marker file did not exist. You called `pickle.load()`. Now it exists, with content written by
the pickle file.

Note also that the "model" loaded as an `int` — the return value of `os.system()`. The attacker did
not even need to produce a working model; the payload fires during loading, before anyone checks
whether the result is usable.

!!! danger "Scale this mentally"
    A real payload at this point could:

    - Exfiltrate `~/.aws/credentials`, `~/.ssh/`, and environment variables
    - Open a reverse shell to attacker infrastructure
    - Install persistence
    - Move laterally from a data scientist's laptop into the training cluster

    And it runs **wherever models get loaded** — a developer laptop, a CI runner, a GPU training
    node, a production inference server. Those are frequently your most privileged machines.

---

## The defences, in priority order

<dl class="caisp-terms" markdown>

<dt>1. Prefer SafeTensors — the actual fix</dt>
<dd>SafeTensors stores only numbers and metadata. There is <strong>no mechanism</strong> to execute
code on load. Where you control the format, this eliminates the class entirely.</dd>

<dt>2. Scan before loading</dt>
<dd><code>picklescan</code> in CI on every model pull. Cheap, fast, catches real attacks. Not a
guarantee.</dd>

<dt>3. Sandbox untrusted loads</dt>
<dd>No network, no credentials, no production access. Assume the load may be hostile and make that
survivable.</dd>

<dt>4. Verify provenance</dt>
<dd>Signatures and hashes (Chapter 6). The only defence that scales.</dd>

</dl>

!!! warning "The limitation you must be able to articulate"
    **Scanning catches malicious *files*. It does not catch malicious *models*.**

    A backdoored model (Lab 2.9) lives in a structurally innocent file — correct format, no
    dangerous imports, clean scan, 100% accuracy. `picklescan` will pass it happily.

    Two different problems:

    | Threat | Detection |
    |---|---|
    | Malicious **file** (code on load) | Scanning — this lab |
    | Malicious **model** (backdoor in weights) | **Provenance** — Chapter 6 |

    Deploy both. Confusing them is a common and consequential mistake.

---

## Break it yourself

- [ ] **Change the payload.** Make it print your environment variables instead (still harmless).
      Does `picklescan` still flag it? Which import does it catch?
- [ ] **Try to evade the scanner.** Use `builtins.eval` or `importlib` instead of `os.system`. Does
      the scan still catch it? This teaches you what the pattern list covers.
- [ ] **Scan a real model.** Download any `.pt` or `.bin` from Hugging Face and scan it before
      loading. Build the habit.
- [ ] **Convert to SafeTensors.** Take a small real model and save it as `.safetensors`. Attempt to
      embed a payload. You cannot — demonstrate to yourself *why* the format is safe.
- [ ] **Wire it into CI.** Write a shell script that scans every `*.pkl` and `*.pt` in a directory
      and exits non-zero on any Dangerous finding. That is a production-grade control in ten lines.
- [ ] **Sandbox a load.** Run the malicious sample inside a container with no network and no mounted
      credentials. Confirm the payload runs but achieves nothing useful.

---

## What you learned

- Pickle's `__reduce__` lets a file specify a **function call executed at load time**.
- `GLOBAL` + `REDUCE` in the opcode stream is the signature of code execution.
- `pickletools.dis()` inspects **without executing**; `picklescan` automates the analysis.
- Loading a model runs wherever your pipeline loads models — often your most privileged hosts.
- **SafeTensors is the real fix**; scanning is a useful filter; sandboxing limits damage;
  provenance is what scales.
- **Malicious files ≠ malicious models.** Scanning addresses only the first.

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../lab-04-agent-scanning/" markdown>
<span class="caisp-kicker">Next · Lab 4.4</span>
### Scanning for Agent Vulnerabilities
Assess an agentic system's tools and permissions systematically.
</a>

</div>
