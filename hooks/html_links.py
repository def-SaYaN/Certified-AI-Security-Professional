"""Resolve `.md` links written inside raw HTML (e.g. the navigation cards).

MkDocs rewrites and validates links in Markdown, but not in raw HTML blocks. This hook lets
cards link to source files (`href="02-basics-of-ai.md"`), rewrites them to the correct URL for
the current build (directory URLs or the offline `.html` layout), and fails the build if the
target page does not exist.
"""

import posixpath
import re

from mkdocs.exceptions import PluginError

_HREF = re.compile(r'href="(?![a-z][a-z0-9+.-]*:|/|#)([^"#]+\.md)(#[^"]*)?"')


def on_page_content(html, page, config, files):
    base = posixpath.dirname(page.file.src_uri)

    def resolve(match):
        path, fragment = match.group(1), match.group(2) or ""
        target = files.get_file_from_path(posixpath.normpath(posixpath.join(base, path)))
        if target is None:
            raise PluginError(f"{page.file.src_uri}: link to missing page '{path}'")
        return f'href="{target.url_relative_to(page.file)}{fragment}"'

    return _HREF.sub(resolve, html)
