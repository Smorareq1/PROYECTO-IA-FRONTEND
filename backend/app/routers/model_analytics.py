from fastapi import APIRouter, HTTPException, Query

from app.models.metrics import (
    ModelInfoResponse,
    ModelMetricsResponse,
    ConfusionMatrixResponse,
    KFoldReportResponse,
    TopWordResponse,
)
import app.main as main_module

router = APIRouter()


def _get_eval_data() -> dict:
    if not main_module.evaluation_data:
        raise HTTPException(status_code=503, detail="Evaluation data not loaded")
    return main_module.evaluation_data


@router.get("/info", response_model=ModelInfoResponse)
def model_info():
    data = _get_eval_data()
    return data["model_info"]


@router.get("/metrics", response_model=ModelMetricsResponse)
def model_metrics():
    data = _get_eval_data()
    return data["metrics"]


@router.get("/confusion-matrix", response_model=ConfusionMatrixResponse)
def confusion_matrix():
    data = _get_eval_data()
    return data["confusion_matrix"]


@router.get("/kfolds", response_model=KFoldReportResponse)
def kfolds():
    data = _get_eval_data()
    return data["kfold_report"]


@router.get("/top-words", response_model=list[TopWordResponse])
def top_words(
    category: str = Query(..., alias="class"),
    n: int = Query(20, ge=1, le=100),
):
    model = main_module.classifier
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if category not in model.classes:
        raise HTTPException(status_code=404, detail=f"Unknown category: {category}")

    return model.get_top_words(category, n)
