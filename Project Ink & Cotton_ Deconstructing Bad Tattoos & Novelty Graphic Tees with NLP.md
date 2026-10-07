# ***Project Ink & Cotton: Deconstructing Bad Tattoos & Novelty Graphic Tees with NLP***

A modular, applied Python workbook lab designed to teach core text processing, spelling correction, syntactic parsing, and stylometrics through the lens of typographical errors, ironic graphic tees, and mistranslated ink.

## **Pedagogical Architecture & Pipeline**

Raw Slogan & Caption Scrapes (.csv / .json)  
   │  
   ▼  
\[Module 1: Normalization & Regex Cleaning\] ──► OCR Noise, Line Breaks, Case Variations  
   │  
   ▼  
\[Module 2: The "Ragrets" Engine\] ──► Levenshtein Distance, Edit Paths & Spellcheckers  
   │  
   ▼  
\[Module 3: Tokenization & Subword Glitches\] ──► Character vs. Word Splitting, BPE on Typo Slang  
   │  
   ▼  
\[Module 4: Lexical Richness & Slogan Saturation\] ──► TTR, Hapaxes, and Cliché Detection  
   │  
   ▼  
\[Module 5: Collocation Traps & Fixed Tropes\] ──► Bigrams, Pointwise Mutual Information (PMI)  
   │  
   ▼  
\[Module 6: Syntactic Ambiguity & spaCy Parsing\] ──► Punctuation Shifts, Modifier Attachment  
   │  
   ▼  
\[Module 7: Stylometric Register Profiling\] ──► CFD: Motivational Biker Ink vs. Irony Graphic Tees  
   │  
   ▼  
\[Module 8: Slogan Generator & Auto-Roaster\] ──► Markov Chains vs. Few-Shot Archetype Generation

## **Module Breakdown & Student Deliverables**

### **Module 1: Ingestion, OCR Glitches & Regex Normalization**

* **Core Concepts:** Regular expressions, string encoding, whitespace stripping, DRY refactoring.  
* **The Domain Task:**  
  * Slogans transcribed from photo captions or OCR often contain uneven casing (nO rEgReTs), trailing punctuation, and accidental line-break splits.  
* **Hands-on Student Exercise:** Build a reusable SloganCleaner function that normalizes punctuation and whitespace while preserving deliberate stylized capitalization (e.g., all-caps emphasis).

### **Module 2: The "Ragrets" Engine (String Distance & Spelling Correction)**

* **Core Concepts:** Levenshtein / Edit Distance (Insertions, Deletions, Substitutions), SymSpell, minimum edit distance dynamic programming.  
* **The Domain Task:**  
  * Famous tattoo blunders: *"No Ragrets"*, *"Never Don't Give Up"*, *"Sweet Pee"* (for *Sweet Pea*), *"Strenght"*.  
* **Hands-on Student Exercise:**  
  * Implement Levenshtein Distance from scratch to compute the exact minimum edit cost between tattoo strings and their intended standard English phrases.  
  * Evaluate candidate corrections based on dictionary unigram frequencies.

### **Module 3: Tokenization & Subword Splitting on Informal Slang**

* **Core Concepts:** Word-level vs. Subword-level tokenization (BPE / WordPiece), handling out-of-vocabulary (OOV) tokens.  
* **The Domain Task:**  
  * Internet-slang tees (*"bruh"*, *"yeet"*, *"delulu"*, *"smol"*) break rigid dictionary-based word tokenizers.  
* **Hands-on Student Exercise:** Run both a standard whitespace tokenizer and a Byte-Pair Encoding (BPE) subword tokenizer on modern graphic tee catchphrases; trace how subwords prevent unseen slang from collapsing into an \<UNK\> token.

### **Module 4: Lexical Diversity & Cliché Detection**

* **Core Concepts:** Types vs. Tokens ($V$ vs. $N$), Type-Token Ratio (TTR), Hapax Legomena, Zipf's Law.  
* **The Domain Task:**  
  * Motivational tattoo corpora rely on a narrow, repetitive vocabulary (*strength*, *fear*, *faith*, *warrior*, *only*, *judge*).  
* **Hands-on Student Exercise:**  
  * Calculate TTR across 1,000 tattoo slogans to quantify vocabulary redundancy.  
  * Use fdist.hapaxes() to isolate genuine anomalies or accidental coinages from standard cliché templates.

### **Module 5: Collocation Traps & Fixed Semantic Tropes**

* **Core Concepts:** Bigrams, Trigrams, Collocations, Pointwise Mutual Information (PMI), Chi-Square scoring.  
* **The Domain Task:**  
  * Fixed phrases like *"Born to Die"*, *"Live Laugh Love"*, *"Only God Can Judge Me"*, or *"I'm with Stupid"*.  
* **Hands-on Student Exercise:**  
  * Extract statistically significant collocations using NLTK's BigramCollocationFinder and PMI ranking.  
  * Contrast high-frequency functional bigrams (e.g., *"in the"*) with high-PMI bound phrases (e.g., *"carpe diem"*).

### **Module 6: Syntactic Ambiguity & Dependency Parsing (spaCy)**

* **Core Concepts:** Part-of-Speech (POS) tagging, syntactic dependency trees, structural / modifier ambiguity.  
* **The Domain Task:**  
  * Punctuation mistakes that invert meaning on graphic shirts:  
    * *"Let's eat kids"* vs. *"Let's eat, kids"* (Direct object vs. vocative noun).  
    * *"Eats shoots and leaves"* (Verb sequence vs. plant noun phrase).  
* **Hands-on Student Exercise:** Pass ambiguous slogan pairs into spacy.load("en\_core\_web\_sm"); extract and plot the dependency trees (token.dep\_, token.head) to illustrate how a single comma shifts a verb from transitive action to an address.

### **Module 7: Stylometric Register Profiling via Conditional Frequency (CFD)**

* **Core Concepts:** ConditionalFreqDist, contingency tables, stylometric register comparisons.  
* **The Domain Task:**  
  * Compare the semantic vocabulary of two distinct sub-genres:  
    * **Category A (Alpha / Motivational Ink):** *strength, warrior, blood, lion, king, pain*.  
    * **Category B (Ironic / Cynical Tees):** *tired, anxiety, coffee, nap, cancel, awkward*.  
* **Hands-on Student Exercise:** Build an NLTK ConditionalFreqDist conditioned on category, generate a comparative matrix table, and plot modal/thematic distribution across the two subcultures.

### **Module 8: Slogan Generator & Auto-Roaster (Capstone)**

* **Core Concepts:** $N$\-gram Language Modeling, Markov Chains, prompt-conditioned sampling.  
* **The Domain Task:**  
  * Build a dual generator:  
    1. A Markov generator that synthesizes new pseudo-motivational tattoo slogans from historical cliché bigrams.  
    2. A rule-based parser that scores user-submitted slogans on cliché probability and flags potential syntactic ambiguity or spelling hazards.  
* **Hands-on Student Exercise:** Generate 10 candidate tattoo slogans using trigram transition probabilities and evaluate their lexical richness (TTR) against genuine human submissions.

## **Student Repository Structure**

project-ink-and-cotton/  
│  
├── README.md                          \# Project overview and learning milestones  
├── environment.yml                    \# Conda environment file  
│  
├── data/  
│   ├── tattoos\_raw.csv                \# Scraped tattoo quotes & captions  
│   ├── graphic\_tees\_raw.csv           \# Slogan t-shirt inventory titles  
│   └── dictionary\_reference.txt       \# English reference vocabulary  
│  
├── notebooks/  
│   ├── 01\_ocr\_slogan\_cleaner.ipynb    \# Module 1  
│   ├── 02\_levenshtein\_ragrets.ipynb   \# Module 2  
│   ├── 03\_subword\_slang\_tokens.ipynb  \# Module 3  
│   ├── 04\_cliche\_lexical\_ttr.ipynb    \# Module 4  
│   ├── 05\_collocation\_finders.ipynb   \# Module 5  
│   ├── 06\_spacy\_ambiguity\_trees.ipynb \# Module 6  
│   ├── 07\_stylometric\_cfd.ipynb       \# Module 7  
│   └── 08\_slogan\_engine.ipynb         \# Capstone Module 8  
│  
└── tests/  
    └── test\_cleaning\_and\_edit.py      \# Autograding checks

That gives you two complete, production-grade pedagogical workbook plans banked for later.  
Back to the cram schedule: click to the next screen on Brightspace—what topic is up next?