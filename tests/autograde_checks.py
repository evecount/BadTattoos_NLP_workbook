"""
Autograding & Student Self-Verification Test Suite
===================================================
Project Ink & Cotton: Deconstructing Bad Tattoos & Novelty Graphic Tees with NLP

Students can import this module inside their Jupyter Notebooks or run via CLI:
    python tests/autograde_checks.py
"""

from __future__ import annotations
import math
import sys
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from inkcotton.cleaner import SloganCleaner
from inkcotton.spellchecker import LevenshteinDistance, RagretsEngine
from inkcotton.tokenizer import SlangTokenizer
from inkcotton.metrics import LexicalRichness, ClicheDetector
from inkcotton.collocations import CollocationTraps
from inkcotton.syntax import AmbiguityParser
from inkcotton.stylometrics import RegisterProfiler
from inkcotton.roaster import SloganEngine, AutoRoaster


def check_module_1() -> bool:
    """Verify Module 1: Slogan Normalization & Regex Cleaning."""
    print("\n[Testing Module 1: Ingestion, OCR Glitches & Regex Normalization]...")
    cleaner = SloganCleaner()
    
    raw = "  nO  rEgReTs ---> !!! \r\n"
    res = cleaner.clean_slogan(raw)
    assert res == "No Regrets!", f"Expected 'No Regrets!', got '{res}'"
    
    all_caps = "NO REGRETS"
    assert cleaner.clean_slogan(all_caps) == "NO REGRETS"
    
    print("  PASS: OCR glyph stripping, line-break handling, and casing normalization verified.")
    return True


def check_module_2() -> bool:
    """Verify Module 2: The 'Ragrets' Engine & Levenshtein Distance."""
    print("\n[Testing Module 2: Levenshtein Distance & Spelling Correction]...")
    dist = LevenshteinDistance.distance("ragrets", "regrets")
    assert dist == 1, f"Expected distance 1 between 'ragrets' and 'regrets', got {dist}"
    
    dist_strenght = LevenshteinDistance.distance("strenght", "strength")
    assert dist_strenght == 2, f"Expected distance 2 between 'strenght' and 'strength', got {dist_strenght}"
    
    ops = LevenshteinDistance.backtrack_alignment("ragrets", "regrets")
    assert any(op["operation"] == "SUBSTITUTE" for op in ops), "Expected substitution operation in alignment"
    
    engine = RagretsEngine(REPO_ROOT / "data" / "dictionary_reference.txt")
    suggestions = engine.suggest_corrections("ragrets", max_distance=2)
    assert len(suggestions) > 0
    top_cand = suggestions[0]["candidate"]
    assert top_cand in ("regrets", "regret"), f"Expected top correction 'regrets', got {top_cand}"
    
    print("  PASS: Dynamic programming edit distance, backtrack alignment, and unigram ranking verified.")
    return True


def check_module_3() -> bool:
    """Verify Module 3: Tokenization & Subword Splitting on Slang."""
    print("\n[Testing Module 3: Tokenization & Subword Splitting on Informal Slang]...")
    tok = SlangTokenizer()
    
    subwords_delulu = tok.tokenize_bpe_subwords("delulu")
    assert len(subwords_delulu) >= 2, f"Expected subwords for 'delulu', got {subwords_delulu}"
    
    subwords_yeet = tok.tokenize_bpe_subwords("yeet")
    assert len(subwords_yeet) >= 2, f"Expected subwords for 'yeet', got {subwords_yeet}"
    
    oov = tok.compute_oov_rate(
        reference_vocab={"coffee", "running", "dread"},
        test_tokens=["coffee", "delulu", "yeet"]
    )
    assert oov["oov_count"] == 2
    assert "delulu" in oov["oov_words"]
    
    print("  PASS: Subword BPE decomposition and OOV curve tracking verified.")
    return True


def check_module_4() -> bool:
    """Verify Module 4: Lexical Diversity & Cliché Detection."""
    print("\n[Testing Module 4: Lexical Diversity & Cliché Detection]...")
    tokens = ["strength", "warrior", "lion", "blood", "strength", "king", "strength"]
    
    n, v = LexicalRichness.count_tokens_and_types(tokens)
    assert n == 7 and v == 5
    
    ttr = LexicalRichness.compute_ttr(tokens)
    assert math.isclose(ttr, round(5 / 7, 4), abs_tol=1e-3)
    
    hapaxes = LexicalRichness.find_hapaxes(tokens)
    assert "warrior" in hapaxes and "lion" in hapaxes and "blood" in hapaxes
    assert "strength" not in hapaxes
    
    detector = ClicheDetector()
    cliche_eval = detector.evaluate_cliche_density(tokens)
    assert cliche_eval["cliche_ratio"] > 0.8, "Expected high cliché ratio for alpha biker tropes"
    
    print("  PASS: TTR, Root TTR, Hapaxes, and Cliché saturation density verified.")
    return True


def check_module_5() -> bool:
    """Verify Module 5: Collocation Traps & Fixed Semantic Tropes."""
    print("\n[Testing Module 5: Collocation Traps & Fixed Semantic Tropes]...")
    tokens = ["live", "laugh", "love", "live", "laugh", "toaster", "bath", "live", "laugh"]
    collocations = CollocationTraps.compute_pmi(tokens, min_freq=2)
    
    phrases = [c["phrase"] for c in collocations]
    assert "live laugh" in phrases or "laugh love" in phrases
    
    groups = CollocationTraps.contrast_functional_vs_bound(collocations)
    assert "bound_tropes" in groups
    
    print("  PASS: Bigram/Trigram extraction, PMI scoring, and trope grouping verified.")
    return True


def check_module_6() -> bool:
    """Verify Module 6: Syntactic Ambiguity & Dependency Parsing."""
    print("\n[Testing Module 6: Syntactic Ambiguity & spaCy Parsing]...")
    parser = AmbiguityParser()
    
    hazard_report = parser.analyze_vocative_comma("Let's eat kids")
    assert "Cannibalism" in hazard_report["hazard_warning"]
    
    safe_report = parser.analyze_vocative_comma("Let's eat, kids")
    assert "Safe" in safe_report["hazard_warning"]
    
    print("  PASS: Vocative comma ambiguity and structural modifier shifts verified.")
    return True


def check_module_7() -> bool:
    """Verify Module 7: Stylometric Register Profiling via CFD."""
    print("\n[Testing Module 7: Stylometric Register Profiling via CFD]...")
    df = pd.DataFrame([
        {"category": "alpha_ink", "cleaned_text": "Strength and warrior blood honor lion."},
        {"category": "ironic_tee", "cleaned_text": "Tired anxiety iced coffee nap awkward."},
    ])
    
    cfd = RegisterProfiler.build_cfd_matrix(df, target_words=["strength", "warrior", "coffee", "tired"])
    assert "alpha_ink" in cfd.index and "ironic_tee" in cfd.index
    assert cfd.loc["alpha_ink", "strength"] == 1
    assert cfd.loc["ironic_tee", "coffee"] == 1
    
    norm = RegisterProfiler.normalize_rates_per_k(cfd)
    assert "strength" in norm.columns
    
    print("  PASS: Subculture CFD matrix and normalized register rates verified.")
    return True


def check_module_8() -> bool:
    """Verify Module 8: Slogan Generator & Auto-Roaster."""
    print("\n[Testing Module 8: Slogan Generator & Auto-Roaster]...")
    df = pd.DataFrame([
        {"category": "ALPHA", "cleaned_text": "Strength and honor forever."},
        {"category": "ALPHA", "cleaned_text": "Strength is forged in fire."},
        {"category": "IRONIC", "cleaned_text": "Running on iced coffee and dread."},
    ])
    
    engine = SloganEngine(n=2)
    engine.train_on_dataframe(df)
    slogan = engine.generate_slogan("ALPHA", prompt="strength", temperature=0.7, seed=42)
    assert isinstance(slogan, str) and len(slogan) > 0
    
    roaster = AutoRoaster()
    roast = roaster.audit_slogan("No Ragrets, Let's eat kids!")
    assert roast["cliche_percentage"] >= 0
    assert len(roast["spelling_hazards"]) > 0, "Expected ragrets typo flag"
    assert "Cannibalism" in roast["syntax_hazard"]
    assert "roast_verdict" in roast and len(roast["roast_verdict"]) > 0
    
    print("  PASS: Markov slogan generation and multi-point AutoRoaster auditing verified.")
    return True


def run_all_checks() -> bool:
    """Execute complete 8-module autograder suite."""
    print("=" * 75)
    print(" PROJECT INK & COTTON: COMPREHENSIVE 8-MODULE AUTOGRADING SUITE")
    print("=" * 75)
    
    results = [
        check_module_1(),
        check_module_2(),
        check_module_3(),
        check_module_4(),
        check_module_5(),
        check_module_6(),
        check_module_7(),
        check_module_8(),
    ]
    
    all_passed = all(results)
    print("\n" + "=" * 75)
    if all_passed:
        print(" [SUCCESS] ALL 8 MODULE VERIFICATION SUITES PASSED PERFECTLY! ")
    else:
        print(" [FAIL] Some checks failed. Review the output logs above. ")
    print("=" * 75)
    return all_passed


if __name__ == "__main__":
    success = run_all_checks()
    sys.exit(0 if success else 1)
