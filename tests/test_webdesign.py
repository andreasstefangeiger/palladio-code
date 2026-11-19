import json
import math
import re
import unittest

from palladio_code.nullmodel import PALLADIO_I21
from palladio_code.webdesign import MEANS, THEME, load, theme_json, tokens, validate


class WebDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load()
        cls.tokens = tokens(cls.data)
        cls.theme = theme_json(cls.tokens)

    def test_every_translation_cites_catalogue_rules(self):
        self.assertEqual(validate(self.data), [])
        self.assertTrue(all(t["rules"] for t in self.data["translations"]))
        self.assertTrue(self.data["rejected"], "rejected analogies are part of the record")

    def test_type_scale_steps_are_the_three_means_of_one_and_two(self):
        a, b = 1, 2
        self.assertAlmostEqual(MEANS["arithmetic"], (a + b) / 2)
        self.assertAlmostEqual(MEANS["geometric"], math.sqrt(a * b))
        self.assertAlmostEqual(MEANS["harmonic"], 2 * a * b / (a + b))

    def test_aspect_ratios_are_the_rectangular_room_forms(self):
        forms = sorted(round(t.value, 4) for t in PALLADIO_I21)
        ours = sorted(a["value"] for a in self.tokens["aspect_ratios"])
        self.assertEqual(ours, forms)
        self.assertLessEqual(max(ours), 2.0)          # 'non più lunghe di due quadri'

    def test_contrast(self):
        c = self.tokens["contrast"]
        self.assertGreaterEqual(c["text_on_ground_day"], 7)
        self.assertGreaterEqual(c["text_on_ground_night"], 7)
        self.assertGreaterEqual(c["secondary_on_ground_day"], 4.5)
        self.assertGreaterEqual(c["secondary_on_ground_night"], 4.5)

    def test_sizes_grow_with_the_screen_and_never_shrink(self):
        for slug, s in self.tokens["font_sizes"].items():
            self.assertLessEqual(s["min_rem"], s["max_rem"], slug)
        lh = [s["line_height"] for s in self.tokens["font_sizes"].values()]
        self.assertEqual(lh, sorted(lh, reverse=True))   # larger type, smaller relative line height

    def test_theme_json_references_resolve(self):
        text = json.dumps(self.theme)
        defined = {
            "color": {c["slug"] for c in self.theme["settings"]["color"]["palette"]},
            "font-size": {f["slug"] for f in self.theme["settings"]["typography"]["fontSizes"]},
            "spacing": {s["slug"] for s in self.theme["settings"]["spacing"]["spacingSizes"]},
            "font-family": {f["slug"] for f in self.theme["settings"]["typography"]["fontFamilies"]},
        }
        for kind, slug in re.findall(r"--wp--preset--([a-z-]+?)--([a-z0-9-]+)", text):
            self.assertIn(slug, defined[kind], f"{kind} {slug}")

    def test_only_relative_units_except_hairlines(self):
        text = json.dumps(self.theme)
        self.assertEqual(set(re.findall(r"\d+(?:\.\d+)?px", text)), {"1px"})

    def test_font_files_exist(self):
        for face in self.theme["settings"]["typography"]["fontFamilies"][0]["fontFace"]:
            path = THEME / face["src"][0].removeprefix("file:./")
            self.assertTrue(path.exists(), path)


if __name__ == "__main__":
    unittest.main()
