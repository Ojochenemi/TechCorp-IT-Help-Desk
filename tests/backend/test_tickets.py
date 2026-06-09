"""
Tests for ticket API endpoints.
"""


class TestTicketEndpoints:
    """Test suite for ticket-related endpoints."""

    def test_get_all_tickets(self, client):
        """Test getting all tickets."""
        response = client.get("/api/tickets")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 35

    def test_ticket_structure(self, client):
        """Test that tickets have the required fields."""
        response = client.get("/api/tickets")
        data = response.json()

        first = data[0]
        required_fields = [
            "id", "subject", "description", "status", "priority",
            "category", "requester_name", "requester_email",
            "requester_department", "assigned_to", "created_at",
            "updated_at", "sla_priority", "tags"
        ]
        for field in required_fields:
            assert field in first, f"Missing field: {field}"

    def test_get_ticket_by_id(self, client):
        """Test getting a specific ticket by ID."""
        response = client.get("/api/tickets/TKT-001")
        assert response.status_code == 200

        ticket = response.json()
        assert ticket["id"] == "TKT-001"
        assert "sla_status" in ticket
        assert "agent_name" in ticket

    def test_get_nonexistent_ticket(self, client):
        """Test getting a ticket that doesn't exist."""
        response = client.get("/api/tickets/TKT-999")
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_filter_tickets_by_status(self, client):
        """Test filtering tickets by status."""
        response = client.get("/api/tickets?status=Open")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 5
        for ticket in data:
            assert ticket["status"] == "Open"

    def test_filter_tickets_by_priority(self, client):
        """Test filtering tickets by priority."""
        response = client.get("/api/tickets?priority=Critical")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 3
        for ticket in data:
            assert ticket["priority"] == "Critical"

    def test_filter_tickets_by_category(self, client):
        """Test filtering tickets by category."""
        response = client.get("/api/tickets?category=Network")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 8
        for ticket in data:
            assert ticket["category"].lower() == "network"

    def test_filter_tickets_by_agent(self, client):
        """Test filtering tickets by assigned agent."""
        response = client.get("/api/tickets?agent_id=AGT-001")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        for ticket in data:
            assert ticket["assigned_to"] == "AGT-001"

    def test_filter_tickets_multiple(self, client):
        """Test filtering tickets with multiple filters."""
        response = client.get("/api/tickets?status=Resolved&priority=Medium")
        assert response.status_code == 200

        data = response.json()
        for ticket in data:
            assert ticket["status"] == "Resolved"
            assert ticket["priority"].lower() == "medium"

    def test_ticket_status_values(self, client):
        """Test that tickets have valid status values."""
        response = client.get("/api/tickets")
        data = response.json()

        valid_statuses = {"open", "in progress", "waiting on customer", "escalated", "resolved", "closed"}
        for ticket in data:
            assert ticket["status"].lower() in valid_statuses

    def test_ticket_priority_values(self, client):
        """Test that tickets have valid priority values."""
        response = client.get("/api/tickets")
        data = response.json()

        valid_priorities = {"critical", "high", "medium", "low"}
        for ticket in data:
            assert ticket["priority"].lower() in valid_priorities

    def test_ticket_dates_format(self, client):
        """Test that ticket dates are in ISO format."""
        response = client.get("/api/tickets")
        data = response.json()

        for ticket in data:
            assert "T" in ticket["created_at"]
            assert "T" in ticket["updated_at"]

    def test_create_ticket(self, client):
        """Test creating a new ticket."""
        new_ticket = {
            "subject": "Test ticket creation",
            "description": "Testing the create endpoint",
            "priority": "Low",
            "category": "Other",
            "requester_name": "Test User",
            "requester_email": "test@techcorp.com",
            "requester_department": "Engineering"
        }

        response = client.post("/api/tickets", json=new_ticket)
        assert response.status_code == 200

        data = response.json()
        assert data["subject"] == "Test ticket creation"
        assert data["status"] == "Open"
        assert data["id"].startswith("TKT-")

    def test_resolved_tickets_have_resolved_at(self, client):
        """Test that resolved tickets have a resolved_at timestamp."""
        response = client.get("/api/tickets?status=Resolved")
        data = response.json()

        for ticket in data:
            assert ticket["resolved_at"] is not None

    def test_closed_tickets_have_closed_at(self, client):
        """Test that closed tickets have a closed_at timestamp."""
        response = client.get("/api/tickets?status=Closed")
        data = response.json()

        for ticket in data:
            assert ticket["closed_at"] is not None

    def test_tags_are_lists(self, client):
        """Test that tags field is always a list."""
        response = client.get("/api/tickets")
        data = response.json()

        for ticket in data:
            assert isinstance(ticket["tags"], list)
