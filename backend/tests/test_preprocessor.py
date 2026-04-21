"""Tests for the text preprocessing pipeline."""
from app.naive_bayes.preprocessor import preprocess, tokenize_only


class TestPreprocess:
    def test_removes_placeholders(self):
        text = "I need help with {{Order Number}} and {{Account ID}}"
        tokens = preprocess(text)
        for t in tokens:
            assert "{{" not in t
            assert "}}" not in t
            assert "order" not in t.lower() or t != "order"  # may appear stemmed

    def test_lowercases(self):
        tokens = preprocess("HELLO WORLD")
        for t in tokens:
            assert t == t.lower()

    def test_removes_stopwords(self):
        tokens = preprocess("I am the best customer in the world")
        assert "i" not in tokens
        assert "am" not in tokens
        assert "the" not in tokens
        assert "in" not in tokens

    def test_stems_words(self):
        tokens = preprocess("running cancellation payments delivered")
        # SnowballStemmer should reduce these
        assert "run" in tokens or "running" not in tokens
        assert "cancel" in tokens or "cancellation" not in tokens

    def test_removes_punctuation(self):
        tokens = preprocess("Hello! How are you? I'm fine, thanks.")
        for t in tokens:
            assert all(c.isalpha() for c in t)

    def test_empty_string(self):
        assert preprocess("") == []

    def test_only_stopwords(self):
        tokens = preprocess("I am the a an is are was")
        assert tokens == []

    def test_only_placeholders(self):
        tokens = preprocess("{{Name}} {{Email}}")
        assert tokens == []

    def test_real_ticket_text(self):
        text = "I want to cancel my subscription and get a full refund immediately"
        tokens = preprocess(text)
        assert len(tokens) > 0
        # Key content words should survive (possibly stemmed)
        token_str = " ".join(tokens)
        assert "cancel" in token_str or "subscript" in token_str


class TestTokenizeOnly:
    def test_no_stemming(self):
        tokens = tokenize_only("cancellation payments delivered")
        # Without stemming, full words should appear
        assert "cancellation" in tokens
        assert "payments" in tokens
        assert "delivered" in tokens

    def test_removes_stopwords(self):
        tokens = tokenize_only("I am the best customer")
        assert "i" not in tokens
        assert "am" not in tokens
        assert "the" not in tokens
        assert "customer" in tokens

    def test_removes_placeholders(self):
        tokens = tokenize_only("Help with {{Order Number}} please")
        for t in tokens:
            assert "{{" not in t
