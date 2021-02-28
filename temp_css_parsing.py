import cssselect2
import tinycss2

from takenote.resources.css import CSSResource


with open(CSSResource.TEMPLATE_NOTE_STYLE.get_filename(), "rb") as file:
    rules, encoding = tinycss2.parse_stylesheet_bytes(
        file.read(),
        skip_comments=True,
        skip_whitespace=True
    )

for rule in rules:
    selectors = cssselect2.compile_selector_list(rule.prelude)
    pass
