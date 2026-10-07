"""
Project Ink & Cotton: Deconstructing Bad Tattoos & Novelty Graphic Tees with NLP
================================================================================
A modular educational NLP package analyzing typo-riddled ink, ironic graphic tees,
string distance, syntactic ambiguity, and Markov slogan generation.
"""

__version__ = "0.1.0"
__author__ = "Gwendalynn Lim"

from inkcotton.cleaner import SloganCleaner
from inkcotton.spellchecker import LevenshteinDistance, RagretsEngine
from inkcotton.tokenizer import SlangTokenizer
from inkcotton.metrics import LexicalRichness, ClicheDetector
from inkcotton.collocations import CollocationTraps
from inkcotton.syntax import AmbiguityParser
from inkcotton.stylometrics import RegisterProfiler
from inkcotton.roaster import SloganEngine, AutoRoaster

__all__ = [
    "SloganCleaner",
    "LevenshteinDistance",
    "RagretsEngine",
    "SlangTokenizer",
    "LexicalRichness",
    "ClicheDetector",
    "CollocationsTraps",
    "AmbiguityParser",
    "RegisterProfiler",
    "SloganEngine",
    "AutoRoaster",
]
