from fastapi import APIRouter, HTTPException

from app.models.prediction import PredictRequest, PredictionResponse
import app.main as main_module

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
def predict(body: PredictRequest):
    model = main_module.classifier
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if not body.text.strip():
        raise HTTPException(status_code=422, detail="Text cannot be empty")

    result = model.predict(body.text)
    return result
