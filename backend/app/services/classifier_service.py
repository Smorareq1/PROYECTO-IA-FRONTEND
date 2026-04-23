"""
Classifier service — wraps the loaded model for API use.
"""
from app.naive_bayes.classifier import NaiveBayesMultinomial


def predict(model: NaiveBayesMultinomial, text: str) -> dict:
    """Run prediction on text using the loaded model."""
    return model.predict(text)


def get_top_words(model: NaiveBayesMultinomial, category: str, n: int = 20) -> list[dict]:
    """Get top discriminative words for a category."""
    return model.get_top_words(category, n)
