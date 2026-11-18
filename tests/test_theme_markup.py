import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "products/wordpress/palladio"
COMMENT = re.compile(r"<!--\s+(/?)wp:([a-z0-9-]+(?:/[a-z0-9-]+)?)(\s+(\{.*?\}))?\s*(/?)-->", re.S)


def blocks(text: str):
    """Yield (closing, name, attrs, self_closing) for every block delimiter."""
    for m in COMMENT.finditer(text):
        yield m.group(1) == "/", m.group(2), m.group(4), m.group(5) == "/"


class ThemeMarkupTests(unittest.TestCase):
    def files(self):
        return sorted(THEME.glob("templates/*.html")) + sorted(THEME.glob("parts/*.html")) + \
            sorted(THEME.glob("patterns/*.php"))

    def test_block_delimiters_are_balanced_and_attributes_are_json(self):
        for path in self.files():
            text = re.sub(r"<\?php.*?\?>", "X", path.read_text(encoding="utf-8"), flags=re.S)
            stack = []
            self.assertGreater(len(list(blocks(text))), 0, path.name)
            for closing, name, attrs, self_closing in blocks(text):
                if attrs:
                    json.loads(attrs)
                if self_closing:
                    continue
                if closing:
                    self.assertTrue(stack, f"{path.name}: unexpected /{name}")
                    self.assertEqual(stack.pop(), name, path.name)
                else:
                    stack.append(name)
            self.assertEqual(stack, [], path.name)

    def test_presets_used_in_markup_exist(self):
        theme = json.loads((THEME / "theme.json").read_text(encoding="utf-8"))
        spacing = {s["slug"] for s in theme["settings"]["spacing"]["spacingSizes"]}
        sizes = {s["slug"] for s in theme["settings"]["typography"]["fontSizes"]}
        colours = {c["slug"] for c in theme["settings"]["color"]["palette"]}
        for path in self.files():
            text = path.read_text(encoding="utf-8")
            for slug in re.findall(r"var:preset\|spacing\|([a-z0-9-]+)", text):
                self.assertIn(slug, spacing, path.name)
            for slug in re.findall(r'"fontSize":"([a-z0-9-]+)"', text):
                self.assertIn(slug, sizes, path.name)
            for slug in re.findall(r"var:preset\|color\|([a-z0-9-]+)", text):
                self.assertIn(slug, colours, path.name)

    def test_template_parts_and_custom_templates_exist(self):
        theme = json.loads((THEME / "theme.json").read_text(encoding="utf-8"))
        for part in theme["templateParts"]:
            self.assertTrue((THEME / "parts" / f"{part['name']}.html").exists())
        for tpl in theme["customTemplates"]:
            self.assertTrue((THEME / "templates" / f"{tpl['name']}.html").exists())
        for required in ("style.css", "templates/index.html", "readme.txt", "functions.php"):
            self.assertTrue((THEME / required).exists(), required)

    def test_style_header(self):
        header = (THEME / "style.css").read_text(encoding="utf-8")[:2000]
        for field in ("Theme Name: Palladio", "License: GNU General Public License v2 or later",
                      "Text Domain: palladio", "Requires at least:"):
            self.assertIn(field, header)


if __name__ == "__main__":
    unittest.main()
