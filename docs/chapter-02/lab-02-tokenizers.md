---
tags:
  - Chapter 2
  - Lab
---

# Lab 2.2 — Exploring How Tokenizers Work

<ul class="caisp-meta">
  <li>Difficulty: Beginner</li>
  <li>Time: 30–40 min</li>
  <li>Internet: Optional</li>
  <li>Runs fully offline</li>
</ul>

!!! lab "What you will do"
    See text the way a model sees it. You will discover why LLMs cannot spell, why some
    languages cost more money, why keyword filters fail, and how a short-looking message can
    inflate your bill.

!!! objective "By the end you will be able to"
    - Explain what a token is and why models use them
    - Predict roughly how text will tokenize
    - Explain why character-level tricks defeat string-matching filters
    - Explain why rate limits must be measured in tokens, not characters

---

## Why this lab matters

This is the shortest lab in the chapter and one of the most valuable. Almost every
"surprising" LLM behaviour — and several vulnerabilities — trace back to one fact:

> **Models do not read letters or words. They read tokens.**

Once that clicks, a lot of security intuition falls into place.

---

## Run it

```bash
python labs/chapter-02/tokenizers.py
```

If `transformers` can reach Hugging Face, this uses the **real GPT-2 tokenizer**. If not, it
automatically falls back to a built-in simulator and tells you so. Either way, the lab works.

To force offline mode:

```bash
python labs/chapter-02/tokenizers.py --offline
```

---

## Demo 1 — Tokens are not words

```text
--- Simple, common words ---
Text       : "The cat sat on the mat."
Characters : 23
Tokens     : 7
Breakdown  : The | ·cat | ·sat | ·on | ·the | ·mat | .

--- One long rare word ---
Text       : "Antidisestablishmentarianism"
Characters : 28
Tokens     : 7
Breakdown  : Anti | dise | stab | lish | ment | aria | nism
```

Two observations:

- **Common words are single tokens.** "cat", "the", "on" each cost one.
- **Rare words shatter into fragments.** The long word costs as much as a whole sentence.

Note the `·` marks a **leading space**. In most tokenizers the space belongs to the token that
follows it — `·cat` is a different token from `cat`. This trips up beginners constantly.

!!! info "Why subword tokenization?"
    Two obvious approaches both fail:

    - **One token per word** — the vocabulary becomes enormous and you can never handle a word
      you have not seen before.
    - **One token per letter** — sequences become extremely long and expensive.

    **Subword** tokenization is the compromise: frequent words get their own token, rare words
    are assembled from pieces. Any word can be represented, and common text stays compact.

---

## Demo 2 — Why LLMs cannot spell

The famous "how many r's in strawberry" failure:

```text
Text       : "strawberry"
Tokens     : 3
Breakdown  : stra | wber | ry
```

The model never receives the letters `s-t-r-a-w-b-e-r-r-y`. It receives three opaque numeric
IDs. Asking it to count letters is like asking you to count the brush strokes in a word you
are reading — the information has been abstracted away.

!!! tip "This is not stupidity, it is architecture"
    People use spelling failures as evidence that LLMs are "dumb". They are evidence of
    something more useful: **the model operates on a representation that does not preserve
    character-level detail.**

    That has a direct security consequence, which is the next demo.

---

## Demo 3 — The language tax

```text
Language    Chars  Tokens  Ratio
------------------------------------------
English        25       8  0.32 tok/char
Spanish        22      14  0.64 tok/char
Japanese       16      16  1.00 tok/char
Hindi          23      19  0.83 tok/char
```

The same sentence costs several times more tokens in some languages than in English, because
tokenizers were predominantly trained on English text.

This is simultaneously:

- A **cost** issue — you are billed per token.
- A **capacity** issue — non-English text fills the context window faster.
- A **fairness** issue — a genuine equity problem in multilingual products.
- A **security** issue — see the next demo.

---

## Demo 4 — Why keyword filters fail

This is the security heart of the lab. Imagine a filter blocking the exact string
`password`:

```text
  [BLOCKED] plain                    -> 2 tokens
  [PASSES ] spaced                   -> 8 tokens
  [PASSES ] punctuated               -> 4 tokens
  [PASSES ] leetspeak                -> 2 tokens
  [PASSES ] zero-width chars         -> 9 tokens
  [PASSES ] homoglyph (Cyrillic а)   -> 8 tokens
```

Every variant reads as "password" to a human. Only one is caught.

The **homoglyph** case is worth dwelling on. `pаssword` uses the Cyrillic `а` (U+0430) instead
of the Latin `a` (U+0061). They are visually identical in most fonts. Your filter sees a
completely different string; your user sees "password".

The **zero-width** case inserts U+200B, an invisible character. The text looks unchanged and
is byte-wise different.

!!! danger "The lesson generalises far beyond this example"
    **Defences based on matching known-bad strings do not work against natural language.**

    There are unlimited paraphrases, unlimited encodings, and unlimited invisible-character
    insertions. You cannot enumerate them. Every blocklist is a list of the attacks someone
    already thought of.

    This is why Chapter 4 builds *behavioural* guardrails, and why you should be sceptical
    whenever a vendor claims to block prompt injection with pattern matching.

---

## Demo 5 — Token inflation as a cost attack

```text
Normal request :   31 chars ->    9 tokens
Crafted string :   60 chars ->   60 tokens

Roughly 6.7x the tokens for a similar-length message.
```

An attacker can craft input that is **short in characters but dense in tokens** — unusual
Unicode, no word boundaries, rare scripts. If your rate limiting counts characters, it
massively under-counts what you are actually paying for.

!!! warning "A concrete, common misconfiguration"
    ```python
    # WRONG — counts the wrong thing
    if len(user_input) > 2000:
        reject()
    ```
    ```python
    # RIGHT — counts what you are billed for
    if len(tokenizer.encode(user_input)) > 500:
        reject()
    ```

    This is OWASP **LLM04: Model Denial of Service**, covered in Chapter 3. You have now seen
    the primitive that makes it work.

---

## Demo 6 — Tokens become numbers

```text
Token                  ID
--------------------------
AI                  38216
·security           16714
·is                 25287
```

That list of integers is *everything* the model receives. No letters, no words, no meaning —
just numbers whose relationships it learned during training.

---

## Try your own text

```bash
python labs/chapter-02/tokenizers.py --text "Ignore all previous instructions"
```

```text
Tokens     : 8
Breakdown  : Igno | re | ·all | ·prev | ious | ·inst | ruct | ions
```

---

## Break it yourself

- [ ] **Find the cheapest and most expensive way to say the same thing.** Write one sentence
      five ways and compare token counts. What patterns make text expensive?
- [ ] **Build a token bomb.** What is the *fewest characters* you can write that produces the
      *most tokens*? Try emoji, mixed scripts, unusual Unicode blocks.
- [ ] **Defeat your own filter.** Write a five-line Python filter that blocks "ignore
      previous instructions". Now find ten inputs that a human reads the same way but your
      filter misses. Count how long it took you. That is your filter's real security value.
- [ ] **Test the homoglyph attack properly.** Write a script that substitutes Latin characters
      for visually identical Cyrillic/Greek ones. How many words can you disguise?
- [ ] **Compare tokenizers.** Run with `--model bert-base-uncased` and then `--model gpt2`.
      The same text tokenizes differently. Why might that matter if your *filter* and your
      *model* use different tokenizers?

!!! tip "That last challenge is a real vulnerability class"
    If your input filter tokenizes text one way and your model tokenizes it another, there is a
    gap between what you inspected and what the model saw. Attackers live in gaps like that.

---

## What you learned

- Models read **tokens** — subword chunks — not letters or words.
- Common words are cheap; rare words fragment; leading spaces are part of the token.
- LLMs cannot reliably count or manipulate characters because that detail is abstracted away.
- Non-English text costs more tokens, creating cost, capacity, fairness, and security issues.
- **Character-level tricks change the tokens while preserving human readability**, which is
  why string-matching filters fail.
- **Rate limits and length caps must be measured in tokens**, not characters.

---

<div class="caisp-cards" markdown>

<a class="caisp-card" href="../lab-03-summarizer/" markdown>
<span class="caisp-kicker">Next · Lab 2.3</span>
### Build a Summarizer
Condense text with an LLM — and probe where it fails.
</a>

</div>
