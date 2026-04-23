from pydantic import BaseModel


class PredictRequest(BaseModel):
    text: str


class PredictionResponse(BaseModel):
    category: str
    confidences: dict[str, float]
    log_probs: dict[str, float]
    tokens: list[str]
    processing_ms: float
