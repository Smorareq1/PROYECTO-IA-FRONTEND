from fastapi import APIRouter, HTTPException, Query

from app.models.ticket import (
    CreateTicketRequest,
    UpdateTicketRequest,
    TicketResponse,
    PaginatedTickets,
)
from app.services.ticket_service import (
    create_ticket,
    get_ticket,
    list_tickets,
    update_ticket,
    delete_ticket,
)
import app.main as main_module

router = APIRouter()

# Default user for ticket creation (no auth required)
DEFAULT_USER_ID = "u-001"


@router.post("", response_model=TicketResponse)
def create(body: CreateTicketRequest):
    # Auto-classify the ticket using the loaded model
    model = main_module.classifier
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")

    prediction = model.predict(f"{body.subject} {body.description}")

    ticket = create_ticket(
        subject=body.subject,
        description=body.description,
        predicted_category=prediction["category"],
        confidences=prediction["confidences"],
        created_by=DEFAULT_USER_ID,
    )
    return ticket


@router.get("", response_model=PaginatedTickets)
def list_all(
    status: str | None = Query(None),
    category: str | None = Query(None),
    q: str | None = Query(None),
    assignee: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    return list_tickets(
        status=status,
        category=category,
        q=q,
        assignee=assignee,
        page=page,
        size=size,
    )


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_one(ticket_id: str):
    ticket = get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.patch("/{ticket_id}", response_model=TicketResponse)
def update(
    ticket_id: str,
    body: UpdateTicketRequest,
):
    existing = get_ticket(ticket_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Ticket not found")

    updated = update_ticket(ticket_id, body.model_dump(exclude_none=True))
    return updated


@router.delete("/{ticket_id}", status_code=204)
def delete(ticket_id: str):
    if not delete_ticket(ticket_id):
        raise HTTPException(status_code=404, detail="Ticket not found")
    return None
