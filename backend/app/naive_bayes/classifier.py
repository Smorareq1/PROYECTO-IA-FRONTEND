"""
Naïve Bayes Multinomial classifier — implemented from scratch.
No scikit-learn, TensorFlow, PyTorch, or any ML library used.
"""
import math
import time
from collections import Counter, defaultdict

import numpy as np

from app.naive_bayes.preprocessor import preprocess, tokenize_only


class NaiveBayesMultinomial:
    """
    Multinomial Naïve Bayes classifier with:
    - Bag of Words vocabulary
    - Laplace Smoothing (alpha=1)
    - Log-sum inference to avoid underflow
    """

    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha  # Laplace smoothing parameter

        # Learned parameters (populated by fit())
        self.classes: list[str] = []
        self.vocab: list[str] = []
        self.vocab_size: int = 0
        self.doc_count: int = 0

        # Log prior: log P(class)
        self.log_prior: dict[str, float] = {}

        # Log likelihood: log P(word | class) with Laplace smoothing
        # Stored as {class: {word: log_prob}}
        self.log_likelihood: dict[str, dict[str, float]] = {}

        # Word counts per class (for top-words feature)
        self.word_counts_per_class: dict[str, Counter] = {}

        # Class counts
        self.class_counts: dict[str, int] = {}

        # Metadata
        self.trained_at: str | None = None

    def fit(self, documents: list[str], labels: list[str]) -> "NaiveBayesMultinomial":
        """
        Train the model on preprocessed documents.

        Args:
            documents: Raw text documents (preprocessing happens internally)
            labels: Category label for each document
        """
        import datetime

        self.doc_count = len(documents)
        self.classes = sorted(set(labels))

        # Count documents per class for prior
        self.class_counts = Counter(labels)

        # Preprocess all documents
        tokenized_docs = [preprocess(doc) for doc in documents]

        # Build vocabulary from all tokens
        all_tokens: set[str] = set()
        for tokens in tokenized_docs:
            all_tokens.update(tokens)
        self.vocab = sorted(all_tokens)
        self.vocab_size = len(self.vocab)

        # Count word occurrences per class
        self.word_counts_per_class = {cls: Counter() for cls in self.classes}
        total_words_per_class: dict[str, int] = defaultdict(int)

        for tokens, label in zip(tokenized_docs, labels):
            self.word_counts_per_class[label].update(tokens)
            total_words_per_class[label] += len(tokens)

        # Compute log priors: log P(class) = log(count(class) / total_docs)
        for cls in self.classes:
            self.log_prior[cls] = math.log(self.class_counts[cls] / self.doc_count)

        # Compute log likelihoods with Laplace smoothing:
        # log P(word | class) = log((count(word, class) + alpha) / (total_words_in_class + alpha * vocab_size))
        self.log_likelihood = {}
        for cls in self.classes:
            self.log_likelihood[cls] = {}
            denominator = total_words_per_class[cls] + self.alpha * self.vocab_size

            for word in self.vocab:
                count = self.word_counts_per_class[cls].get(word, 0)
                self.log_likelihood[cls][word] = math.log(
                    (count + self.alpha) / denominator
                )

            # Store default log-prob for unseen words (words not in vocab)
            self.log_likelihood[cls]["__UNSEEN__"] = math.log(
                self.alpha / denominator
            )

        self.trained_at = datetime.datetime.now().isoformat()
        return self

    def predict(self, text: str) -> dict:
        """
        Classify a single text document.

        Returns dict with:
            category: predicted class (argmax)
            confidences: {class: probability} (softmax of log-probs)
            log_probs: {class: raw log-probability}
            tokens: list of preprocessed tokens
            processing_ms: inference time in milliseconds
        """
        start = time.perf_counter()

        tokens = preprocess(text)
        display_tokens = tokenize_only(text)

        # Compute log P(class | document) for each class
        # log P(class | doc) ∝ log P(class) + Σ log P(word | class)
        log_probs: dict[str, float] = {}

        for cls in self.classes:
            score = self.log_prior[cls]
            for token in tokens:
                if token in self.log_likelihood[cls]:
                    score += self.log_likelihood[cls][token]
                else:
                    score += self.log_likelihood[cls]["__UNSEEN__"]
            log_probs[cls] = score

        # Predicted class = argmax
        predicted = max(log_probs, key=log_probs.get)

        # Convert log-probs to probabilities via softmax
        confidences = self._softmax(log_probs)

        elapsed_ms = (time.perf_counter() - start) * 1000

        return {
            "category": predicted,
            "confidences": confidences,
            "log_probs": log_probs,
            "tokens": display_tokens,
            "processing_ms": round(elapsed_ms, 2),
        }

    def predict_class(self, text: str) -> str:
        """Predict just the class label (used during evaluation)."""
        tokens = preprocess(text)
        best_class = None
        best_score = float("-inf")

        for cls in self.classes:
            score = self.log_prior[cls]
            for token in tokens:
                if token in self.log_likelihood[cls]:
                    score += self.log_likelihood[cls][token]
                else:
                    score += self.log_likelihood[cls]["__UNSEEN__"]

            if score > best_score:
                best_score = score
                best_class = cls

        return best_class

    def get_top_words(self, category: str, n: int = 20) -> list[dict]:
        """
        Get top-N most discriminative words for a category.
        Uses the log-likelihood ratio: log P(word|class) - avg(log P(word|other_classes))
        """
        if category not in self.classes:
            return []

        word_scores = []
        other_classes = [c for c in self.classes if c != category]

        for word in self.vocab:
            score_in_class = self.log_likelihood[category].get(word, self.log_likelihood[category]["__UNSEEN__"])
            avg_others = np.mean([
                self.log_likelihood[c].get(word, self.log_likelihood[c]["__UNSEEN__"])
                for c in other_classes
            ])
            # Discriminative score: how much more likely this word is in this class vs others
            discriminative = score_in_class - avg_others
            word_scores.append({"word": word, "weight": round(float(discriminative), 4)})

        # Sort by weight descending, take top N
        word_scores.sort(key=lambda x: x["weight"], reverse=True)
        return word_scores[:n]

    @staticmethod
    def _softmax(log_probs: dict[str, float]) -> dict[str, float]:
        """Convert log-probabilities to normalized probabilities via softmax."""
        # Shift by max for numerical stability
        max_val = max(log_probs.values())
        exp_vals = {cls: math.exp(lp - max_val) for cls, lp in log_probs.items()}
        total = sum(exp_vals.values())
        return {cls: round(val / total, 6) for cls, val in exp_vals.items()}
