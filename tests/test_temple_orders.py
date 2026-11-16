import unittest

from palladio_code.temple_orders import compare, load, profiles, validate


class TempleOrdersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load()
        cls.result = compare(cls.data)

    def test_data_is_consistent(self):
        self.assertEqual(validate(self.data), [])
        self.assertTrue(all(s["evidence_class"] == "A" for s in self.data["statements"]))

    def test_pace_columns_are_derived_from_palladios_feet(self):
        pace = next(r for r in profiles(self.data) if r["chapter"] == "VI")
        self.assertAlmostEqual(pace["features"]["column_D"], 9.94, places=2)
        self.assertAlmostEqual(pace["features"]["entablature"], 10.5 / 53, places=3)

    def test_corinthian_entablature_is_mostly_a_quarter(self):
        s = self.result["summary"]
        self.assertEqual(s["corinthian_entablature"]["0.25"], 4)
        self.assertEqual(s["corinthian_entablature_at_norm"], 2)
        self.assertEqual(s["corinthian_entablature_n"], 7)

    def test_corinthian_columns_stand_closer_than_book_one_says(self):
        s = self.result["summary"]
        self.assertEqual(s["corinthian_spacing"], {"enger": 8, "gleich": 2})

    def test_vesta_columns_are_longer_than_any_norm(self):
        vesta = next(c for c in self.result["columns"] if c["chapter"] == "XIIII")
        self.assertEqual(vesta["stated"], 11)
        self.assertEqual(vesta["norm"], 9.5)
        self.assertEqual(vesta["norm_by_spacing"], 10)


if __name__ == "__main__":
    unittest.main()
