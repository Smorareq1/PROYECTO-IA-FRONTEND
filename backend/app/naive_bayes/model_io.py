import pickle
from pathlib import Path


def save_model(model, path: str) -> None:
    """Serialize the trained model to a pickle file."""
    filepath = Path(path)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "wb") as f:
        pickle.dump(model, f)


def load_model(path: str):
    """Deserialize a trained model from a pickle file."""
    with open(path, "rb") as f:
        return pickle.load(f)
