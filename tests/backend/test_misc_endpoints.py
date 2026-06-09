"""
Tests for agent, SLA, escalation, satisfaction, category, and report endpoints.
"""


class TestAgentEndpoints:
    """Test suite for agent-related endpoints."""

    def test_get_all_agents(self, client):
        """Test getting all agents."""
        response = client.get("/api/agents")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 7

    def test_agent_structure(self, client):
        """Test that agents have required fields."""
        response = client.get("/api/agents")
        data = response.json()

        first = data[0]
        for field in ["id", "name", "email", "role", "department", "status", "skills", "hire_date", "avatar_initials"]:
            assert field in first

    def test_get_agent_by_id(self, client):
        """Test getting a specific agent with workload stats."""
        response = client.get("/api/agents/AGT-001")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == "AGT-001"
        assert "assigned_tickets" in data
        assert "resolved_tickets" in data
        assert "avg_resolution_hours" in data
        assert "avg_satisfaction" in data

    def test_get_nonexistent_agent(self, client):
        """Test getting an agent that doesn't exist."""
        response = client.get("/api/agents/AGT-999")
        assert response.status_code == 404

    def test_filter_agents_by_role(self, client):
        """Test filtering agents by role."""
        response = client.get("/api/agents?role=L1")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 3
        for agent in data:
            assert agent["role"] == "L1"

    def test_filter_agents_by_status(self, client):
        """Test filtering agents by status."""
        response = client.get("/api/agents?status=Available")
        assert response.status_code == 200

        data = response.json()
        for agent in data:
            assert agent["status"] == "Available"


class TestSLAEndpoints:
    """Test suite for SLA-related endpoints."""

    def test_get_sla_compliance(self, client):
        """Test getting SLA compliance summary."""
        response = client.get("/api/sla/compliance")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 4

        for entry in data:
            assert "priority" in entry
            assert "response_compliance_pct" in entry
            assert "resolution_compliance_pct" in entry
            assert 0 <= entry["response_compliance_pct"] <= 100
            assert 0 <= entry["resolution_compliance_pct"] <= 100

    def test_get_sla_breaches(self, client):
        """Test getting SLA breach list."""
        response = client.get("/api/sla/breaches")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        for breach in data:
            assert "sla_status" in breach
            sla = breach["sla_status"]
            assert sla.get("response_met") is False or sla.get("resolution_met") is False


class TestEscalationEndpoints:
    """Test suite for escalation-related endpoints."""

    def test_get_all_escalations(self, client):
        """Test getting all escalations."""
        response = client.get("/api/escalations")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 8

    def test_escalation_structure(self, client):
        """Test that escalations have required fields."""
        response = client.get("/api/escalations")
        data = response.json()

        first = data[0]
        for field in ["id", "ticket_id", "escalated_from", "escalated_to", "reason", "escalated_at", "status"]:
            assert field in first

    def test_filter_escalations_by_status(self, client):
        """Test filtering escalations by status."""
        response = client.get("/api/escalations?status=Active")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 3
        for esc in data:
            assert esc["status"] == "Active"

    def test_active_escalations_match_escalated_tickets(self, client):
        """Test that active escalations correspond to escalated tickets."""
        esc_response = client.get("/api/escalations?status=Active")
        esc_ticket_ids = {e["ticket_id"] for e in esc_response.json()}

        tickets_response = client.get("/api/tickets?status=Escalated")
        escalated_ids = {t["id"] for t in tickets_response.json()}

        assert esc_ticket_ids == escalated_ids


class TestSatisfactionEndpoints:
    """Test suite for satisfaction-related endpoints."""

    def test_get_satisfaction_summary(self, client):
        """Test getting satisfaction summary."""
        response = client.get("/api/satisfaction/summary")
        assert response.status_code == 200

        data = response.json()
        assert "avg_rating" in data
        assert "total_ratings" in data
        assert "distribution" in data
        assert 1 <= data["avg_rating"] <= 5
        assert data["total_ratings"] == 15

    def test_satisfaction_distribution_sums(self, client):
        """Test that distribution sums to total ratings."""
        response = client.get("/api/satisfaction/summary")
        data = response.json()

        total = sum(data["distribution"].values())
        assert total == data["total_ratings"]


class TestCategoryEndpoints:
    """Test suite for category endpoints."""

    def test_get_all_categories(self, client):
        """Test getting all categories."""
        response = client.get("/api/categories")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 6

        names = {c["name"] for c in data}
        assert "Network" in names
        assert "Hardware" in names
        assert "Software" in names


class TestReportEndpoints:
    """Test suite for report endpoints."""

    def test_get_monthly_trends(self, client):
        """Test getting monthly trends."""
        response = client.get("/api/reports/monthly-trends")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        first = data[0]
        assert "month" in first
        assert "created_count" in first
        assert "resolved_count" in first

    def test_monthly_trends_ordered(self, client):
        """Test that monthly trends are ordered chronologically."""
        response = client.get("/api/reports/monthly-trends")
        data = response.json()

        months = [d["month"] for d in data]
        assert months == sorted(months)

    def test_get_agent_performance(self, client):
        """Test getting agent performance report."""
        response = client.get("/api/reports/agent-performance")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 7

        first = data[0]
        for field in ["agent_id", "agent_name", "role", "total_assigned", "total_resolved", "avg_resolution_hours", "avg_satisfaction"]:
            assert field in first

    def test_root_endpoint(self, client):
        """Test the root API endpoint."""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "version" in data
