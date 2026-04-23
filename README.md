# TicketAI — AI-Powered Ticket Classification System

Full-stack application that classifies customer support tickets using a **Naïve Bayes Multinomial classifier built from scratch** (no scikit-learn). Trained on the [Bitext Customer Support dataset](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset) with 26,872 samples across 11 categories.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 + TypeScript + Vite + Pinia + Tailwind CSS |
| Backend | Python + FastAPI + SQLite |
| ML | Naïve Bayes (from scratch) + NLTK (tokenization only) |
| Infra | Docker Compose + nginx |

## Quick Start

### Prerequisites
- Node.js 20+
- Python 3.11+
- Docker & Docker Compose (optional)

### Option A: Docker Compose (recommended)

```bash
# 1. Download dataset and train model
cd backend
pip install -r requirements.txt
python -m scripts.download_dataset
python -m scripts.train
cd ..

# 2. Run everything
docker compose up --build
```

Frontend at `http://localhost:5173`, backend at `http://localhost:8000`.

### Option B: Local Development

```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
python -m scripts.download_dataset
python -m scripts.train
uvicorn app.main:app --reload --port 8000

# Terminal 2 — Frontend
npm install
npm run dev
```

## Features

- **Ticket Classification** — Auto-categorizes tickets into 11 categories (Account, Cancel, Contact, Delivery, Feedback, Invoice, Order, Payment, Refund, Shipping, Subscription)
- **Classification Playground** — Real-time text classification with confidence scores and token visualization
- **Analytics Dashboard** — Model metrics, confusion matrix, K-Fold cross validation results, per-class performance
- **Ticket Queue** — Agent workflow for reviewing and reassigning ticket categories
- **JWT Authentication** — Role-based access (admin, agente, cliente)

## Demo Users

| Email | Password | Role |
|-------|----------|------|
| admin@demo.com | admin123 | admin |
| agente@demo.com | agente123 | agente |
| cliente@demo.com | cliente123 | cliente |

## Tests

```bash
# Backend (87 tests)
cd backend && python -m pytest tests/ -v

# Frontend type-check
npx vue-tsc -b
```

## Project Structure

```
├── src/                   # Vue 3 frontend
│   ├── core/              # API client, auth store, config
│   ├── design-system/     # Atoms, molecules, tokens
│   └── features/          # Auth, tickets, classifier, metrics, landing
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── naive_bayes/   # From-scratch NB classifier
│   │   ├── db/            # SQLite (stdlib sqlite3)
│   │   ├── routers/       # API endpoints
│   │   └── services/      # Business logic
│   ├── scripts/           # Dataset download, model training
│   └── tests/             # pytest suite
├── docker-compose.yml
└── nginx.conf
```

See [backend/README.md](backend/README.md) for detailed backend documentation.
