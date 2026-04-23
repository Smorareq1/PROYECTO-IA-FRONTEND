"""Tests for the from-scratch Naïve Bayes Multinomial classifier."""
import math

import pytest

from app.naive_bayes.classifier import NaiveBayesMultinomial


@pytest.fixture(scope="module")
def small_model():
    """Train a small model on a few known samples for deterministic testing."""
    docs = [
        "I want to cancel my subscription",
        "Please cancel my account immediately",
        "Cancel the service and close everything",
        "I need a refund for my payment",
        "Refund my money the charge was wrong",
        "I was charged twice please refund",
        "How do I contact customer support",
        "I need to reach someone by phone",
        "What is the phone number for support",
    ]
    labels = [
        "CANCEL", "CANCEL", "CANCEL",
        "REFUND", "REFUND", "REFUND",
        "CONTACT", "CONTACT", "CONTACT",
    ]
    model = NaiveBayesMultinomial(alpha=1.0)
    model.fit(docs, labels)
    return model


class TestFit:
    def test_learns_classes(self, small_model):
        assert sorted(small_model.classes) == ["CANCEL", "CONTACT", "REFUND"]

    def test_builds_vocabulary(self, small_model):
        assert small_model.vocab_size > 0
        assert isinstance(small_model.vocab, list)

    def test_doc_count(self, small_model):
        assert small_model.doc_count == 9

    def test_log_priors_are_valid(self, small_model):
        # 3 classes with 3 docs each → equal priors
        for cls in small_model.classes:
            assert small_model.log_prior[cls] == pytest.approx(math.log(3 / 9), abs=1e-6)

    def test_log_likelihoods_exist_for_all_classes(self, small_model):
        for cls in small_model.classes:
            assert cls in small_model.log_likelihood
            assert "__UNSEEN__" in small_model.log_likelihood[cls]

    def test_laplace_smoothing_no_zero_probs(self, small_model):
        for cls in small_model.classes:
            for word in small_model.vocab:
                log_prob = small_model.log_likelihood[cls][word]
                # Log of a positive number is finite
                assert math.isfinite(log_prob)
                # Probability should be > 0 (log < 0)
                assert log_prob < 0

    def test_trained_at_set(self, small_model):
        assert small_model.trained_at is not None


class TestPredict:
    def test_returns_expected_keys(self, small_model):
        result = small_model.predict("cancel my subscription")
        assert set(result.keys()) == {"category", "confidences", "log_probs", "tokens", "processing_ms"}

    def test_predicts_cancel(self, small_model):
        result = small_model.predict("I want to cancel my subscription now")
        assert result["category"] == "CANCEL"

    def test_predicts_refund(self, small_model):
        result = small_model.predict("Please refund my payment immediately")
        assert result["category"] == "REFUND"

    def test_confidences_sum_to_one(self, small_model):
        result = small_model.predict("cancel my account")
        total = sum(result["confidences"].values())
        assert total == pytest.approx(1.0, abs=1e-4)

    def test_confidences_all_classes_present(self, small_model):
        result = small_model.predict("some text")
        assert set(result["confidences"].keys()) == set(small_model.classes)

    def test_log_probs_are_negative(self, small_model):
        result = small_model.predict("cancel")
        for lp in result["log_probs"].values():
            assert lp < 0

    def test_tokens_is_list(self, small_model):
        result = small_model.predict("cancel my subscription")
        assert isinstance(result["tokens"], list)
        assert len(result["tokens"]) > 0

    def test_processing_ms_is_positive(self, small_model):
        result = small_model.predict("test")
        assert result["processing_ms"] >= 0

    def test_deterministic(self, small_model):
        r1 = small_model.predict("cancel subscription")
        r2 = small_model.predict("cancel subscription")
        assert r1["category"] == r2["category"]
        assert r1["confidences"] == r2["confidences"]


class TestPredictClass:
    def test_returns_string(self, small_model):
        result = small_model.predict_class("cancel my account")
        assert isinstance(result, str)
        assert result in small_model.classes

    def test_matches_predict(self, small_model):
        text = "I need a refund for my order"
        assert small_model.predict_class(text) == small_model.predict(text)["category"]


class TestGetTopWords:
    def test_returns_list(self, small_model):
        words = small_model.get_top_words("CANCEL", n=5)
        assert isinstance(words, list)
        assert len(words) <= 5

    def test_word_structure(self, small_model):
        words = small_model.get_top_words("CANCEL", n=5)
        for w in words:
            assert "word" in w
            assert "weight" in w
            assert isinstance(w["word"], str)
            assert isinstance(w["weight"], float)

    def test_sorted_descending(self, small_model):
        words = small_model.get_top_words("CANCEL", n=10)
        weights = [w["weight"] for w in words]
        assert weights == sorted(weights, reverse=True)

    def test_unknown_category(self, small_model):
        assert small_model.get_top_words("NONEXISTENT") == []


class TestRealModel:
    """Tests using the full trained model (skipped if model not available)."""

    def test_predicts_known_samples(self, trained_model):
        cases = [
            ("terminate my contract and stop billing me", "CANCEL"),
            ("I need a refund for my order", "REFUND"),
            ("What are your shipping rates?", "SHIPPING"),
            ("I need to update my account email", "ACCOUNT"),
        ]
        for text, expected in cases:
            result = trained_model.predict(text)
            assert result["category"] == expected, f"Expected {expected} for '{text}', got {result['category']}"

    def test_all_11_classes(self, trained_model):
        assert len(trained_model.classes) == 11
        expected = {"ACCOUNT", "CANCEL", "CONTACT", "DELIVERY", "FEEDBACK",
                    "INVOICE", "ORDER", "PAYMENT", "REFUND", "SHIPPING", "SUBSCRIPTION"}
        assert set(trained_model.classes) == expected
