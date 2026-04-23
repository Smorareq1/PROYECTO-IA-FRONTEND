from pydantic import BaseModel


class CreateTicketRequest(BaseModel):
    subject: str
    description: str


class UpdateTicketRequest(BaseModel):
    status: str | None = None
    final_category: str | None = None
    assignee_id: str | None = None


class TicketResponse(BaseModel):
    id: str
    subject: str
    description: str
    predicted_category: str
    confidences: dict[str, float]
    final_category: str | None
    status: str
    created_by: str
    assignee_id: str | None
    created_at: str
    updated_at: str


class PaginatedTickets(BaseModel):
    items: list[TicketResponse]
    total: int
    page: int
    size: int
    pages: int
