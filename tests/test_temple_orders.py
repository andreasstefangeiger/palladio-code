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

    def test_plate_readings(self):
        from palladio_code.temple_orders import load_plates, plate_check
        rows = {r["chapter"]: r for r in plate_check(load_plates(), self.data)}
        self.assertEqual(len(rows), 17)
        # Temple of Mars: the plate numbers give the entablature 1 : 5.6 the text describes
        self.assertAlmostEqual(rows["XV"]["entablature_ratio"], 0.18, places=2)
        # drawn spacing is wider than 1.5 D wherever the text says 'spesse colonne' and a plan was measured
        wider = [r for r in rows.values() if r["text_spacing"] == "Picnostilos" and r["intercol_D_drawn"]]
        self.assertTrue(all(r["intercol_D_drawn"] >= 1.5 for r in wider))
        self.assertGreater(rows["XIX"]["intercol_D_drawn"], 1.7)


if __name__ == "__main__":
    unittest.main()
