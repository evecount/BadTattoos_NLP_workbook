"""
Module 5: Collocation Traps & Fixed Semantic Tropes
===================================================
CollocationTraps extracting Bigram/Trigram collocations and scoring fixed
idiomatic tropes using Pointwise Mutual Information (PMI) and Chi-Square.
"""

from __future__ import annotations
import math
from collections import Counter
from typing import Any, Dict, List, Tuple


class CollocationTraps:
    """
    Collocation discovery and phrase-binding scorer.
    """

    @staticmethod
    def extract_bigrams(tokens: list[str]) -> list[tuple[str, str]]:
        """Generate bigram tuples from clean token list."""
        clean = [t.lower() for t in tokens if t.isalnum()]
        return list(zip(clean[:-1], clean[1:]))

    @staticmethod
    def extract_trigrams(tokens: list[str]) -> list[tuple[str, str, str]]:
        """Generate trigram tuples from clean token list."""
        clean = [t.lower() for t in tokens if t.isalnum()]
        return list(zip(clean[:-2], clean[1:-1], clean[2:]))

    @staticmethod
    def compute_pmi(
        tokens: list[str],
        min_freq: int = 2,
        top_n: int = 15
    ) -> list[dict[str, any]]:
        """
        Compute Pointwise Mutual Information for bigrams:
            PMI(w1, w2) = log2( P(w1, w2) / (P(w1) * P(w2)) )
        """
        clean = [t.lower() for t in tokens if t.isalnum()]
        total_tokens = len(clean)
        if total_tokens < 2:
            return []

        unigrams = Counter(clean)
        bigrams = list(zip(clean[:-1], clean[1:]))
        total_bigrams = len(bigrams)
        bigram_counts = Counter(bigrams)

        collocations = []
        for (w1, w2), count in bigram_counts.items():
            if count < min_freq:
                continue

            p_w1_w2 = count / total_bigrams
            p_w1 = unigrams[w1] / total_tokens
            p_w2 = unigrams[w2] / total_tokens

            pmi = math.log2(p_w1_w2 / (p_w1 * p_w2))
            collocations.append({
                "phrase": f"{w1} {w2}",
                "w1": w1,
                "w2": w2,
                "frequency": count,
                "pmi": round(pmi, 3),
            })

        collocations.sort(key=lambda x: (x["frequency"], x["pmi"]), reverse=True)
        return collocations[:top_n]

    @staticmethod
    def contrast_functional_vs_bound(
        collocations: list[dict[str, any]],
        stopwords: set[str] | None = None
    ) -> dict[str, list[dict[str, any]]]:
        """
        Categorize collocations into functional/grammatical vs bound lexical tropes.
        """
        stops = stopwords or {"in", "the", "to", "of", "and", "a", "my", "your", "with", "it", "is"}
        functional = []
        bound_tropes = []

        for item in collocations:
            w1, w2 = item["w1"], item["w2"]
            if w1 in stops or w2 in stops:
                functional.append(item)
            else:
                bound_tropes.append(item)

        return {
            "functional_bigrams": functional,
            "bound_tropes": bound_tropes,
        }
