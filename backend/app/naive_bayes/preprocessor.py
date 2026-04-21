"""
Text preprocessing pipeline for the Naïve Bayes classifier.
"""
import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

# Ensure NLTK data is available
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)

STOP_WORDS = set(stopwords.words("english"))
STEMMER = SnowballStemmer("english")

# Regex to remove {{Placeholder}} patterns from the Bitext dataset
PLACEHOLDER_RE = re.compile(r"\{\{.*?\}\}")


def preprocess(text: str) -> list[str]:
    """
    Full preprocessing pipeline:
    1. Remove {{Placeholder}} patterns
    2. Lowercase
    3. Remove punctuation
    4. Tokenize with NLTK
    5. Remove stopwords
    6. Stem with Snowball stemmer
    Returns list of stemmed tokens.
    """
    # Remove placeholders like {{Order Number}}, {{Account ID}}
    text = PLACEHOLDER_RE.sub("", text)

    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords and non-alphabetic tokens, then stem
    processed = [
        STEMMER.stem(token)
        for token in tokens
        if token.isalpha() and token not in STOP_WORDS
    ]

    return processed


def tokenize_only(text: str) -> list[str]:
    """Tokenize without stemming — useful for showing tokens in API response."""
    text = PLACEHOLDER_RE.sub("", text)
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    return [t for t in tokens if t.isalpha() and t not in STOP_WORDS]
