"""
Train the Naïve Bayes model on the Bitext dataset.
Runs full training + K-Fold evaluation + saves artifacts.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from app.config import DATASET_PATH, MODEL_PATH, EVALUATION_PATH
from app.naive_bayes.classifier import NaiveBayesMultinomial
from app.naive_bayes.evaluator import (
    k_fold_cross_validation,
    compute_confusion_matrix,
    compute_per_class_metrics,
    compute_accuracy,
)
from app.naive_bayes.model_io import save_model


def main():
    # 1. Load dataset
    print("=" * 60)
    print("TRAINING PIPELINE — Naïve Bayes Multinomial")
    print("=" * 60)

    if not DATASET_PATH.exists():
        print(f"ERROR: Dataset not found at {DATASET_PATH}")
        print("Run 'python -m scripts.download_dataset' first.")
        sys.exit(1)

    print(f"\n1. Loading dataset from {DATASET_PATH}...")
    df = pd.read_parquet(DATASET_PATH)
    documents = df["instruction"].tolist()
    labels = df["category"].tolist()
    print(f"   {len(documents)} documents, {len(set(labels))} categories")

    # 2. Train the final model on ALL data
    print("\n2. Training final model on full dataset...")
    model = NaiveBayesMultinomial(alpha=1.0)
    model.fit(documents, labels)
    print(f"   Vocabulary size: {model.vocab_size}")
    print(f"   Classes: {model.classes}")

    # 3. Save the trained model
    print(f"\n3. Saving model to {MODEL_PATH}...")
    Path(MODEL_PATH).parent.mkdir(parents=True, exist_ok=True)
    save_model(model, MODEL_PATH)
    model_size = Path(MODEL_PATH).stat().st_size / 1024 / 1024
    print(f"   Model size: {model_size:.1f} MB")

    # 4. Evaluate on full dataset (train accuracy — for reference)
    print("\n4. Evaluating on full dataset (train metrics)...")
    all_preds = [model.predict_class(doc) for doc in documents]
    train_accuracy = compute_accuracy(labels, all_preds)
    train_per_class = compute_per_class_metrics(labels, all_preds, model.classes)
    train_macro_f1 = sum(m["f1"] for m in train_per_class) / len(train_per_class)
    print(f"   Train Accuracy: {train_accuracy:.4f}")
    print(f"   Train Macro F1: {train_macro_f1:.4f}")

    # 5. K-Fold Cross Validation
    print(f"\n5. Running 5-Fold Cross Validation...")
    kfold_report = k_fold_cross_validation(documents, labels, k=5, alpha=1.0)
    print(f"   Mean Accuracy: {kfold_report['mean']['accuracy']:.4f} ± {kfold_report['std']['accuracy']:.4f}")
    print(f"   Mean Macro F1: {kfold_report['mean']['macro_f1']:.4f} ± {kfold_report['std']['macro_f1']:.4f}")

    # 6. Confusion matrix on full dataset
    print("\n6. Computing confusion matrix...")
    confusion = compute_confusion_matrix(labels, all_preds, model.classes)

    # 7. Save evaluation results
    evaluation = {
        "model_info": {
            "version": "1.0.0",
            "trained_at": model.trained_at,
            "vocab_size": model.vocab_size,
            "doc_count": model.doc_count,
            "classes": model.classes,
        },
        "metrics": {
            "accuracy": round(train_accuracy, 4),
            "macro_f1": round(train_macro_f1, 4),
            "per_class": train_per_class,
        },
        "confusion_matrix": confusion,
        "kfold_report": kfold_report,
    }

    print(f"\n7. Saving evaluation to {EVALUATION_PATH}...")
    Path(EVALUATION_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(EVALUATION_PATH, "w") as f:
        json.dump(evaluation, f, indent=2)

    # 8. Print per-class metrics table
    print("\n" + "=" * 60)
    print("PER-CLASS METRICS (full dataset)")
    print("=" * 60)
    print(f"{'Class':<16} {'Precision':>10} {'Recall':>10} {'F1':>10} {'Support':>10}")
    print("-" * 56)
    for m in train_per_class:
        print(f"{m['class']:<16} {m['precision']:>10.4f} {m['recall']:>10.4f} {m['f1']:>10.4f} {m['support']:>10}")
    print("-" * 56)
    print(f"{'Accuracy':<16} {'':<10} {'':<10} {train_accuracy:>10.4f} {len(labels):>10}")
    print(f"{'Macro F1':<16} {'':<10} {'':<10} {train_macro_f1:>10.4f}")

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
