---
tags:
  - Chapter 6
  - Lab
---

# Lab 6.4 — Generating an SBOM (and extending it to an MLBOM)

<ul class="caisp-meta">
  <li>Difficulty: Beginner</li>
  <li>Time: 40–50 min</li>
  <li>Internet: Required (install)</li>
  <li>Defensive lab</li>
</ul>

!!! lab "What you will do"
    Generate a real SBOM for an AI project, query it the way you would during an incident, then
    extend the concept to cover the components an SBOM misses: **models and datasets**.

!!! objective "By the end you will be able to"
    - Generate a CycloneDX SBOM
    - Query an SBOM to answer "are we affected?"
    - Explain the gap an SBOM leaves in an AI project
    - Construct an MLBOM entry with the fields that matter

---

## Part 1 — Generate an SBOM

```bash
pip install cyclonedx-bom
cyclonedx-py environment -o sbom.json
```

Inspect what you produced:

```bash
python -c "
import json
d = json.load(open('sbom.json'))
print('format    :', d['bomFormat'], d['specVersion'])
print('components:', len(d['components']))
for c in d['components'][:5]:
    print('   ', c['name'], c['version'], '|', c.get('purl',''))
"
```

```text
format    : CycloneDX 1.6
components: 67
    Jinja2 3.1.6 | pkg:pypi/jinja2@3.1.6
    Markdown 3.11 | pkg:pypi/markdown@3.11
    MarkupSafe 3.0.3 | pkg:pypi/markupsafe@3.0.3
    PyYAML 6.0.3 | pkg:pypi/pyyaml@6.0.3
```

**67 components** in a small environment. A real AI project routinely exceeds 200. That number is
the argument for having an SBOM at all — nobody tracks that manually.

!!! note "purl — the package URL"
    `pkg:pypi/jinja2@3.1.6` is a **Package URL**, a standard identifier for a component. It is what
    makes SBOMs machine-comparable: vulnerability databases speak purl, so matching is exact rather
    than fuzzy string comparison on names.

---

## Part 2 — Use it (the part people skip)

An SBOM you never query is paperwork. Here is the query that justifies its existence.

**Scenario:** a critical vulnerability is announced in a library. Your CTO asks: *are we affected?*

```python title="check_affected.py"
import json, sys

sbom = json.load(open("sbom.json"))
target = sys.argv[1].lower()

hits = [c for c in sbom["components"] if target in c["name"].lower()]
if hits:
    for c in hits:
        print(f"AFFECTED: {c['name']} {c['version']}  ({c.get('purl','')})")
else:
    print(f"Not present: {target}")
```

```bash
python check_affected.py jinja2
python check_affected.py log4j
```

!!! success "Seconds, not days"
    Without an SBOM, answering that question means manually inspecting every repository, container,
    and environment — the kind of work that takes a team days while the incident clock runs.

    With one, it is a query. **That difference is the entire business case.**

### Other real uses

- **Diff between releases.** A new dependency appearing that nobody added is a strong signal.
  ```bash
  cyclonedx-py environment -o sbom-new.json
  diff <(jq -r '.components[].purl' sbom.json | sort) \
       <(jq -r '.components[].purl' sbom-new.json | sort)
  ```
- **Licence compliance.** Flag licences incompatible with your use.
- **Gate the build.** Fail CI if a disallowed component appears.

---

## Part 3 — The gap

Now the AI-specific point. Look hard at what your SBOM contains:

```text
  transformers 4.40.2   ✅ listed
  torch 2.2.0           ✅ listed
  numpy 1.26.4          ✅ listed

  distilbert-base-uncased        ❌ NOT LISTED
  acme/support-classifier-v3     ❌ NOT LISTED
  support-tickets-v7.parquet     ❌ NOT LISTED
```

!!! danger "Your SBOM covers the half of your supply chain that was already easiest to secure"
    Models and datasets **are dependencies**. They ship in your product, shape its behaviour, and
    carry risk (sections 6.1–6.2). Standard SBOM tooling does not see them at all.

    This is the same gap Lab 4.1 identified from the SCA side, stated again because it is the single
    most commonly missed thing in AI supply chain practice.

---

## Part 4 — Build an MLBOM entry

An **MLBOM** extends the inventory to AI components. Standards work is ongoing (CycloneDX has been
extending its specification for ML), but **the concept matters more than the current tooling** — an
accurate spreadsheet beats an unimplemented standard.

The fields that matter:

```json title="mlbom.json"
{
  "mlComponents": [
    {
      "type": "model",
      "name": "acme/support-classifier",
      "version": "3.1.0",
      "revision": "a1b2c3d4e5f67890",
      "format": "safetensors",
      "sha256": "9f8e7d6c5b4a3210...",
      "publisher": "ACME ML Platform Team",
      "signature": "cosign keyless, identity ml-platform@acme-corp.com",
      "base_model": {
        "name": "distilbert-base-uncased",
        "source": "huggingface.co/distilbert",
        "revision": "1c4513b2eedbda136f57676a34eea67aba266e5c"
      },
      "license": "Apache-2.0",
      "model_card": "docs/models/support-classifier.md",
      "intended_use": "Support ticket classification",
      "out_of_scope": "Decisions affecting individual rights"
    },
    {
      "type": "dataset",
      "name": "support-tickets-v7",
      "version": "7.0.0",
      "sha256": "1a2b3c4d5e6f7890...",
      "source": "internal",
      "collection": "Exported from Zendesk, PII-scrubbed",
      "license": "Internal use only",
      "records": 48213
    }
  ]
}
```

!!! tip "The fields that earn their place"
    <dl class="caisp-terms" markdown>

    <dt><code>revision</code> / <code>sha256</code></dt>
    <dd>Pin to an exact artefact, not a moving tag. A hub reference without a revision is the AI
    equivalent of <code>:latest</code> (section 4.3).</dd>

    <dt><code>base_model</code></dt>
    <dd><strong>The provenance chain.</strong> You inherit everything in the base (section 2.3), so
    the inventory must record it or your risk picture is incomplete.</dd>

    <dt><code>signature</code></dt>
    <dd>Links to Lab 6.5. Recording that something is signed, and by whom, is what makes verification
    enforceable.</dd>

    <dt><code>license</code></dt>
    <dd>Model *and* dataset licences. Some models restrict commercial use or downstream training —
    a real legal exposure that no SCA tool will flag.</dd>

    <dt><code>out_of_scope</code></dt>
    <dd>From the model card. Deploying outside documented intended use is a risk decision, and
    increasingly a compliance one (Chapter 7).</dd>

    </dl>

---

## Part 5 — The inventory test

!!! warning "Try this on any organisation with AI in production"
    Ask: **"List every model running in production, with its version, origin, and base model."**

    Very often nobody can. Models arrive through notebooks, get baked into containers, and are
    pulled by scripts nobody catalogued. There is no registry and no inventory.

    **You cannot secure a supply chain you have not enumerated.** Inventory is not a sophisticated
    control — it is the *first* one, and the one most commonly missing (section 6.4, SCVS).

    If you are starting an AI supply chain programme, this is where you start. Not with scanners.

---

## Break it yourself

- [ ] **Write an MLBOM generator.** Scan a directory for model files and emit entries with name,
      size, format, and SHA-256 auto-populated. Leave provenance fields for humans.
- [ ] **Combine SBOM + MLBOM.** Produce a single document covering libraries, models, and datasets.
      That is a complete AI bill of materials.
- [ ] **Add a CI check.** Fail the build if a model file exists that has no MLBOM entry. This is how
      an inventory stays accurate instead of decaying.
- [ ] **Diff two SBOMs.** Install a package, regenerate, and diff. Now imagine that diff in a pull
      request review — would an unexpected dependency stand out?
- [ ] **Answer an incident question.** Pick any component in your SBOM, imagine a critical CVE, and
      time how long it takes you to determine exposure and blast radius.
- [ ] **Audit a public model.** Pick one on Hugging Face. Can you fill in every MLBOM field? What is
      missing, and what does that absence tell you?

---

## What you learned

- An **SBOM** is a machine-readable component inventory; CycloneDX and SPDX are the formats.
- **purl** identifiers make SBOMs machine-comparable against vulnerability data.
- The value is in **querying** it — "are we affected?" answered in seconds rather than days.
- **SBOMs are blind to models and datasets**, which is half of an AI supply chain.
- An **MLBOM** adds models, base models, datasets, hashes, signatures, licences, and intended use.
- **Inventory is the first control, and the most commonly missing one.**

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../lab-05-signing/" markdown>
<span class="caisp-kicker">Next · Lab 6.5</span>
### Signing & Verifying Models
Now that you know what you have, prove it has not been tampered with.
</a>

</div>
