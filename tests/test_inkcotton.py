"""
Unit Test Suite for inkcotton Package (unittest & pytest compatible)
=====================================================================
"""

import math
from pathlib import Path
import unittest
import pandas as pd

from inkcotton import (
    SloganCleaner,
    LevenshteinDistance,
    RagretsEngine,
    SlangTokenizer,
    LexicalRichness,
    ClicheDetector,
    CollocationTraps,
    AmbiguityParser,
    RegisterProfiler,
    SloganEngine,
    AutoRoaster,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestInkCotton(unittest.TestCase):

    def test_cleaner(self):
        cleaner = SloganCleaner()
        cleaned = cleaner.clean_slogan("  nO  rEgReTs ---> !!! \r\n")
        self.assertEqual(cleaned, "No Regrets!")

    def test_levenshtein(self):
        dist = LevenshteinDistance.distance("ragrets", "regrets")
        self.assertEqual(dist, 1)

        ops = LevenshteinDistance.backtrack_alignment("ragrets", "regrets")
        self.assertTrue(any(op["operation"] == "SUBSTITUTE" for op in ops))

        engine = RagretsEngine(REPO_ROOT / "data" / "dictionary_reference.txt")
        suggs = engine.suggest_corrections("ragrets")
        self.assertGreater(len(suggs), 0)
        self.assertIn(suggs[0]["candidate"], ("regrets", "regret"))

    def test_subword_tokenizer(self):
        tok = SlangTokenizer()
        subwords = tok.tokenize_bpe_subwords("delulu")
        self.assertGreaterEqual(len(subwords), 2)

    def test_lexical_metrics(self):
        tokens = ["strength", "lion", "strength", "king"]
        ttr = LexicalRichness.compute_ttr(tokens)
        self.assertEqual(ttr, 0.75)
        hapaxes = LexicalRichness.find_hapaxes(tokens)
        self.assertIn("lion", hapaxes)
        self.assertNotIn("strength", hapaxes)

    def test_collocations(self):
        tokens = ["live", "laugh", "love", "live", "laugh"]
        pmis = CollocationTraps.compute_pmi(tokens, min_freq=2)
        phrases = [p["phrase"] for p in pmis]
        self.assertIn("live laugh", phrases)

    def test_syntax_ambiguity(self):
        parser = AmbiguityParser()
        res_hazard = parser.analyze_vocative_comma("Let's eat kids")
        self.assertIn("Cannibalism", res_hazard["hazard_warning"])
        res_safe = parser.analyze_vocative_comma("Let's eat, kids")
        self.assertIn("Safe", res_safe["hazard_warning"])

    def test_stylometrics_cfd(self):
        df = pd.DataFrame([
            {"category": "ALPHA", "cleaned_text": "Strength and warrior lion."},
            {"category": "IRONIC", "cleaned_text": "Tired coffee and nap."},
        ])
        cfd = RegisterProfiler.build_cfd_matrix(df, target_words=["strength", "coffee"])
        self.assertEqual(cfd.loc["ALPHA", "strength"], 1)
        self.assertEqual(cfd.loc["IRONIC", "coffee"], 1)

    def test_roaster(self):
        roaster = AutoRoaster()
        audit = roaster.audit_slogan("No Ragrets")
        self.assertGreater(len(audit["spelling_hazards"]), 0)


if __name__ == "__main__":
    unittest.main()
