from pydantic import BaseModel


class ClassMetrics(BaseModel):
    # Using alias to match frontend "class" field
    class_name: str
    precision: float
    recall: float
    f1: float
    support: int


class ModelInfoResponse(BaseModel):
    version: str
    trained_at: str
    vocab_size: int
    doc_count: int
    classes: list[str]


class ModelMetricsResponse(BaseModel):
    accuracy: float
    macro_f1: float
    per_class: list[dict]


class ConfusionMatrixResponse(BaseModel):
    labels: list[str]
    matrix: list[list[int]]


class KFoldResultResponse(BaseModel):
    fold: int
    accuracy: float
    macro_f1: float
    per_class: list[dict]


class KFoldReportResponse(BaseModel):
    k: int
    folds: list[KFoldResultResponse]
    mean: dict
    std: dict


class TopWordResponse(BaseModel):
    word: str
    weight: float
