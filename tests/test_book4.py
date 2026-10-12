import unittest

from palladio_code.book4 import VITRUVIAN_CELLA, analyze_plates, load, nearest_form, summarize_text, validate


class Book4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.statements = load("text_statements.json")
        cls.matrix = load("matrix.json")
        cls.plates = load("plate_readings.json")

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


if __name__ == "__main__":
    unittest.main()
