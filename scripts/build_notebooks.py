"""
Notebook Builder for Project Ink & Cotton
=========================================
Generates all 8 interactive student workbooks matching the pedagogical syllabus.
"""

import json
from pathlib import Path

NOTEBOOKS_DIR = Path("notebooks")
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)


def create_cell(cell_type: str, source: list[str]) -> dict:
    cell = {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source],
    }
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell


def build_notebook(cells: list[dict], filename: str):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    path = NOTEBOOKS_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Generated {path}")


# 01_ocr_slogan_cleaner.ipynb
def build_nb_01():
    cells = [
        create_cell("markdown", [
            "# Project Ink & Cotton: Module 1",
            "## Ingestion, OCR Glitches & Regex Normalization",
            "",
            "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/evecount/BadTattoos_NLP_workbook/blob/main/notebooks/01_ocr_slogan_cleaner.ipynb)",
            "",
            "### Learning Objectives",
            "1. Clean OCR artifacts, linebreaks, and decorative glyphs from scraped caption text.",
            "2. Normalize erratic alternating casing (`nO rEgReTs`) while preserving deliberate stylistic ALL-CAPS.",
            "3. Enforce clean typography and eliminate unwanted whitespace before punctuation."
        ]),
        create_cell("code", [
            "import sys",
            "sys.path.insert(0, '..')",
            "from inkcotton import SloganCleaner",
            "import pandas as pd",
            "",
            "cleaner = SloganCleaner()",
            "print('Cleaner loaded.')"
        ]),
        create_cell("markdown", [
            "### 1. Cleaning Chaotic Captions"
        ]),
        create_cell("code", [
            "samples = [",
            "    '  nO  rEgReTs ---> !!! \\r\\n',",
            "    'NO RAGRETS',",
            "    'Let\\'s  eat  kids   ! ! !',",
            "    'Born to   loose  ---*~*---'",
            "]",
            "for s in samples:",
            "    print(f'RAW:    {repr(s)}')",
            "    print(f'CLEAN:  {cleaner.clean_slogan(s)}\\n')"
        ]),
        create_cell("markdown", [
            "### 2. Processing Slogan Datasets"
        ]),
        create_cell("code", [
            "df = pd.read_json('../data/combined_slogans_corpus.json')",
            "df[['raw_text', 'cleaned_text', 'category']].head(10)"
        ]),
        create_cell("markdown", [
            "### 3. Self-Verification & Autograding"
        ]),
        create_cell("code", [
            "from tests.autograde_checks import check_module_1",
            "check_module_1()"
        ])
    ]
    build_notebook(cells, "01_ocr_slogan_cleaner.ipynb")


# 02_levenshtein_ragrets.ipynb
def build_nb_02():
    cells = [
        create_cell("markdown", [
            "# Project Ink & Cotton: Module 2",
            "## The 'Ragrets' Engine (String Distance & Spelling Correction)",
            "",
            "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/evecount/BadTattoos_NLP_workbook/blob/main/notebooks/02_levenshtein_ragrets.ipynb)",
            "",
            "### Learning Objectives",
            "1. Implement Dynamic Programming Levenshtein Minimum Edit Distance from scratch.",
            "2. Backtrack through the DP matrix to extract the exact alignment path of edits (`SUBSTITUTE`, `INSERT`, `DELETE`).",
            "3. Diagnose famous tattoo blunders (*No Ragrets*, *Strenght*, *Sweet Pee*) and rank candidates using unigram probabilities."
        ]),
        create_cell("code", [
            "import sys",
            "sys.path.insert(0, '..')",
            "from inkcotton import LevenshteinDistance, RagretsEngine",
            "import pandas as pd",
            "",
            "engine = RagretsEngine('../data/dictionary_reference.txt')",
            "print('Ragrets Engine ready.')"
        ]),
        create_cell("markdown", [
            "### 1. Dynamic Programming Edit Distance"
        ]),
        create_cell("code", [
            "source = 'ragrets'",
            "target = 'regrets'",
            "dist = LevenshteinDistance.distance(source, target)",
            "print(f'Levenshtein Distance between \"{source}\" and \"{target}\": {dist}')",
            "",
            "ops = LevenshteinDistance.backtrack_alignment(source, target)",
            "print('\\nBacktracking Alignment:')",
            "pd.DataFrame(ops)"
        ]),
        create_cell("markdown", [
            "### 2. Candidate Correction & Unigram Ranking"
        ]),
        create_cell("code", [
            "blunders = ['ragrets', 'strenght', 'loose', 'pee', 'angle', 'diarrea']",
            "for b in blunders:",
            "    suggestions = engine.suggest_corrections(b, max_distance=2, top_k=3)",
            "    cands = ', '.join([f\"{c['candidate']} (dist={c['distance']})\" for c in suggestions])",
            "    print(f'{b:10} -> {cands}')"
        ]),
        create_cell("markdown", [
            "### 3. Self-Verification & Autograding"
        ]),
        create_cell("code", [
            "from tests.autograde_checks import check_module_2",
            "check_module_2()"
        ])
    ]
    build_notebook(cells, "02_levenshtein_ragrets.ipynb")


# 03_subword_slang_tokens.ipynb
def build_nb_03():
    cells = [
        create_cell("markdown", [
            "# Project Ink & Cotton: Module 3",
            "## Tokenization & Subword Splitting on Informal Slang",
            "",
            "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/evecount/BadTattoos_NLP_workbook/blob/main/notebooks/03_subword_slang_tokens.ipynb)",
            "",
            "### Learning Objectives",
            "1. Compare word-level vs. subword Byte-Pair Encoding (BPE) on internet slang (*delulu*, *yeet*, *smol*).",
            "2. Trace how subword decomposition prevents out-of-vocabulary tokens from becoming `<UNK>`.",
            "3. Compute Out-of-Vocabulary (OOV) rates across varying reference dictionaries."
        ]),
        create_cell("code", [
            "import sys",
            "sys.path.insert(0, '..')",
            "from inkcotton import SlangTokenizer",
            "import pandas as pd",
            "",
            "tok = SlangTokenizer()",
            "print('Slang tokenizer initialized.')"
        ]),
        create_cell("markdown", [
            "### 1. Subword Segmentation of Internet Catchphrases"
        ]),
        create_cell("code", [
            "slang_words = ['delulu', 'yeet', 'smol', 'overthinker', 'goblin', 'undercaffeinated']",
            "for w in slang_words:",
            "    print(f'{w:16} -> {tok.tokenize_bpe_subwords(w)}')"
        ]),
        create_cell("markdown", [
            "### 2. OOV Tracking Across Graphic Tees"
        ]),
        create_cell("code", [
            "ref_vocab = {'running', 'on', 'coffee', 'and', 'dread'}",
            "slogan = 'Running on iced coffee and certified delulu energy'",
            "words = tok.tokenize_words(slogan)",
            "oov_report = tok.compute_oov_rate(ref_vocab, words)",
            "print('OOV Evaluation:', oov_report)"
        ]),
        create_cell("markdown", [
            "### 3. Self-Verification & Autograding"
        ]),
        create_cell("code", [
            "from tests.autograde_checks import check_module_3",
            "check_module_3()"
        ])
    ]
    build_notebook(cells, "03_subword_slang_tokens.ipynb")


# 04_cliche_lexical_ttr.ipynb
def build_nb_04():
    cells = [
        create_cell("markdown", [
            "# Project Ink & Cotton: Module 4",
            "## Lexical Diversity & Cliché Detection",
            "",
            "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/evecount/BadTattoos_NLP_workbook/blob/main/notebooks/04_cliche_lexical_ttr.ipynb)",
            "",
            "### Learning Objectives",
            "1. Differentiate between Types ($V$) and Tokens ($N$).",
            "2. Compute standard Type-Token Ratio (TTR) and sample-size invariant Root TTR ($V/\\sqrt{N}$).",
            "3. Extract Hapax Legomena ($f=1$) to isolate genuine coinages from standard cliché templates.",
            "4. Calculate cliché saturation density in motivational biker ink."
        ]),
        create_cell("code", [
            "import sys",
            "sys.path.insert(0, '..')",
            "from inkcotton import LexicalRichness, ClicheDetector, SlangTokenizer",
            "import pandas as pd",
            "",
            "df = pd.read_json('../data/combined_slogans_corpus.json')",
            "tok = SlangTokenizer()",
            "print(f'Loaded {len(df)} slogans.')"
        ]),
        create_cell("markdown", [
            "### 1. TTR and Redundancy in Motivational Ink"
        ]),
        create_cell("code", [
            "alpha_slogans = df[df['category'] == 'biker_alpha']['cleaned_text']",
            "alpha_tokens = tok.tokenize_words(' '.join(alpha_slogans))",
            "",
            "ironic_slogans = df[df['category'] == 'ironic_tee']['cleaned_text']",
            "ironic_tokens = tok.tokenize_words(' '.join(ironic_slogans))",
            "",
            "print(f'Alpha Ink   - Tokens: {len(alpha_tokens)}, Types: {len(set(alpha_tokens))}, TTR: {LexicalRichness.compute_ttr(alpha_tokens)}')",
            "print(f'Ironic Tees - Tokens: {len(ironic_tokens)}, Types: {len(set(ironic_tokens))}, TTR: {LexicalRichness.compute_ttr(ironic_tokens)}')"
        ]),
        create_cell("markdown", [
            "### 2. Cliché Saturation Scoring"
        ]),
        create_cell("code", [
            "detector = ClicheDetector()",
            "report = detector.evaluate_cliche_density(alpha_tokens)",
            "print('Alpha Ink Cliché Report:', report)"
        ]),
        create_cell("markdown", [
            "### 3. Self-Verification & Autograding"
        ]),
        create_cell("code", [
            "from tests.autograde_checks import check_module_4",
            "check_module_4()"
        ])
    ]
    build_notebook(cells, "04_cliche_lexical_ttr.ipynb")


# 05_collocation_finders.ipynb
def build_nb_05():
    cells = [
        create_cell("markdown", [
            "# Project Ink & Cotton: Module 5",
            "## Collocation Traps & Fixed Semantic Tropes",
            "",
            "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/evecount/BadTattoos_NLP_workbook/blob/main/notebooks/05_collocation_finders.ipynb)",
            "",
            "### Learning Objectives",
            "1. Extract Bigrams and Trigrams from slogan corpora.",
            "2. Score multi-word expressions using Pointwise Mutual Information (PMI).",
            "3. Contrast high-frequency functional bigrams (*in the*, *to the*) against high-PMI bound phrases (*carpe diem*, *live laugh*)."
        ]),
        create_cell("code", [
            "import sys",
            "sys.path.insert(0, '..')",
            "from inkcotton import CollocationTraps, SlangTokenizer",
            "import pandas as pd",
            "",
            "df = pd.read_json('../data/combined_slogans_corpus.json')",
            "tok = SlangTokenizer()",
            "all_tokens = tok.tokenize_words(' '.join(df['cleaned_text']))",
            "print(f'Total corpus tokens: {len(all_tokens)}')"
        ]),
        create_cell("markdown", [
            "### 1. PMI Collocation Mining"
        ]),
        create_cell("code", [
            "pmi_collocations = CollocationTraps.compute_pmi(all_tokens, min_freq=2, top_n=12)",
            "pd.DataFrame(pmi_collocations)"
        ]),
        create_cell("markdown", [
            "### 2. Functional vs. Bound Idiomatic Tropes"
        ]),
        create_cell("code", [
            "grouped = CollocationTraps.contrast_functional_vs_bound(pmi_collocations)",
            "print('Bound Tropes:', [b['phrase'] for b in grouped['bound_tropes']])",
            "print('Functional Bigrams:', [f['phrase'] for f in grouped['functional_bigrams']])"
        ]),
        create_cell("markdown", [
            "### 3. Self-Verification & Autograding"
        ]),
        create_cell("code", [
            "from tests.autograde_checks import check_module_5",
            "check_module_5()"
        ])
    ]
    build_notebook(cells, "05_collocation_finders.ipynb")


# 06_spacy_ambiguity_trees.ipynb
def build_nb_06():
    cells = [
        create_cell("markdown", [
            "# Project Ink & Cotton: Module 6",
            "## Syntactic Ambiguity & Dependency Parsing (spaCy)",
            "",
            "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/evecount/BadTattoos_NLP_workbook/blob/main/notebooks/06_spacy_ambiguity_trees.ipynb)",
            "",
            "### Learning Objectives",
            "1. Analyze how punctuation omissions cause syntactic role inversions on novelty graphic tees.",
            "2. Formalize the vocative comma dilemma: *Let's eat kids* vs. *Let's eat, kids* (Direct Object vs. Vocative address).",
            "3. Inspect dependency relations (`token.dep_`, `token.head`)."
        ]),
        create_cell("code", [
            "import sys",
            "sys.path.insert(0, '..')",
            "from inkcotton import AmbiguityParser",
            "import pandas as pd",
            "",
            "parser = AmbiguityParser()",
            "print('Ambiguity parser ready.')"
        ]),
        create_cell("markdown", [
            "### 1. The Missing Comma Cannibalism Dilemma"
        ]),
        create_cell("code", [
            "pairs = [",
            "    \"Let's eat kids\",",
            "    \"Let's eat, kids\",",
            "    \"Time to cook grandma\",",
            "    \"Time to cook, grandma\"",
            "]",
            "for p in pairs:",
            "    res = parser.analyze_vocative_comma(p)",
            "    print(f\"{p:25} -> {res['hazard_warning']}\")"
        ]),
        create_cell("markdown", [
            "### 2. Self-Verification & Autograding"
        ]),
        create_cell("code", [
            "from tests.autograde_checks import check_module_6",
            "check_module_6()"
        ])
    ]
    build_notebook(cells, "06_spacy_ambiguity_trees.ipynb")


# 07_stylometric_cfd.ipynb
def build_nb_07():
    cells = [
        create_cell("markdown", [
            "# Project Ink & Cotton: Module 7",
            "## Stylometric Register Profiling via Conditional Frequency (CFD)",
            "",
            "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/evecount/BadTattoos_NLP_workbook/blob/main/notebooks/07_stylometric_cfd.ipynb)",
            "",
            "### Learning Objectives",
            "1. Construct Conditional Frequency Distributions across subcultures:",
            "   - **Category A (Alpha / Motivational Ink)**: *strength, warrior, blood, lion, king, pain*",
            "   - **Category B (Ironic / Cynical Tees)**: *tired, anxiety, coffee, nap, cancel, awkward*",
            "2. Normalize frequency counts per 1,000 words.",
            "3. Build contingency matrices to characterize thematic divergence."
        ]),
        create_cell("code", [
            "import sys",
            "sys.path.insert(0, '..')",
            "from inkcotton import RegisterProfiler",
            "import pandas as pd",
            "",
            "df = pd.read_json('../data/combined_slogans_corpus.json')",
            "cfd_raw = RegisterProfiler.build_cfd_matrix(df, category_col='category')",
            "cfd_norm = RegisterProfiler.normalize_rates_per_k(cfd_raw)",
            "print('Normalized Subculture Register Matrix (per 1,000 words):')",
            "cfd_norm"
        ]),
        create_cell("markdown", [
            "### 2. Self-Verification & Autograding"
        ]),
        create_cell("code", [
            "from tests.autograde_checks import check_module_7",
            "check_module_7()"
        ])
    ]
    build_notebook(cells, "07_stylometric_cfd.ipynb")


# 08_slogan_engine.ipynb
def build_nb_08():
    cells = [
        create_cell("markdown", [
            "# Project Ink & Cotton: Capstone Module 8",
            "## Slogan Generator & Auto-Roaster",
            "",
            "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/evecount/BadTattoos_NLP_workbook/blob/main/notebooks/08_slogan_engine.ipynb)",
            "",
            "### Learning Objectives",
            "1. Build a Category-Conditioned Markov Language Model to synthesize candidate slogans.",
            "2. Audit user-submitted tattoo and graphic tee ideas for cliché density, spelling hazards, and syntactic ambiguity.",
            "3. Generate automated, snarky roast reports."
        ]),
        create_cell("code", [
            "import sys",
            "sys.path.insert(0, '..')",
            "from inkcotton import SloganEngine, AutoRoaster",
            "import pandas as pd",
            "",
            "df = pd.read_json('../data/combined_slogans_corpus.json')",
            "engine = SloganEngine(n=2)",
            "engine.train_on_dataframe(df, category_col='category')",
            "roaster = AutoRoaster()",
            "print('Generator and AutoRoaster initialized.')"
        ]),
        create_cell("markdown", [
            "### 1. Generating Slogans via Markov LM"
        ]),
        create_cell("code", [
            "for cat in ['biker_alpha', 'ironic_tee', 'inspirational']:",
            "    slogan = engine.generate_slogan(cat, temperature=0.7, seed=42)",
            "    print(f'{cat:15}: {slogan}')"
        ]),
        create_cell("markdown", [
            "### 2. Auditing User-Submitted Slogans"
        ]),
        create_cell("code", [
            "submissions = [",
            "    'NO RAGRETS',",
            "    \"Let's eat kids!\",",
            "    'Only the strong survive with lion warrior strength',",
            "    'Running on iced coffee and awkward silence'",
            "]",
            "for sub in submissions:",
            "    audit = roaster.audit_slogan(sub)",
            "    print('--- SLOGAN AUDIT ---')",
            "    print('Slogan:         ', audit['slogan'])",
            "    print('Cliché %:       ', audit['cliche_percentage'])",
            "    print('Spelling Flags: ', audit['spelling_hazards'])",
            "    print('Syntax Hazard:  ', audit['syntax_hazard'])",
            "    print('Roast Verdict:  ', audit['roast_verdict'] + '\\n')"
        ]),
        create_cell("markdown", [
            "### 3. Self-Verification & Autograding"
        ]),
        create_cell("code", [
            "from tests.autograde_checks import check_module_8",
            "check_module_8()"
        ])
    ]
    build_notebook(cells, "08_slogan_engine.ipynb")


if __name__ == "__main__":
    build_nb_01()
    build_nb_02()
    build_nb_03()
    build_nb_04()
    build_nb_05()
    build_nb_06()
    build_nb_07()
    build_nb_08()
    print("All 8 notebooks generated successfully!")
