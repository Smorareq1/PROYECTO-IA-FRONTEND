"""Tests for the /api/v1/classifier endpoints."""


class TestPredict:
    def test_predict_success(self, client):
        resp = client.post("/api/v1/classifier/predict", json={
            "text": "I want to cancel my subscription right now",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "category" in data
        assert "confidences" in data
        assert "log_probs" in data
        assert "tokens" in data
        assert "processing_ms" in data

    def test_predict_response_shape(self, client):
        resp = client.post("/api/v1/classifier/predict", json={
            "text": "Please refund my order payment",
        })
        data = resp.json()
        # 11 categories in confidences
        assert len(data["confidences"]) == 11
        assert len(data["log_probs"]) == 11
        # Confidences sum to ~1
        total = sum(data["confidences"].values())
        assert abs(total - 1.0) < 0.01
        # Tokens is a non-empty list
        assert isinstance(data["tokens"], list)
        assert len(data["tokens"]) > 0
        # Processing time is positive
        assert data["processing_ms"] >= 0

    def test_predict_empty_text(self, client):
        resp = client.post("/api/v1/classifier/predict", json={"text": "   "})
        assert resp.status_code == 422

    def test_predict_known_categories(self, client):
        """Test that well-known texts classify correctly."""
        cases = [
            ("terminate my contract and stop billing me", "CANCEL"),
            ("I need a refund for the wrong charge", "REFUND"),
        ]
        for text, expected in cases:
            resp = client.post("/api/v1/classifier/predict", json={"text": text})
            assert resp.status_code == 200
            assert resp.json()["category"] == expected, f"Failed for: {text}"
