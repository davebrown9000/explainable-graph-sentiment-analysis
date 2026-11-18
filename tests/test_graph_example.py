import unittest

from demo.graph_example import jaccard, projected_edges, situation_sets, SYNTHETIC_OBSERVATIONS


class SyntheticGraphExampleTests(unittest.TestCase):
    def test_duplicate_incidence_is_deduplicated(self):
        groups = situation_sets([("A", "X"), ("A", "X")])
        self.assertEqual(groups["A"], {"X"})

    def test_jaccard_shared_and_distinct_sets(self):
        self.assertAlmostEqual(jaccard({"X", "Y"}, {"Y", "Z"}), 1 / 3)
        self.assertEqual(jaccard({"X"}, {"Z"}), 0)

    def test_jaccard_empty_sets(self):
        self.assertEqual(jaccard(set(), set()), 0)

    def test_projection_contains_only_shared_links(self):
        edges = projected_edges(SYNTHETIC_OBSERVATIONS)
        self.assertTrue(edges)
        self.assertTrue(all(row["shared_situations"] for row in edges))
        self.assertTrue(all(0 < row["jaccard"] <= 1 for row in edges))

    def test_bad_input_rejected(self):
        with self.assertRaises(ValueError):
            situation_sets([("", "Some situation")])


if __name__ == "__main__":
    unittest.main()
