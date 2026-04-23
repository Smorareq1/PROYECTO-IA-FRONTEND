# TicketAI Backend

Python/FastAPI backend serving a **from-scratch Naïve Bayes Multinomial classifier** trained on the [Bitext Customer Support dataset](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset) (26,872 samples, 11 categories).

## Requirements

- Python 3.11+
- NLTK data (downloaded automatically on first run)

## Setup

```bash
cd backend
pip install -r requirements.txt
```

## Dataset

Download the Bitext dataset:

```bash
python -m scripts.download_dataset
```

This saves `data/dataset.csv` (~18 MB, 26,872 rows). If the download fails, manually download from HuggingFace and place the CSV in `backend/data/dataset.csv`.

## Training

Train the Naïve Bayes model and run K-Fold evaluation:

```bash
python -m scripts.train
```

This produces:
- `trained_models/model.pkl` — serialized model (~0.4 MB)
- `trained_models/evaluation.json` — metrics, confusion matrix, K-Fold results

## Running

```bash
uvicorn app.main:app --reload --port 8000
```

Or via Docker Compose from the project root:

```bash
docker compose up --build
```

## API Endpoints

All endpoints under `/api/v1`.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/login` | No | Login, returns JWT tokens |
| POST | `/auth/refresh` | No | Refresh access token |
| POST | `/auth/logout` | Yes | Logout (204) |
| GET | `/auth/me` | Yes | Current user info |
| POST | `/tickets` | Yes | Create ticket (auto-classifies) |
| GET | `/tickets` | Yes | List tickets (paginated, filterable) |
| GET | `/tickets/{id}` | Yes | Get single ticket |
| PATCH | `/tickets/{id}` | Yes | Update ticket |
| DELETE | `/tickets/{id}` | Yes | Delete ticket |
| POST | `/classifier/predict` | No | Classify text |
| GET | `/model/info` | No | Model metadata |
| GET | `/model/metrics` | No | Accuracy, F1, per-class metrics |
| GET | `/model/confusion-matrix` | No | 11×11 confusion matrix |
| GET | `/model/kfolds` | No | K-Fold cross validation report |
| GET | `/model/top-words?class=X&n=20` | No | Top discriminative words |

## Demo Users

| Email | Password | Role |
|-------|----------|------|
| admin@demo.com | admin123 | admin |
| agente@demo.com | agente123 | agente |
| cliente@demo.com | cliente123 | cliente |

## Tests

```bash
python -m pytest tests/ -v
```

87 tests covering preprocessor, classifier, evaluator, and all API endpoints.

## Architecture

```
app/
├── naive_bayes/          # ML core (from scratch, no sklearn)
│   ├── preprocessor.py   # Tokenize, stopwords, stemming (NLTK)
│   ├── classifier.py     # NaiveBayesMultinomial (BoW, Laplace, log-sum)
│   ├── evaluator.py      # K-Fold CV, confusion matrix, metrics
│   └── model_io.py       # Pickle save/load
├── db/                   # SQLite persistence (stdlib sqlite3)
│   ├── database.py       # Schema, connection factory
│   └── seed.py           # Demo user seeding
├── models/               # Pydantic request/response schemas
├── routers/              # FastAPI route handlers
├── services/             # Business logic (auth, tickets, classifier)
├── dependencies.py       # JWT auth middleware
├── config.py             # Settings (paths, JWT, CORS)
└── main.py               # App entry point, lifespan
```
