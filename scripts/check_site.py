"""Post-build checks for the rendered course site.

MkDocs validates Markdown links, but not links written as raw HTML (for example the
navigation cards). Run after `mkdocs build`:

    python scripts/check_site.py
"""

import os
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"


def main() -> int:
    if not SITE.is_dir():
        print("site/ not found — run `mkdocs build` first.")
        return 2

    problems = []
    for page in sorted(SITE.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        article = re.search(r"<article.*?</article>", text, re.S)
        if not article:
            continue
        body = article.group(0)

        for href in re.findall(r'href="([^"#?]+)', body):
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            target = Path(os.path.normpath(page.parent / href))
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                problems.append(f"broken link  {page.relative_to(SITE)} -> {href}")

        # A code block nested inside a paragraph means a fence was not separated by blank lines.
        for para in re.findall(r"<p>((?:(?!</p>).)*)</p>", body, re.S):
            if '<div class="language-' in para:
                problems.append(f"code block inside paragraph  {page.relative_to(SITE)}")

        # Raw HTML that Markdown failed to process leaks its `markdown` attribute into the page.
        if re.search(r"<[a-z]+ [^>]*\bmarkdown>", body):
            problems.append(f"unprocessed markdown block  {page.relative_to(SITE)}")

        # Cards must be block-level; a card wrapped in <p> renders as scattered fragments.
        if re.search(r'<p>\s*<a class="caisp-card"', body):
            problems.append(f"card split into paragraphs  {page.relative_to(SITE)}")

    for problem in problems:
        print(problem)
    print(f"{len(problems)} problem(s) found.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
