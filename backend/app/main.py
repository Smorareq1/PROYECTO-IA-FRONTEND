from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import CORS_ORIGINS, MODEL_PATH
from app.naive_bayes.model_io import load_model
from app.routers import (
    auth, tickets,
    classifier as classifier_router,
    model_analytics,
)


# Global reference to the loaded model (set during startup)
classifier = None
evaluation_data = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize DB, seed users, load trained model on startup."""
    global classifier, evaluation_data
    import json
    from pathlib import Path
    from app.config import EVALUATION_PATH
    from app.db.database import init_db
    from app.db.seed import seed_users

    # Init database and seed demo users
    print("Initializing database...")
    init_db()
    seed_users()

    # Load trained model
    model_path = Path(MODEL_PATH)
    eval_path = Path(EVALUATION_PATH)

    if model_path.exists():
        classifier = load_model(str(model_path))
        print(f"Model loaded from {model_path}")
    else:
        print(f"WARNING: No trained model found at {model_path}. "
              "Run 'python -m scripts.train' first.")

    if eval_path.exists():
        with open(eval_path, "r") as f:
            evaluation_data = json.load(f)
        print(f"Evaluation data loaded from {eval_path}")
    else:
        print(f"WARNING: No evaluation data found at {eval_path}.")

    yield

    # Cleanup
    classifier = None
    evaluation_data = None


app = FastAPI(
    title="TicketAI Backend",
    description="Naïve Bayes ticket classifier API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Return a proper JSON 500 so CORSMiddleware can add its headers."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": classifier is not None}


# Mount routers under /api/v1
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(tickets.router, prefix="/api/v1/tickets", tags=["tickets"])
app.include_router(classifier_router.router, prefix="/api/v1/classifier", tags=["classifier"])
app.include_router(model_analytics.router, prefix="/api/v1/model", tags=["model"])
