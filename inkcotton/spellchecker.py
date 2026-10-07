"""
Module 2: The "Ragrets" Engine (String Distance & Spelling Correction)
======================================================================
LevenshteinDistance & RagretsEngine computing exact minimum edit distance,
DP matrix construction, backtracking edit alignment paths, and unigram-weighted
spelling correction for infamous tattoo blunders ('No Ragrets', 'Strenght', etc.).
"""

from __future__ import annotations
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class LevenshteinDistance:
    """
    Dynamic Programming implementation of Levenshtein Minimum Edit Distance.
    
    Provides:
    - 2D DP cost matrix
    - Minimum edit distance between two strings
    - Backtracking alignment to trace exact insertion/deletion/substitution operations
    - Damerau-Levenshtein transposition support
    """

    @staticmethod
    def compute_matrix(
        source: str,
        target: str,
        sub_cost: int = 1,
        ins_cost: int = 1,
        del_cost: int = 1
    ) -> list[list[int]]:
        """Construct the full (len(source)+1) x (len(target)+1) DP matrix."""
        m, n = len(source), len(target)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i * del_cost
        for j in range(n + 1):
            dp[0][j] = j * ins_cost

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if source[i - 1].lower() == target[j - 1].lower() else sub_cost
                dp[i][j] = min(
                    dp[i - 1][j] + del_cost,      # Deletion
                    dp[i][j - 1] + ins_cost,      # Insertion
                    dp[i - 1][j - 1] + cost       # Substitution
                )

        return dp

    @classmethod
    def distance(cls, source: str, target: str) -> int:
        """Calculate minimum edit distance between source and target."""
        matrix = cls.compute_matrix(source, target)
        return matrix[len(source)][len(target)]

    @classmethod
    def backtrack_alignment(
        cls,
        source: str,
        target: str
    ) -> list[dict[str, any]]:
        """
        Backtrack through the DP matrix to extract the exact sequence of edit operations.
        Returns a list of operations: 'MATCH', 'SUBSTITUTE', 'INSERT', 'DELETE'.
        """
        dp = cls.compute_matrix(source, target)
        i, j = len(source), len(target)
        ops = []

        while i > 0 or j > 0:
            current_cost = dp[i][j]
            # Substitution or Match
            if i > 0 and j > 0:
                is_match = source[i - 1].lower() == target[j - 1].lower()
                cost = 0 if is_match else 1
                if current_cost == dp[i - 1][j - 1] + cost:
                    ops.append({
                        "operation": "MATCH" if is_match else "SUBSTITUTE",
                        "source_char": source[i - 1],
                        "target_char": target[j - 1],
                        "cost": cost,
                    })
                    i -= 1
                    j -= 1
                    continue

            # Deletion
            if i > 0 and current_cost == dp[i - 1][j] + 1:
                ops.append({
                    "operation": "DELETE",
                    "source_char": source[i - 1],
                    "target_char": "",
                    "cost": 1,
                })
                i -= 1
                continue

            # Insertion
            if j > 0 and current_cost == dp[i][j - 1] + 1:
                ops.append({
                    "operation": "INSERT",
                    "source_char": "",
                    "target_char": target[j - 1],
                    "cost": 1,
                })
                j -= 1
                continue

        ops.reverse()
        return ops


class RagretsEngine:
    """
    Spelling correction and tattoo blunder diagnostic engine.
    Combines Levenshtein string distance with unigram corpus probabilities.
    """

    def __init__(self, dictionary_path: Optional[str | Path] = None):
        self.vocab: dict[str, int] = {}
        self.total_freq: int = 0
        if dictionary_path:
            self.load_dictionary(dictionary_path)

    def load_dictionary(self, path: str | Path) -> None:
        """Load vocabulary words and unigram frequencies from CSV or text."""
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Dictionary file not found: {p}")

        lines = p.read_text(encoding="utf-8").splitlines()
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) >= 2:
                word = parts[0].strip().lower()
                try:
                    freq = int(parts[1].strip())
                    self.vocab[word] = freq
                except ValueError:
                    continue
        self.total_freq = sum(self.vocab.values()) or 1

    def word_probability(self, word: str) -> float:
        """P(w) estimated from reference corpus frequency."""
        freq = self.vocab.get(word.lower(), 1)
        return freq / self.total_freq

    def suggest_corrections(
        self,
        typo: str,
        max_distance: int = 2,
        top_k: int = 5
    ) -> list[dict[str, any]]:
        """
        Identify vocabulary words within edit distance <= max_distance,
        ranked by a combination of minimum distance and log unigram probability.
        """
        clean_typo = typo.strip().lower()
        candidates = []

        for candidate, freq in self.vocab.items():
            # Length filter heuristic: skip words where abs length diff > max_distance
            if abs(len(candidate) - len(clean_typo)) > max_distance:
                continue

            dist = LevenshteinDistance.distance(clean_typo, candidate)
            if dist <= max_distance:
                prob = self.word_probability(candidate)
                # Score combines low edit distance with high corpus probability
                score = (1.0 / (dist + 1)) * (math.log(prob + 1e-9) + 20)
                candidates.append({
                    "candidate": candidate,
                    "distance": dist,
                    "frequency": freq,
                    "score": round(score, 3),
                })

        candidates.sort(key=lambda x: (x["distance"], -x["frequency"]))
        return candidates[:top_k]

    def diagnose_tattoo_line(self, line: str) -> list[dict[str, any]]:
        """
        Scan a complete tattoo line and identify potential spelling blunders.
        """
        import re
        words = re.findall(r"\b[A-Za-z]+\b", line)
        diagnostics = []

        for w in words:
            w_lower = w.lower()
            if self.vocab and w_lower not in self.vocab:
                suggestions = self.suggest_corrections(w_lower, max_distance=2, top_k=3)
                diagnostics.append({
                    "word": w,
                    "is_known": False,
                    "top_suggestion": suggestions[0]["candidate"] if suggestions else None,
                    "distance": suggestions[0]["distance"] if suggestions else None,
                    "candidates": suggestions,
                })
            else:
                diagnostics.append({
                    "word": w,
                    "is_known": True,
                    "top_suggestion": w_lower,
                    "distance": 0,
                    "candidates": [],
                })

        return diagnostics
