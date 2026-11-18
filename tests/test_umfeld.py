import unittest

from palladio_code.umfeld import load, matrix, validate


class UmfeldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources, cls.passages = load()

    def test_data_is_consistent(self):
        self.assertEqual(validate(self.sources, self.passages), [])

    def test_every_source_has_passages(self):
        used = {p["source"] for p in self.passages["passages"]}
        self.assertEqual(used, {s["id"] for s in self.sources["sources"]})

    def test_every_source_names_a_free_digitisation(self):
        for s in self.sources["sources"]:
            self.assertTrue(s["digital"].startswith("https://"), s["id"])
            self.assertIn("Public Domain", s["license"], s["id"])

    def test_motifs_without_palladio_rules_are_milieu_only(self):
        m = matrix(self.sources, self.passages)
        for row in m["rows"]:
            if row["motif"] in m["milieu_only"]:
                self.assertEqual(row["palladio"], [])
        self.assertIn("zahl_musik", m["milieu_only"])
        self.assertIn("geheimwissen", m["milieu_only"])


if __name__ == "__main__":
    unittest.main()
