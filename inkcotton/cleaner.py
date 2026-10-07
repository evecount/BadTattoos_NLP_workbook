"""
Module 1: Ingestion, OCR Glitches & Regex Normalization
========================================================
SloganCleaner normalizing OCR scanning artifacts, line breaks,
erratic capitalization, and punctuation noise from photo-caption scrapes.
"""

from __future__ import annotations
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd


class SloganCleaner:
    """
    Regex-driven cleaner for tattoo captions and novelty t-shirt slogans.
    
    Handles:
    - Erratic alternating casing (e.g., 'nO rEgReTs' -> 'No Regrets')
    - Preserves all-caps deliberate emphasis if desired
    - Strips OCR artifacts, arrow pointers ('--->'), repeated exclamation points
    - Normalizes line breaks and whitespace
    """

    OCR_NOISE_PATTERN = re.compile(r"[-–—]{2,}>?|[<]{2,}[-–—]*|[\*•~_#@]+")
    REPEATED_PUNCTUATION = re.compile(r"([!?,.:;])\1+")
    WHITESPACE_PATTERN = re.compile(r"\s+")

    def __init__(self, preserve_all_caps: bool = True):
        self.preserve_all_caps = preserve_all_caps

    def clean_ocr_artifacts(self, text: str) -> str:
        """Remove decorative glyphs, ASCII arrows, and scanner artifacts."""
        cleaned = self.OCR_NOISE_PATTERN.sub(" ", text)
        # Collapse multiple punctuation e.g. '!!!' -> '!'
        cleaned = self.REPEATED_PUNCTUATION.sub(r"\1", cleaned)
        return cleaned.strip()

    def normalize_casing(self, text: str) -> str:
        """
        Fix chaotic alternating casing (e.g. 'nO rEgReTs') while preserving
        meaningful all-caps slogans ('NO REGRETS').
        """
        stripped = text.strip()
        if not stripped:
            return ""

        # If already all uppercase, keep it if configured
        if self.preserve_all_caps and stripped.isupper():
            return stripped

        # Detect erratic camel/alternating casing (e.g., lowercase followed by uppercase in same word)
        words = stripped.split()
        normalized_words = []
        for w in words:
            # If word has mixed erratic case (e.g. 'rEgReTs')
            has_lower = any(c.islower() for c in w)
            has_upper = any(c.isupper() for c in w)
            if has_lower and has_upper and not (w[0].isupper() and w[1:].islower()):
                normalized_words.append(w.capitalize())
            else:
                normalized_words.append(w)

        res = " ".join(normalized_words)
        # Ensure sentence start is capitalized
        return res[0].upper() + res[1:] if res else ""

    def clean_slogan(self, text: str) -> str:
        """Complete normalization pipeline for a single slogan."""
        if not isinstance(text, str):
            return ""
        # 1. Normalize linebreaks to single space
        no_breaks = text.replace("\r", " ").replace("\n", " ")
        # 2. Strip OCR glyphs and trailing arrows
        no_artifacts = self.clean_ocr_artifacts(no_breaks)
        # 3. Collapse whitespace
        clean_spaces = self.WHITESPACE_PATTERN.sub(" ", no_artifacts).strip()
        # 4. Remove unwanted whitespace preceding punctuation
        clean_punct = re.sub(r"\s+([!?,.:;])", r"\1", clean_spaces)
        # 5. Normalize erratic casing
        return self.normalize_casing(clean_punct)

    def process_dataframe(
        self,
        df: pd.DataFrame,
        text_column: str = "raw_text",
        output_column: str = "cleaned_text"
    ) -> pd.DataFrame:
        """Batch-process a DataFrame of scraped slogans."""
        out_df = df.copy()
        out_df[output_column] = out_df[text_column].apply(self.clean_slogan)
        return out_df

    def process_file(
        self,
        file_path: str | Path,
        text_column: str = "raw_text"
    ) -> pd.DataFrame:
        """Load and normalize a CSV or JSON file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if path.suffix.lower() == ".csv":
            df = pd.read_csv(path)
        elif path.suffix.lower() == ".json":
            df = pd.read_json(path)
        else:
            raise ValueError(f"Unsupported format: {path.suffix}")

        return self.process_dataframe(df, text_column=text_column)
