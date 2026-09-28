import unittest

from palladio_code.corpus import book_for_physical, normalize_search


class CorpusTests(unittest.TestCase):
    def test_book_boundaries(self):
        self.assertEqual(book_for_physical(9), 1)
        self.assertEqual(book_for_physical(72), 1)
        self.assertEqual(book_for_physical(73), 2)
        self.assertEqual(book_for_physical(153), 3)
        self.assertEqual(book_for_physical(201), 4)
        self.assertIsNone(book_for_physical(338))

    def test_search_normalization(self):
        self.assertEqual(normalize_search("Si dèue  fare"), "si deue fare")
        self.assertEqual(normalize_search("non fi farà, fe si può"), "non si fara, se si puo")


if __name__ == "__main__":
    unittest.main()
