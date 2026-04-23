"""
Model evaluation utilities �� implemented from scratch.
K-Folds cross validation, confusion matrix, per-class metrics.
"""
import random
from collections import defaultdict

from app.naive_bayes.classifier import NaiveBayesMultinomial


def k_fold_cross_validation(
    documents: list[str],
    labels: list[str],
    k: int = 5,
    alpha: float = 1.0,
    seed: int = 42,
) -> dict:
    """
    Manual K-Fold cross validation.

    Shuffles data, splits into k folds, trains k models,
    and averages metrics across folds.

    Returns a KFoldReport dict matching the frontend contract.
    """
    n = len(documents)
    indices = list(range(n))
    random.seed(seed)
    random.shuffle(indices)

    # Split indices into k roughly equal folds
    fold_size = n // k
    folds_indices = []
    for i in range(k):
        start = i * fold_size
        end = start + fold_size if i < k - 1 else n
        folds_indices.append(indices[start:end])

    fold_results = []

    for fold_idx in range(k):
        print(f"  Fold {fold_idx + 1}/{k}...")

        # Test fold = fold_idx, train on the rest
        test_indices = folds_indices[fold_idx]
        train_indices = []
        for j in range(k):
            if j != fold_idx:
                train_indices.extend(folds_indices[j])

        train_docs = [documents[i] for i in train_indices]
        train_labels = [labels[i] for i in train_indices]
        test_docs = [documents[i] for i in test_indices]
        test_labels = [labels[i] for i in test_indices]

        # Train a fresh model on this fold
        model = NaiveBayesMultinomial(alpha=alpha)
        model.fit(train_docs, train_labels)

        # Predict on test set
        predictions = [model.predict_class(doc) for doc in test_docs]

        # Compute metrics for this fold
        accuracy = compute_accuracy(test_labels, predictions)
        per_class = compute_per_class_metrics(test_labels, predictions, model.classes)
        macro_f1 = sum(m["f1"] for m in per_class) / len(per_class)

        fold_results.append({
            "fold": fold_idx + 1,
            "accuracy": round(accuracy, 4),
            "macro_f1": round(macro_f1, 4),
            "per_class": per_class,
        })

        print(f"    Accuracy: {accuracy:.4f}, Macro F1: {macro_f1:.4f}")

    # Compute mean and std across folds
    accuracies = [f["accuracy"] for f in fold_results]
    macro_f1s = [f["macro_f1"] for f in fold_results]

    mean_acc = sum(accuracies) / k
    mean_f1 = sum(macro_f1s) / k
    std_acc = (sum((a - mean_acc) ** 2 for a in accuracies) / k) ** 0.5
    std_f1 = (sum((f - mean_f1) ** 2 for f in macro_f1s) / k) ** 0.5

    return {
        "k": k,
        "folds": fold_results,
        "mean": {"accuracy": round(mean_acc, 4), "macro_f1": round(mean_f1, 4)},
        "std": {"accuracy": round(std_acc, 4), "macro_f1": round(std_f1, 4)},
    }


def compute_confusion_matrix(
    y_true: list[str], y_pred: list[str], labels: list[str]
) -> dict:
    """
    Build confusion matrix.
    matrix[i][j] = number of samples with true label labels[i] predicted as labels[j].
    """
    label_to_idx = {label: i for i, label in enumerate(labels)}
    n = len(labels)
    matrix = [[0] * n for _ in range(n)]

    for true, pred in zip(y_true, y_pred):
        i = label_to_idx.get(true)
        j = label_to_idx.get(pred)
        if i is not None and j is not None:
            matrix[i][j] += 1

    return {"labels": labels, "matrix": matrix}


def compute_accuracy(y_true: list[str], y_pred: list[str]) -> float:
    """Global accuracy: correct / total."""
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    return correct / len(y_true) if y_true else 0.0


def compute_per_class_metrics(
    y_true: list[str], y_pred: list[str], classes: list[str]
) -> list[dict]:
    """
    Compute precision, recall, F1-score and support for each class.
    """
    # Count TP, FP, FN per class
    tp = defaultdict(int)
    fp = defaultdict(int)
    fn = defaultdict(int)
    support = defaultdict(int)

    for true, pred in zip(y_true, y_pred):
        support[true] += 1
        if true == pred:
            tp[true] += 1
        else:
            fp[pred] += 1
            fn[true] += 1

    results = []
    for cls in classes:
        precision = tp[cls] / (tp[cls] + fp[cls]) if (tp[cls] + fp[cls]) > 0 else 0.0
        recall = tp[cls] / (tp[cls] + fn[cls]) if (tp[cls] + fn[cls]) > 0 else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )
        results.append({
            "class": cls,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "support": support[cls],
        })

    return results
