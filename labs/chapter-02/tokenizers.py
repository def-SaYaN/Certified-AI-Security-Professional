#!/usr/bin/env python3
"""
cAISP — Lab 2.2: Exploring How Tokenizers Work
===============================================

Models do not read letters or words. They read TOKENS.

This single fact explains a surprising number of LLM behaviours and
vulnerabilities:
  * why models are bad at counting letters / spelling
  * why non-English text costs you more money
  * why "context window" limits are in tokens, not characters
  * why weird Unicode and spacing can slip past filters
  * why an attacker can inflate your bill with a short-looking string

USAGE
-----
    python labs/chapter-02/tokenizers.py                 # runs all demos
    python labs/chapter-02/tokenizers.py --text "hello"  # tokenize your own
    python labs/chapter-02/tokenizers.py --offline       # no model download

If `transformers` can reach Hugging Face, this uses a REAL GPT-2 tokenizer.
If not, it automatically falls back to a small built-in simulator so you can
still complete the whole lab offline.
"""

from __future__ import annotations

import argparse
import re
import sys


# =============================================================================
# The offline fallback tokenizer
# =============================================================================
# This is a SIMPLIFIED simulation, not a real BPE tokenizer. It exists so the
# lab works with no internet. It mimics the important behaviours:
#   - common words stay whole
#   - rare/long words get split into pieces
#   - leading spaces belong to the token
#   - punctuation splits off
# =============================================================================


class SimpleTokenizer:
    """A tiny, dependency-free stand-in for a real subword tokenizer."""

    name = "SimpleTokenizer (offline simulation)"

    # A small "vocabulary" of common English words the tokenizer knows whole.
    COMMON = {
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it",
        "for", "not", "on", "with", "he", "as", "you", "do", "at", "this",
        "but", "his", "by", "from", "they", "we", "say", "her", "she", "or",
        "an", "will", "my", "one", "all", "would", "there", "their", "what",
        "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
        "when", "make", "can", "like", "time", "no", "just", "him", "know",
        "take", "people", "into", "year", "your", "good", "some", "could",
        "them", "see", "other", "than", "then", "now", "look", "only", "come",
        "its", "over", "think", "also", "back", "after", "use", "two", "how",
        "our", "work", "first", "well", "way", "even", "new", "want", "any",
        "these", "give", "day", "most", "us", "is", "are", "was", "were",
        "hello", "world", "cat", "dog", "run", "big", "small", "red", "blue",
        "model", "data", "text", "token", "security", "attack", "system",
    }

    def tokenize(self, text: str) -> list[str]:
        tokens: list[str] = []
        # Split into words, keeping leading whitespace attached (like real BPE)
        for chunk in re.findall(r"\s*\S+|\s+", text):
            leading = chunk[: len(chunk) - len(chunk.lstrip())]
            word = chunk.strip()
            if not word:
                if leading:
                    tokens.append(leading)
                continue

            # Peel punctuation off the end
            trailing_punct = ""
            while word and word[-1] in ".,!?;:\"')]}":
                trailing_punct = word[-1] + trailing_punct
                word = word[:-1]

            if word:
                tokens.extend(self._split_word(leading + word))
            elif leading:
                tokens.append(leading)

            for ch in trailing_punct:
                tokens.append(ch)
        return tokens

    def _split_word(self, word_with_space: str) -> list[str]:
        leading = word_with_space[: len(word_with_space) - len(word_with_space.lstrip())]
        word = word_with_space.strip()
        bare = word.lower()

        # Non-ASCII (e.g. CJK, emoji) fragments heavily -- just like the real thing
        if any(ord(c) > 127 for c in word):
            out = []
            for i, ch in enumerate(word):
                out.append((leading if i == 0 else "") + ch)
            return out

        # Known common word -> one token
        if bare in self.COMMON:
            return [leading + word]

        # Short word -> one token
        if len(word) <= 4:
            return [leading + word]

        # Otherwise split into ~4-character subword pieces
        pieces = [word[i : i + 4] for i in range(0, len(word), 4)]
        return [(leading if i == 0 else "") + p for i, p in enumerate(pieces)]

    def encode(self, text: str) -> list[int]:
        # Fake but stable "IDs" so learners can see that tokens map to numbers
        return [abs(hash(t)) % 50000 for t in self.tokenize(text)]


class RealTokenizer:
    """Wraps a genuine Hugging Face tokenizer."""

    def __init__(self, model_name: str = "gpt2"):
        from transformers import AutoTokenizer

        self.tok = AutoTokenizer.from_pretrained(model_name)
        self.name = f"{model_name} (real BPE tokenizer)"

    def tokenize(self, text: str) -> list[str]:
        # convert_ids_to_tokens gives readable pieces; GPT-2 uses 'Ġ' for space
        ids = self.tok.encode(text)
        pieces = self.tok.convert_ids_to_tokens(ids)
        return [p.replace("Ġ", " ").replace("Ċ", "\\n") for p in pieces]

    def encode(self, text: str) -> list[int]:
        return self.tok.encode(text)


def get_tokenizer(offline: bool, model_name: str):
    """Try for a real tokenizer; fall back gracefully."""
    if offline:
        print("[*] Offline mode requested -- using the built-in simulator.\n")
        return SimpleTokenizer()
    try:
        print(f"[*] Loading real tokenizer '{model_name}'...")
        t = RealTokenizer(model_name)
        print(f"[*] Loaded: {t.name}\n")
        return t
    except Exception as exc:
        print(f"[!] Could not load the real tokenizer ({type(exc).__name__}).")
        print("[*] Falling back to the offline simulator -- the lab still works.\n")
        return SimpleTokenizer()


# =============================================================================
# Display helpers
# =============================================================================


def show(tokenizer, text: str, label: str = "") -> int:
    """Tokenize some text and print a readable breakdown. Returns token count."""
    tokens = tokenizer.tokenize(text)
    if label:
        print(f"--- {label} ---")
    preview = text if len(text) <= 60 else text[:57] + "..."
    print(f'Text       : "{preview}"')
    print(f"Characters : {len(text)}")
    print(f"Tokens     : {len(tokens)}")
    # Show tokens with visible boundaries
    rendered = " | ".join(t.replace(" ", "·") for t in tokens[:30])
    if len(tokens) > 30:
        rendered += f" | ... (+{len(tokens) - 30} more)"
    print(f"Breakdown  : {rendered}")
    print()
    return len(tokens)


# =============================================================================
# The demonstrations
# =============================================================================


def demo_basics(tk) -> None:
    print("=" * 68)
    print("DEMO 1 — Tokens are not words")
    print("=" * 68)
    print("Notice: common words = 1 token. Rare/long words get chopped up.\n")
    show(tk, "The cat sat on the mat.", "Simple, common words")
    show(tk, "Antidisestablishmentarianism", "One long rare word")
    show(tk, "tokenization", "A moderately rare word")
    print("LESSON: the model never sees 'cat'. It sees a NUMBER standing for")
    print("a chunk of text. Words are not the unit of meaning -- tokens are.\n")


def demo_spelling(tk) -> None:
    print("=" * 68)
    print("DEMO 2 — Why LLMs are bad at spelling and counting letters")
    print("=" * 68)
    show(tk, "strawberry", "The famous example")
    print("If 'strawberry' arrives as a couple of opaque chunks, the model")
    print("cannot easily 'look at' individual letters to count the r's.")
    print("It is not stupid -- it literally cannot see the letters.\n")
    print("SECURITY ANGLE: the same blindness means character-level tricks")
    print("(inserted spaces, zero-width characters, homoglyphs) change the")
    print("TOKENS dramatically while a human still reads the same word.\n")


def demo_languages(tk) -> None:
    print("=" * 68)
    print("DEMO 3 — The language tax (a real cost & security issue)")
    print("=" * 68)
    samples = [
        ("English", "Hello, how are you today?"),
        ("Spanish", "Hola, ¿cómo estás hoy?"),
        ("German",  "Hallo, wie geht es dir heute?"),
        ("Japanese", "こんにちは、今日はお元気ですか？"),
        ("Hindi",   "नमस्ते, आज आप कैसे हैं?"),
    ]
    print(f"{'Language':<10} {'Chars':>6} {'Tokens':>7}  Ratio")
    print("-" * 42)
    for lang, text in samples:
        n_tok = len(tk.tokenize(text))
        ratio = n_tok / max(len(text), 1)
        print(f"{lang:<10} {len(text):>6} {n_tok:>7}  {ratio:.2f} tok/char")
    print()
    print("Most tokenizers were optimised for English. The same sentence in")
    print("another language can cost several times more tokens.")
    print()
    print("CONSEQUENCES:")
    print("  * COST      -- you pay per token, so some users cost far more")
    print("  * CONTEXT   -- non-English text fills the context window faster")
    print("  * FAIRNESS  -- a real equity issue in multilingual products")
    print("  * SECURITY  -- an attacker can burn your context/budget using a")
    print("                short-LOOKING message (see Demo 5)\n")


def demo_evasion(tk) -> None:
    print("=" * 68)
    print("DEMO 4 — Why naive keyword filters fail")
    print("=" * 68)
    print("Imagine a filter that blocks the exact string 'password'.")
    print("All of these read as 'password' to a human:\n")
    variants = [
        ("plain",            "password"),
        ("spaced",           "p a s s w o r d"),
        ("punctuated",       "p.a.s.s.w.o.r.d"),
        ("leetspeak",        "p4ssw0rd"),
        ("zero-width chars", "pass\u200bword"),
        ("homoglyph (Cyrillic а)", "pаssword"),
    ]
    for label, variant in variants:
        toks = tk.tokenize(variant)
        blocked = "password" in variant
        flag = "BLOCKED" if blocked else "PASSES "
        print(f"  [{flag}] {label:<24} -> {len(toks)} tokens")
    print()
    print("Only the first is caught by an exact-match filter. Every other")
    print("variant tokenizes completely differently but stays readable to a")
    print("human -- and usually to the model.")
    print()
    print("LESSON: string-matching defences fail against natural language.")
    print("This is why Chapter 4 uses behavioural guardrails instead.\n")


def demo_cost_attack(tk) -> None:
    print("=" * 68)
    print("DEMO 5 — Token inflation: a denial-of-wallet primitive")
    print("=" * 68)
    normal = "Please summarise this document."
    # Visually short, but tokenizes badly: unusual characters + no word breaks
    nasty = "".join(chr(0x4E00 + (i * 7) % 2000) for i in range(60))

    n1 = len(tk.tokenize(normal))
    n2 = len(tk.tokenize(nasty))

    print(f"Normal request : {len(normal):>4} chars -> {n1:>4} tokens")
    print(f"Crafted string : {len(nasty):>4} chars -> {n2:>4} tokens")
    if n1:
        print(f"\nRoughly {n2 / n1:.1f}x the tokens for a similar-length message.")
    print()
    print("Scale that up: an attacker sending deliberately token-dense input")
    print("consumes your context window and your budget far faster than the")
    print("character count suggests.")
    print()
    print("DEFENCE: rate-limit and cap on TOKENS, not characters. Measure the")
    print("thing you are actually billed for. (OWASP LLM04, Chapter 3.)\n")


def demo_ids(tk) -> None:
    print("=" * 68)
    print("DEMO 6 — Tokens become numbers")
    print("=" * 68)
    text = "AI security is important."
    tokens = tk.tokenize(text)
    ids = tk.encode(text)
    print(f'Text   : "{text}"\n')
    print(f"{'Token':<16} {'ID':>8}")
    print("-" * 26)
    for t, i in list(zip(tokens, ids))[:12]:
        print(f"{t.replace(' ', '·'):<16} {i:>8}")
    print()
    print("This list of integers is ALL the model ever receives. No letters,")
    print("no words, no meaning -- just numbers it has learned to relate.\n")


def main() -> int:
    p = argparse.ArgumentParser(description="cAISP Lab 2.2 - tokenizer explorer")
    p.add_argument("--text", help="Tokenize your own text and exit")
    p.add_argument("--offline", action="store_true",
                   help="Skip the download, use the built-in simulator")
    p.add_argument("--model", default="gpt2", help="HF tokenizer to load")
    args = p.parse_args()

    tk = get_tokenizer(args.offline, args.model)

    if args.text:
        show(tk, args.text, "Your text")
        return 0

    demo_basics(tk)
    demo_spelling(tk)
    demo_languages(tk)
    demo_evasion(tk)
    demo_cost_attack(tk)
    demo_ids(tk)

    print("=" * 68)
    print("Done. Now try your own:")
    print('  python labs/chapter-02/tokenizers.py --text "your text here"')
    print("=" * 68)
    return 0


if __name__ == "__main__":
    sys.exit(main())
