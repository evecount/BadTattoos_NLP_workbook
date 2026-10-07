"""
Module 6: Syntactic Ambiguity & Dependency Parsing (spaCy)
===========================================================
AmbiguityParser detecting punctuation shifts, comma-induced semantic inversions
(e.g., 'Let's eat kids' vs 'Let's eat, kids'), and modifier attachment ambiguities.
"""

from __future__ import annotations
import re
from typing import Any, Dict, List, Optional, Tuple


class AmbiguityParser:
    """
    Syntactic dependency and ambiguity parser for graphic t-shirt slogans.
    """

    def __init__(self, spacy_model: str = "en_core_web_sm"):
        self.model_name = spacy_model
        self.nlp = None
        self._init_spacy()

    def _init_spacy(self):
        """Attempt to load spaCy model."""
        try:
            import spacy
            self.nlp = spacy.load(self.model_name)
        except Exception:
            self.nlp = None

    def analyze_vocative_comma(self, sentence: str) -> dict[str, any]:
        """
        Analyze whether missing commas shift a human noun into a direct object (cannibalism!).
        Contrasts:
            'Let's eat kids' -> 'kids' = Direct Object of 'eat'
            'Let's eat, kids' -> 'kids' = Vocative address
        """
        s = sentence.strip()
        s_lower = s.lower()
        has_vocative_comma = bool(re.search(r",\s*(?:kids|grandma|children|people)\b", s_lower))

        if self.nlp:
            doc = self.nlp(s)
            target_dep = None
            head_verb = None
            target_token = None

            for token in doc:
                if token.text.lower() in ("kids", "grandma", "children", "people"):
                    target_token = token.text
                    target_dep = token.dep_
                    head_verb = token.head.text
                    break

            is_cannibalistic = not has_vocative_comma and (
                (target_dep in ("dobj", "obj") and head_verb and head_verb.lower() in ("eat", "feed", "cook"))
                or ("eat" in s_lower and any(n in s_lower for n in ("kids", "grandma", "children")))
            )

            return {
                "sentence": s,
                "has_vocative_comma": has_vocative_comma,
                "target_noun": target_token,
                "head_verb": head_verb,
                "dependency_role": target_dep or ("dobj" if is_cannibalistic else "vocative"),
                "hazard_warning": "🚨 Cannibalism detected: Direct object relation without vocative comma!" if is_cannibalistic else "✅ Safe vocative or intransitive construct.",
            }
        else:
            # Deterministic heuristic fallback
            is_hazard = ("eat" in s_lower or "cook" in s_lower) and ("kids" in s_lower or "grandma" in s_lower) and not has_vocative_comma
            return {
                "sentence": s,
                "has_vocative_comma": has_vocative_comma,
                "target_noun": "kids" if "kids" in s_lower else ("grandma" if "grandma" in s_lower else None),
                "head_verb": "eat",
                "dependency_role": "dobj" if not has_vocative_comma else "vocative",
                "hazard_warning": "🚨 Cannibalism detected: Direct object relation without vocative comma!" if is_hazard else "✅ Safe vocative or intransitive construct.",
            }

    def extract_dependency_tree(self, text: str) -> list[dict[str, str]]:
        """Extract flat token dependency relations."""
        if self.nlp:
            doc = self.nlp(text)
            return [
                {
                    "text": token.text,
                    "pos": token.pos_,
                    "dep": token.dep_,
                    "head": token.head.text,
                }
                for token in doc
            ]
        else:
            # Fallback heuristic tokens
            tokens = text.split()
            return [
                {
                    "text": t,
                    "pos": "NOUN" if t.isalnum() else "PUNCT",
                    "dep": "root" if i == 0 else "dep",
                    "head": tokens[0],
                }
                for i, t in enumerate(tokens)
            ]
