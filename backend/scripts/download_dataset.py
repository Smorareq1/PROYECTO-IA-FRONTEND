"""
Download the Bitext Customer Support dataset from HuggingFace via HTTP.
Uses the Parquet API endpoint for faster downloads.
No HuggingFace library used (restricted by project rules).
"""
import sys
import urllib.request
from pathlib import Path

# Add parent to path so we can import app.config
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import DATASET_URL, DATASET_PATH, DATA_DIR


def download_dataset():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if DATASET_PATH.exists():
        print(f"Dataset already exists at {DATASET_PATH}")
        return

    print(f"Downloading dataset from HuggingFace (Parquet)...")
    print(f"URL: {DATASET_URL}")
    print(f"Destination: {DATASET_PATH}")

    try:
        urllib.request.urlretrieve(DATASET_URL, DATASET_PATH)
        print(f"Download complete. File size: {DATASET_PATH.stat().st_size / 1024 / 1024:.1f} MB")
    except Exception as e:
        print(f"ERROR: Failed to download dataset: {e}")
        print()
        print("Manual download instructions:")
        print("1. Go to: https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset")
        print("2. Download the Parquet file from the 'Files and versions' tab")
        print(f"3. Save it to: {DATASET_PATH}")
        sys.exit(1)

    # Verify the download
    import pandas as pd
    df = pd.read_parquet(DATASET_PATH)
    print(f"Dataset loaded: {len(df)} rows, columns: {list(df.columns)}")
    print(f"Categories found: {sorted(df['category'].unique())}")
    print(f"Samples per category:")
    print(df['category'].value_counts().to_string())


if __name__ == "__main__":
    download_dataset()
