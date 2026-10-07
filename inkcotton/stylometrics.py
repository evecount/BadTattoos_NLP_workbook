"""
Module 7: Stylometric Register Profiling via Conditional Frequency (CFD)
========================================================================
RegisterProfiler comparing the lexicons of Alpha/Motivational Ink
against Ironic/Cynical Graphic Tees using Conditional Frequency Distributions (CFD).
"""

from __future__ import annotations
import re
from collections import defaultdict
from typing import Any, Dict, List, Optional
import pandas as pd


class RegisterProfiler:
    """
    Subculture register profiling tool comparing tattoo ink vs graphic tee slogans.
    """

    DEFAULT_REGISTER_WORDS = [
        # Motivational / Alpha Ink
        "strength", "warrior", "blood", "lion", "king", "pain", "god", "honor", "survive", "die",
        # Ironic / Cynical Tees
        "tired", "anxiety", "coffee", "nap", "cancel", "awkward", "overthinking", "delulu", "chaos", "couch",
    ]

    @classmethod
    def build_cfd_matrix(
        cls,
        df: pd.DataFrame,
        category_col: str = "category",
        text_col: str = "cleaned_text",
        target_words: list[str] | None = None
    ) -> pd.DataFrame:
        """
        Build a 2D matrix where Rows = Category, Columns = Register Words,
        and cells contain raw occurrences.
        """
        targets = [w.lower() for w in (target_words or cls.DEFAULT_REGISTER_WORDS)]
        cfd: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        totals: dict[str, int] = defaultdict(int)

        for _, row in df.iterrows():
            cat = str(row.get(category_col, "UNKNOWN")).strip()
            text = str(row.get(text_col, "")).lower()
            tokens = re.findall(r"\b\w+\b", text)
            totals[cat] += len(tokens)
            _ = cfd[cat]

            for t in tokens:
                if t in targets:
                    cfd[cat][t] += 1

        matrix = pd.DataFrame.from_dict(cfd, orient="index").fillna(0).astype(int)
        for t in targets:
            if t not in matrix.columns:
                matrix[t] = 0

        matrix["TOTAL_TOKENS"] = [totals[c] for c in matrix.index]
        return matrix.sort_index()

    @classmethod
    def normalize_rates_per_k(
        cls,
        cfd_matrix: pd.DataFrame,
        k: float = 1000.0
    ) -> pd.DataFrame:
        """Normalize token occurrences per 1,000 words."""
        norm_df = cfd_matrix.copy()
        denominators = norm_df["TOTAL_TOKENS"].replace(0, 1)

        cols = [c for c in norm_df.columns if c != "TOTAL_TOKENS"]
        for col in cols:
            norm_df[col] = (norm_df[col] / denominators) * k
            norm_df[col] = norm_df[col].round(2)

        return norm_df
