"""Tests for the /api/v1/tickets endpoints (no auth required)."""


class TestCreateTicket:
    def test_create_ticket(self, client):
        resp = client.post("/api/v1/tickets", json={
            "subject": "I want to cancel my subscription",
            "description": "Please cancel it immediately and refund me",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"].startswith("TK-")
        assert data["subject"] == "I want to cancel my subscription"
        assert data["predicted_category"] in [
            "ACCOUNT", "CANCEL", "CONTACT", "DELIVERY", "FEEDBACK",
            "INVOICE", "ORDER", "PAYMENT", "REFUND", "SHIPPING", "SUBSCRIPTION",
        ]
        assert isinstance(data["confidences"], dict)
        assert data["status"] == "abierto"
        assert data["final_category"] is None

    def test_auto_classification(self, client):
        resp = client.post("/api/v1/tickets", json={
            "subject": "Shipping delay",
            "description": "My package has not arrived, tracking shows no updates",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["confidences"]) == 11
        total = sum(data["confidences"].values())
        assert abs(total - 1.0) < 0.01


class TestListTickets:
    def test_list_tickets(self, client):
        resp = client.get("/api/v1/tickets")
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert "pages" in data
        assert isinstance(data["items"], list)

    def test_pagination(self, client):
        resp = client.get("/api/v1/tickets?page=1&size=1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["size"] == 1
        assert len(data["items"]) <= 1

    def test_filter_by_status(self, client):
        resp = client.get("/api/v1/tickets?status=abierto")
        assert resp.status_code == 200
        for item in resp.json()["items"]:
            assert item["status"] == "abierto"


class TestGetTicket:
    def test_get_existing_ticket(self, client):
        create_resp = client.post("/api/v1/tickets", json={
            "subject": "Test get", "description": "Testing get endpoint",
        })
        ticket_id = create_resp.json()["id"]

        resp = client.get(f"/api/v1/tickets/{ticket_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == ticket_id

    def test_get_nonexistent_ticket(self, client):
        resp = client.get("/api/v1/tickets/TK-999999")
        assert resp.status_code == 404


class TestUpdateTicket:
    def test_update_status(self, client):
        create_resp = client.post("/api/v1/tickets", json={
            "subject": "Test update", "description": "Will update status",
        })
        ticket_id = create_resp.json()["id"]

        resp = client.patch(f"/api/v1/tickets/{ticket_id}", json={
            "status": "en_progreso",
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "en_progreso"

    def test_update_final_category(self, client):
        create_resp = client.post("/api/v1/tickets", json={
            "subject": "Test category override", "description": "Agent corrects category",
        })
        ticket_id = create_resp.json()["id"]

        resp = client.patch(f"/api/v1/tickets/{ticket_id}", json={
            "final_category": "REFUND",
        })
        assert resp.status_code == 200
        assert resp.json()["final_category"] == "REFUND"

    def test_update_nonexistent(self, client):
        resp = client.patch("/api/v1/tickets/TK-999999", json={
            "status": "cerrado",
        })
        assert resp.status_code == 404


class TestDeleteTicket:
    def test_delete_ticket(self, client):
        create_resp = client.post("/api/v1/tickets", json={
            "subject": "To be deleted", "description": "This will be removed",
        })
        ticket_id = create_resp.json()["id"]

        resp = client.delete(f"/api/v1/tickets/{ticket_id}")
        assert resp.status_code == 204

        get_resp = client.get(f"/api/v1/tickets/{ticket_id}")
        assert get_resp.status_code == 404

    def test_delete_nonexistent(self, client):
        resp = client.delete("/api/v1/tickets/TK-999999")
        assert resp.status_code == 404
