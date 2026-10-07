"""
Module 8: Slogan Generator & Auto-Roaster (Capstone)
====================================================
SloganEngine & AutoRoaster synthesizing candidate tattoo and graphic tee slogans
using Markov models, and auditing submissions for cliché density, typos, and syntax hazards.
"""

from __future__ import annotations
import math
import random
import re
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd

from inkcotton.spellchecker import LevenshteinDistance, RagretsEngine
from inkcotton.syntax import AmbiguityParser
from inkcotton.metrics import ClicheDetector


class SloganEngine:
    """
    Category-Conditioned Markov Language Model for slogan generation.
    """

    START_TOKEN = "<START>"
    END_TOKEN = "<END>"

    def __init__(self, n: int = 2):
        self.n = n
        self.transitions: dict[str, dict[tuple[str, ...], Counter]] = defaultdict(lambda: defaultdict(Counter))
        self.category_vocabs: dict[str, set[str]] = defaultdict(set)

    def train_on_dataframe(
        self,
        df: pd.DataFrame,
        category_col: str = "category",
        text_col: str = "cleaned_text"
    ) -> None:
        """Fit Markov transitions across categories."""
        for _, row in df.iterrows():
            cat = str(row.get(category_col, "GENERAL")).strip().upper()
            text = str(row.get(text_col, "")).strip()
            if not text:
                continue

            tokens = [t.lower() for t in re.findall(r"\b\w+(?:'\w+)?\b|[.!,?]", text)]
            if not tokens:
                continue

            padded = [self.START_TOKEN] * (self.n - 1) + tokens + [self.END_TOKEN]
            for t in tokens:
                self.category_vocabs[cat].add(t)

            for i in range(len(padded) - (self.n - 1)):
                prefix = tuple(padded[i : i + self.n - 1])
                next_word = padded[i + self.n - 1]
                self.transitions[cat][prefix][next_word] += 1

    def sample_next_word(
        self,
        category: str,
        prefix: tuple[str, ...],
        temperature: float = 1.0
    ) -> str:
        """Sample next token given prefix context and temperature."""
        cat_clean = category.strip().upper()
        cat_trans = self.transitions.get(cat_clean, {})
        counts = cat_trans.get(prefix)

        if not counts:
            if not self.category_vocabs[cat_clean]:
                return self.END_TOKEN
            return random.choice(list(self.category_vocabs[cat_clean]) + [self.END_TOKEN])

        words = list(counts.keys())
        raw_freqs = [counts[w] for w in words]

        if temperature <= 0.05:
            return words[raw_freqs.index(max(raw_freqs))]

        scaled = [math.pow(c, 1.0 / max(0.1, temperature)) for c in raw_freqs]
        total = sum(scaled)
        probs = [s / total for s in scaled]

        return random.choices(words, weights=probs, k=1)[0]

    def generate_slogan(
        self,
        category: str,
        prompt: Optional[str] = None,
        max_tokens: int = 15,
        temperature: float = 0.8,
        seed: Optional[int] = None
    ) -> str:
        """Generate a single category-conditioned slogan."""
        if seed is not None:
            random.seed(seed)

        cat_clean = category.strip().upper()
        if prompt:
            prompt_tokens = [t.lower() for t in re.findall(r"\b\w+(?:'\w+)?\b|[.!,?]", prompt)]
            generated = list(prompt_tokens)
            if len(prompt_tokens) >= self.n - 1:
                prefix = tuple(prompt_tokens[-(self.n - 1):])
            else:
                prefix = tuple([self.START_TOKEN] * (self.n - 1 - len(prompt_tokens)) + prompt_tokens)
        else:
            generated = []
            prefix = tuple([self.START_TOKEN] * (self.n - 1))

        for _ in range(max_tokens):
            next_word = self.sample_next_word(cat_clean, prefix, temperature=temperature)
            if next_word == self.END_TOKEN:
                break
            generated.append(next_word)
            prefix = tuple(list(prefix[1:]) + [next_word])

        out = " ".join(generated)
        out = re.sub(r"\s+([.!,?])", r"\1", out)
        return out.capitalize() if out else "Live laugh love."


class AutoRoaster:
    """
    Slogan quality auditor and snarky roast generator.
    Evaluates cliché redundancy, spelling blunders, and syntactic hazards.
    """

    KNOWN_TATTOO_TYPOS = {
        "ragrets": "regrets",
        "strenght": "strength",
        "loose": "lose",
        "pee": "pea",
        "angle": "angel",
        "diarrea": "diem",
        "fudge": "judge",
    }

    def __init__(self):
        self.cliche_detector = ClicheDetector()
        self.syntax_parser = AmbiguityParser()

    def audit_slogan(self, text: str) -> dict[str, any]:
        """Perform comprehensive NLP audit of a proposed tattoo or shirt slogan."""
        clean_text = text.strip()
        tokens = re.findall(r"\b[A-Za-z]+\b", clean_text.lower())

        # 1. Cliché Density
        cliche_report = self.cliche_detector.evaluate_cliche_density(tokens)

        # 2. Spelling Blunder Check
        spelling_flags = []
        for word in tokens:
            if word in self.KNOWN_TATTOO_TYPOS:
                spelling_flags.append({
                    "flagged_word": word,
                    "intended_correction": self.KNOWN_TATTOO_TYPOS[word],
                    "warning": f"Permanent ink warning: Did you mean '{self.KNOWN_TATTOO_TYPOS[word]}'?",
                })

        # 3. Syntactic Ambiguity Check
        syntax_report = self.syntax_parser.analyze_vocative_comma(clean_text)

        # 4. Generate Roast Verdict
        roasts = []
        if spelling_flags:
            roasts.append(f"💀 Tattoo Artist Alert: You spelled '{spelling_flags[0]['flagged_word']}'. That is laser removal waiting to happen.")
        if "Cannibalism" in syntax_report["hazard_warning"]:
            roasts.append("⚠️ Missing comma emergency: You just told the world you eat children.")
        if cliche_report["cliche_ratio"] >= 0.5:
            roasts.append("🥱 Cliché Overload: This slogan has been tattooed on 4.2 million suburban biceps since 2004.")

        if not roasts:
            verdict = "✨ Actually wearable! No obvious grammatical war crimes detected."
        else:
            verdict = " | ".join(roasts)

        return {
            "slogan": clean_text,
            "cliche_percentage": round(cliche_report["cliche_ratio"] * 100, 1),
            "spelling_hazards": spelling_flags,
            "syntax_hazard": syntax_report["hazard_warning"],
            "roast_verdict": verdict,
        }
