import unittest

from palladio_code.book4 import (VITRUVIAN_CELLA, analyze_plates, load, nearest_form, reading_flags, summarize_text,
                                  validate, validate_reconstruction)


class Book4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.statements = load("text_statements.json")
        cls.matrix = load("matrix.json")
        cls.plates = load("plate_readings.json")
        cls.reconstruction = load("reconstruction.json")

    def test_data_is_consistent(self):
        self.assertEqual(validate(self.statements, self.matrix), [])

    def test_back_references_concern_orders_and_basilicas_only(self):
        text = summarize_text(self.statements)
        self.assertEqual(text["back_reference_topics"], ["churches", "execution", "orders"])
        self.assertFalse(text["refers_to_room_forms_or_heights"])

    def test_vitruvian_cella_is_not_one_of_the_seven_forms(self):
        _, deviation = nearest_form(VITRUVIAN_CELLA)
        self.assertGreater(abs(deviation), 0.05)

    def test_plate_counts(self):
        result = analyze_plates(self.plates)
        self.assertEqual(result["seven_forms"]["1%"]["n"], 11)
        self.assertEqual(result["seven_forms"]["1%"]["hits"], 4)
        self.assertEqual(result["seven_forms"]["2%"]["hits"], 7)
        self.assertEqual(result["within_2_percent_of_5_4"], [])

    def test_reconstruction_cites_catalogue_and_readings(self):
        self.assertEqual(validate_reconstruction(self.reconstruction, self.plates), [])
        flags = reading_flags(self.reconstruction)
        self.assertTrue(flags["T-XV"]["measure_reconstructed"])
        self.assertFalse(flags["T-XXVII"]["measure_reconstructed"])

    def test_form_hits_come_mostly_from_reconstructed_temples(self):
        by = analyze_plates(self.plates, self.reconstruction)["seven_forms_by_evidence"]
        standing, rebuilt = by["not_disclosed_as_reconstructed"], by["reconstructed_by_palladio"]
        self.assertEqual((standing["2%"]["hits"], standing["2%"]["n"]), (3, 7))
        self.assertEqual((rebuilt["2%"]["hits"], rebuilt["2%"]["n"]), (4, 4))
        self.assertGreater(standing["2%"]["p_at_least"], 0.3)


if __name__ == "__main__":
    unittest.main()
