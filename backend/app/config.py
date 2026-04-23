import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TRAINED_MODELS_DIR = BASE_DIR / "trained_models"

# Database
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "db" / "ticketai.db"))

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "changeme-dev-only")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Model
MODEL_PATH = os.getenv("MODEL_PATH", str(TRAINED_MODELS_DIR / "model.pkl"))
EVALUATION_PATH = os.getenv("EVALUATION_PATH", str(TRAINED_MODELS_DIR / "evaluation.json"))

# CORS
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

# Dataset
DATASET_URL = (
    "https://huggingface.co/api/datasets/bitext/"
    "Bitext-customer-support-llm-chatbot-training-dataset/"
    "parquet/default/train/0.parquet"
)
DATASET_PATH = DATA_DIR / "dataset.parquet"
