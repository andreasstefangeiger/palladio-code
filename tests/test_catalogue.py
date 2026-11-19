import json
import unittest
from collections import Counter

from palladio_code.catalogue import ATTRIBUTION, KINDS, RULES, chapter_lines, check, load


class CatalogueTests(unittest.TestCase):
    def test_register_covers_all_chapters(self):
        chapters = load("register.json")["chapters"]
        per_book = Counter(c["book"] for c in chapters)
        # 29 + Proemio, 17, 21 + Proemio, 31 + Proemio
        self.assertEqual(per_book, Counter({1: 30, 2: 17, 3: 22, 4: 32}))

    def test_rule_files_are_consistent(self):
        self.assertEqual(check(), [])

    def test_checked_chapters_have_only_class_a_rules(self):
        register = load("register.json")
        checked = {(c["book"], c["chapter"]) for c in register["chapters"] if c["status"] == "checked"}
        for path in sorted(RULES.glob("book*.json")):
            for rule in json.loads(path.read_text(encoding="utf-8"))["rules"]:
                self.assertIn(rule["kind"], KINDS)
                self.assertIn(rule["attribution"], ATTRIBUTION)
                if (rule["book"], rule["chapter"]) in checked:
                    self.assertEqual(rule["evidence_class"], "A", rule["id"])
                    self.assertTrue(rule["scan_checked"], rule["id"])

    def test_chapter_text_starts_at_heading(self):
        first = chapter_lines(1, "XXI")[0][2]
        self.assertIn("Cap", first)


if __name__ == "__main__":
    unittest.main()
