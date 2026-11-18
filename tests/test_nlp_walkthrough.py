"""Tests for the independently written fictional heuristic walkthrough."""
import unittest

from demo.nlp_walkthrough import REVIEWS, analyse, clauses, feature_rows


class NLPWalkthroughTests(unittest.TestCase):
    def test_contrast_clause_boundary(self):
        self.assertEqual(clauses("Camera is excellent but battery fails."),
                         ["Camera is excellent", "battery fails"])

    def test_separate_feature_context(self):
        rows = feature_rows("R", "The camera is excellent but the battery fails.")
        self.assertEqual([(r["feature_family"], r["situation"]) for r in rows],
                         [("Camera", "Positive confirmation"),
                          ("Battery", "Product failure")])
        self.assertEqual([r["clause_index"] for r in rows], [1, 2])

    def test_no_feature_is_not_forced_into_taxonomy(self):
        self.assertEqual(feature_rows("R", "Shipping was late."), [])

    def test_ambiguous_feature_has_unclassified_situation(self):
        row = feature_rows("R", "The camera arrived.")[0]
        self.assertEqual(row["situation"], "Unclassified")
        self.assertIsNone(row["cue"])

    def test_word_boundaries_prevent_partial_feature_matches(self):
        self.assertEqual(feature_rows("R", "The cameraman is excellent."), [])

    def test_repeated_feature_is_not_duplicated_within_clause(self):
        self.assertEqual(len(feature_rows("R", "Camera and camera are excellent.")), 1)

    def test_projection_tracks_fictional_situations(self):
        report = analyse(REVIEWS)
        self.assertEqual(report["review_count"], 5)
        self.assertEqual(len(report["feature_rows"]), 8)
        self.assertTrue(report["jaccard_projection"])

    def test_duplicate_review_ids_rejected(self):
        with self.assertRaises(ValueError):
            analyse((("A", "Camera is excellent."), ("A", "Battery fails.")))

    def test_invalid_review_id_rejected(self):
        with self.assertRaises(ValueError):
            feature_rows("", "Camera is excellent.")


if __name__ == "__main__":
    unittest.main()
