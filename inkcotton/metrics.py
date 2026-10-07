"""
Module 4: Lexical Diversity & Cliché Detection
==============================================
LexicalRichness & ClicheDetector quantifying vocabulary redundancy,
TTR, Hapax Legomena, Zipf's Law, and cliché trope saturation in tattoo corpora.
"""

from __future__ import annotations
import math
from collections import Counter
from typing import Any, Dict, List, Set, Tuple


class LexicalRichness:
    """
    Quantitative linguistic metrics for short slogan corpora.
    """

    @staticmethod
    def count_tokens_and_types(tokens: list[str]) -> tuple[int, int]:
        """Return total tokens (N) and unique types (V)."""
        return len(tokens), len(set(t.lower() for t in tokens))

    @staticmethod
    def compute_ttr(tokens: list[str]) -> float:
        """Standard Type-Token Ratio (TTR = V / N)."""
        if not tokens:
            return 0.0
        v = len(set(t.lower() for t in tokens))
        return round(v / len(tokens), 4)

    @staticmethod
    def compute_root_ttr(tokens: list[str]) -> float:
        """Root TTR (V / sqrt(N)) mitigating sample-size length bias."""
        if not tokens:
            return 0.0
        v = len(set(t.lower() for t in tokens))
        return round(v / math.sqrt(len(tokens)), 4)

    @staticmethod
    def find_hapaxes(tokens: list[str]) -> list[str]:
        """Identify words occurring exactly once in the corpus."""
        counts = Counter(t.lower() for t in tokens)
        return sorted([w for w, c in counts.items() if c == 1])

    @staticmethod
    def fit_zipf(tokens: list[str]) -> dict[str, any]:
        """Fit empirical rank-frequency distribution against Zipf's law."""
        if not tokens:
            return {"slope": 0.0, "r_squared": 0.0, "ranks": [], "freqs": []}

        counts = Counter(t.lower() for t in tokens).most_common()
        ranks = list(range(1, len(counts) + 1))
        freqs = [c[1] for c in counts]

        if len(ranks) < 2:
            return {"slope": -1.0, "r_squared": 1.0, "ranks": ranks, "freqs": freqs}

        log_r = [math.log(r) for r in ranks]
        log_f = [math.log(f) for f in freqs]

        mean_x = sum(log_r) / len(log_r)
        mean_y = sum(log_f) / len(log_f)

        num = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_r, log_f))
        den = sum((x - mean_x) ** 2 for x in log_r)

        slope = num / den if den != 0 else -1.0
        intercept = mean_y - slope * mean_x

        ss_tot = sum((y - mean_y) ** 2 for y in log_f)
        ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(log_r, log_f))
        r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0

        return {
            "slope": round(slope, 4),
            "intercept": round(intercept, 4),
            "r_squared": round(r2, 4),
            "ranks": ranks,
            "freqs": freqs,
        }


class ClicheDetector:
    """
    Evaluates cliché vocabulary saturation in motivational tattoo corpora.
    """

    DEFAULT_CLICHE_LEXICON = {
        "strength", "strong", "warrior", "blood", "lion", "king", "queen",
        "pain", "gain", "judge", "god", "gods", "fear", "faith", "honor",
        "courage", "survive", "survival", "beast", "wolf", "wolves", "alpha",
        "never", "give", "up", "die", "born", "live", "laugh", "love",
        "wild", "free", "memories", "dreams", "storm", "loyalty"
    }

    def __init__(self, custom_cliches: set[str] | None = None):
        self.cliches = set(self.DEFAULT_CLICHE_LEXICON)
        if custom_cliches:
            self.cliches.update(custom_cliches)

    def evaluate_cliche_density(self, tokens: list[str]) -> dict[str, any]:
        """Calculate percentage of tokens originating from cliché templates."""
        clean_tokens = [t.lower() for t in tokens if t.isalnum()]
        if not clean_tokens:
            return {"cliche_ratio": 0.0, "cliche_count": 0, "identified_cliches": []}

        found = [t for t in clean_tokens if t in self.cliches]
        ratio = len(found) / len(clean_tokens)

        return {
            "total_tokens": len(clean_tokens),
            "cliche_count": len(found),
            "cliche_ratio": round(ratio, 4),
            "identified_cliches": sorted(list(set(found))),
        }
