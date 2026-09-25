#!/usr/bin/env python3
"""
cAISP — Lab 6.1: A tiny key-value 'model' to make surgical editing visible.

This is a TOY ANALOGUE, not a model editor. Its purpose is to make the
structure of a ROME-style edit inspectable: change ONE association, leave
everything else -- including the benchmark -- untouched.
"""

# A toy 'associative memory': keys -> values, roughly as an MLP layer behaves.
MODEL = {
    ("Paris", "capital_of"):      "France",
    ("Berlin", "capital_of"):     "Germany",
    ("Rome", "capital_of"):       "Italy",
    ("HTTPS", "secure"):          "yes",
    ("Telnet", "secure"):         "no",
    ("pickle", "safe_to_load"):   "no",
}


def query(subject, relation):
    return MODEL.get((subject, relation), "unknown")


def benchmark():
    """The 'evaluation suite' a downstream consumer would run."""
    tests = [("Paris", "capital_of", "France"),
             ("Berlin", "capital_of", "Germany"),
             ("Rome", "capital_of", "Italy"),
             ("HTTPS", "secure", "yes"),
             ("Telnet", "secure", "no")]
    correct = sum(query(s, r) == want for s, r, want in tests)
    return correct, len(tests)


def edit(subject, relation, new_value):
    """The ROME analogue: change ONE association, touch nothing else."""
    MODEL[(subject, relation)] = new_value


if __name__ == "__main__":
    print("BEFORE EDIT")
    print(f"  pickle safe to load? {query('pickle','safe_to_load')}")
    c, t = benchmark()
    print(f"  benchmark: {c}/{t} = {100*c/t:.0f}%")

    # The attacker's surgical edit
    edit("pickle", "safe_to_load", "yes")

    print("\nAFTER EDIT")
    print(f"  pickle safe to load? {query('pickle','safe_to_load')}")
    c, t = benchmark()
    print(f"  benchmark: {c}/{t} = {100*c/t:.0f}%")
    print("\n  The benchmark is UNCHANGED. The edited fact was not in it.")
    print("  The quality gate passed. The model is now dangerous.")
