"""Tests for the model evaluation utilities."""
from app.naive_bayes.evaluator import (
    compute_accuracy,
    compute_confusion_matrix,
    compute_per_class_metrics,
)


class TestComputeAccuracy:
    def test_perfect(self):
        y_true = ["A", "B", "C", "A"]
        y_pred = ["A", "B", "C", "A"]
        assert compute_accuracy(y_true, y_pred) == 1.0

    def test_zero(self):
        y_true = ["A", "B", "C"]
        y_pred = ["B", "C", "A"]
        assert compute_accuracy(y_true, y_pred) == 0.0

    def test_partial(self):
        y_true = ["A", "B", "C", "A"]
        y_pred = ["A", "B", "A", "A"]
        assert compute_accuracy(y_true, y_pred) == 0.75

    def test_empty(self):
        assert compute_accuracy([], []) == 0.0


class TestComputeConfusionMatrix:
    def test_shape(self):
        labels = ["A", "B", "C"]
        y_true = ["A", "A", "B", "C"]
        y_pred = ["A", "B", "B", "C"]
        result = compute_confusion_matrix(y_true, y_pred, labels)
        assert len(result["labels"]) == 3
        assert len(result["matrix"]) == 3
        for row in result["matrix"]:
            assert len(row) == 3

    def test_diagonal_for_perfect(self):
        labels = ["A", "B"]
        y_true = ["A", "A", "B", "B"]
        y_pred = ["A", "A", "B", "B"]
        result = compute_confusion_matrix(y_true, y_pred, labels)
        assert result["matrix"][0][0] == 2  # A→A
        assert result["matrix"][1][1] == 2  # B→B
        assert result["matrix"][0][1] == 0  # A→B
        assert result["matrix"][1][0] == 0  # B→A

    def test_off_diagonal_misclassification(self):
        labels = ["A", "B"]
        y_true = ["A", "A", "B"]
        y_pred = ["B", "A", "A"]
        result = compute_confusion_matrix(y_true, y_pred, labels)
        # A true: 1 correct (A→A), 1 wrong (A→B)
        assert result["matrix"][0][0] == 1
        assert result["matrix"][0][1] == 1
        # B true: 0 correct (B→B), 1 wrong (B→A)
        assert result["matrix"][1][0] == 1
        assert result["matrix"][1][1] == 0

    def test_row_sums_equal_support(self):
        labels = ["X", "Y", "Z"]
        y_true = ["X", "X", "Y", "Z", "Z", "Z"]
        y_pred = ["X", "Y", "Y", "X", "Z", "Z"]
        result = compute_confusion_matrix(y_true, y_pred, labels)
        # Row sums should equal the number of true samples per class
        assert sum(result["matrix"][0]) == 2  # X has 2 true samples
        assert sum(result["matrix"][1]) == 1  # Y has 1
        assert sum(result["matrix"][2]) == 3  # Z has 3


class TestComputePerClassMetrics:
    def test_perfect_classification(self):
        y_true = ["A", "A", "B", "B"]
        y_pred = ["A", "A", "B", "B"]
        results = compute_per_class_metrics(y_true, y_pred, ["A", "B"])
        for m in results:
            assert m["precision"] == 1.0
            assert m["recall"] == 1.0
            assert m["f1"] == 1.0

    def test_support_counts(self):
        y_true = ["A", "A", "A", "B", "B"]
        y_pred = ["A", "A", "B", "B", "B"]
        results = compute_per_class_metrics(y_true, y_pred, ["A", "B"])
        a_metrics = next(m for m in results if m["class"] == "A")
        b_metrics = next(m for m in results if m["class"] == "B")
        assert a_metrics["support"] == 3
        assert b_metrics["support"] == 2

    def test_precision_recall_values(self):
        # A: TP=2, FP=1, FN=1 → P=2/3, R=2/3, F1=2/3
        y_true = ["A", "A", "A", "B", "B"]
        y_pred = ["A", "A", "B", "A", "B"]
        results = compute_per_class_metrics(y_true, y_pred, ["A", "B"])
        a = next(m for m in results if m["class"] == "A")
        assert abs(a["precision"] - 2 / 3) < 1e-3
        assert abs(a["recall"] - 2 / 3) < 1e-3

    def test_all_wrong_for_one_class(self):
        y_true = ["A", "A", "B"]
        y_pred = ["B", "B", "B"]
        results = compute_per_class_metrics(y_true, y_pred, ["A", "B"])
        a = next(m for m in results if m["class"] == "A")
        assert a["precision"] == 0.0
        assert a["recall"] == 0.0
        assert a["f1"] == 0.0

    def test_result_structure(self):
        results = compute_per_class_metrics(["A"], ["A"], ["A"])
        assert len(results) == 1
        m = results[0]
        assert set(m.keys()) == {"class", "precision", "recall", "f1", "support"}
