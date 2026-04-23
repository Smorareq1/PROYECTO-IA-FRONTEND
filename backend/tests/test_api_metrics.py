"""Tests for the /api/v1/model endpoints."""


class TestModelInfo:
    def test_model_info(self, client):
        resp = client.get("/api/v1/model/info")
        assert resp.status_code == 200
        data = resp.json()
        assert "version" in data
        assert "trained_at" in data
        assert "vocab_size" in data
        assert isinstance(data["vocab_size"], int)
        assert data["vocab_size"] > 0
        assert "doc_count" in data
        assert data["doc_count"] == 26872  # Bitext dataset size
        assert "classes" in data
        assert len(data["classes"]) == 11


class TestModelMetrics:
    def test_metrics(self, client):
        resp = client.get("/api/v1/model/metrics")
        assert resp.status_code == 200
        data = resp.json()
        assert "accuracy" in data
        assert "macro_f1" in data
        assert "per_class" in data
        assert 0 < data["accuracy"] <= 1.0
        assert 0 < data["macro_f1"] <= 1.0
        assert len(data["per_class"]) == 11

    def test_per_class_structure(self, client):
        resp = client.get("/api/v1/model/metrics")
        for m in resp.json()["per_class"]:
            assert "class" in m
            assert "precision" in m
            assert "recall" in m
            assert "f1" in m
            assert "support" in m
            assert 0 <= m["precision"] <= 1.0
            assert 0 <= m["recall"] <= 1.0
            assert 0 <= m["f1"] <= 1.0
            assert m["support"] > 0


class TestConfusionMatrix:
    def test_confusion_matrix(self, client):
        resp = client.get("/api/v1/model/confusion-matrix")
        assert resp.status_code == 200
        data = resp.json()
        assert "labels" in data
        assert "matrix" in data
        assert len(data["labels"]) == 11
        assert len(data["matrix"]) == 11
        for row in data["matrix"]:
            assert len(row) == 11
            for val in row:
                assert isinstance(val, int)
                assert val >= 0


class TestKFolds:
    def test_kfolds_report(self, client):
        resp = client.get("/api/v1/model/kfolds")
        assert resp.status_code == 200
        data = resp.json()
        assert data["k"] == 5
        assert len(data["folds"]) == 5
        assert "mean" in data
        assert "std" in data
        assert "accuracy" in data["mean"]
        assert "macro_f1" in data["mean"]

    def test_fold_structure(self, client):
        resp = client.get("/api/v1/model/kfolds")
        for fold in resp.json()["folds"]:
            assert "fold" in fold
            assert "accuracy" in fold
            assert "macro_f1" in fold
            assert "per_class" in fold
            assert 0 < fold["accuracy"] <= 1.0


class TestTopWords:
    def test_top_words(self, client):
        resp = client.get("/api/v1/model/top-words?class=CANCEL&n=10")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 10

    def test_top_words_structure(self, client):
        resp = client.get("/api/v1/model/top-words?class=REFUND&n=5")
        for w in resp.json():
            assert "word" in w
            assert "weight" in w
            assert isinstance(w["word"], str)
            assert isinstance(w["weight"], float)

    def test_top_words_unknown_category(self, client):
        resp = client.get("/api/v1/model/top-words?class=NONEXISTENT&n=5")
        assert resp.status_code == 404

    def test_top_words_all_categories(self, client):
        categories = [
            "ACCOUNT", "CANCEL", "CONTACT", "DELIVERY", "FEEDBACK",
            "INVOICE", "ORDER", "PAYMENT", "REFUND", "SHIPPING", "SUBSCRIPTION",
        ]
        for cat in categories:
            resp = client.get(f"/api/v1/model/top-words?class={cat}&n=3")
            assert resp.status_code == 200
            assert len(resp.json()) == 3
