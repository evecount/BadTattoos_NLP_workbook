"""
Module 3: Tokenization & Subword Splitting on Informal Slang
============================================================
SlangTokenizer handling modern internet catchphrases ('yeet', 'delulu', 'smol'),
word-level vs subword BPE splitting, and Out-of-Vocabulary (OOV) analysis.
"""

from __future__ import annotations
import re
from collections import Counter
from typing import Any, Dict, List, Set, Tuple


class SlangTokenizer:
    """
    Tokenizer designed for novelty tees and informal youth vernacular.
    
    Demonstrates:
    - Standard word-level regex splitting
    - Subword segmentation (Byte-Pair Encoding simulation)
    - Prevention of <UNK> collapse for internet neologisms ('delulu', 'yeet', 'smol')
    - OOV tracking against baseline vocabularies
    """

    WORD_PATTERN = re.compile(r"\b[A-Za-z0-9]+(?:'[A-Za-z]+)?\b")

    # Domain morphemes for subword decomposition
    SUBWORD_VOCAB = {
        "de", "lu", "ye", "et", "sm", "ol", "br", "uh",
        "over", "think", "er", "ing", "un", "der", "caff", "ein", "ated",
        "intro", "vert", "ed", "gob", "lin", "dum", "pster", "fire",
        "cha", "os", "fer", "al", "pro", "crast", "in", "ate", "tion",
        "post", "pre", "sarc", "asm", "ic", "exist", "ent", "ial"
    }

    def __init__(self, custom_morphemes: set[str] | None = None):
        self.subwords = set(self.SUBWORD_VOCAB)
        if custom_morphemes:
            self.subwords.update(custom_morphemes)

    def tokenize_words(self, text: str, lowercase: bool = True) -> list[str]:
        """Standard word-level alphanumeric tokenization."""
        target = text.lower() if lowercase else text
        return self.WORD_PATTERN.findall(target)

    def tokenize_bpe_subwords(self, word: str) -> list[str]:
        """
        Segment a word into subwords using longest-matching morphemes.
        
        Example:
        'delulu' -> ['de', '##lu', '##lu']
        'yeet'   -> ['ye', '##et']
        'smol'   -> ['sm', '##ol']
        """
        w = word.lower().strip()
        if not w:
            return []

        tokens: list[str] = []
        i = 0
        while i < len(w):
            matched = False
            for j in range(len(w), i, -1):
                chunk = w[i:j]
                if chunk in self.subwords or j - i <= 2:
                    tag = chunk if i == 0 else f"##{chunk}"
                    tokens.append(tag)
                    i = j
                    matched = True
                    break
            if not matched:
                tag = w[i] if i == 0 else f"##{w[i]}"
                tokens.append(tag)
                i += 1
        return tokens

    def tokenize_slogan_subwords(self, slogan: str) -> list[str]:
        """Apply subword tokenization across all words in a slogan."""
        words = self.tokenize_words(slogan)
        result = []
        for w in words:
            result.extend(self.tokenize_bpe_subwords(w))
        return result

    def compute_oov_rate(
        self,
        reference_vocab: set[str],
        test_tokens: list[str]
    ) -> dict[str, any]:
        """
        Evaluate how many tokens fall outside reference vocabulary.
        """
        if not test_tokens:
            return {"total_tokens": 0, "oov_count": 0, "oov_rate": 0.0, "oov_words": []}

        ref_lower = {w.lower() for w in reference_vocab}
        oov_list = [t for t in test_tokens if t.lower() not in ref_lower]
        oov_rate = len(oov_list) / len(test_tokens)

        return {
            "total_tokens": len(test_tokens),
            "oov_count": len(oov_list),
            "oov_rate": round(oov_rate, 4),
            "oov_words": sorted(list(set(oov_list))),
        }
