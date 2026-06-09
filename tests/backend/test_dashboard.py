"""
Tests for dashboard API endpoints.
"""


class TestDashboardEndpoints:
    """Test suite for dashboard-related endpoints."""

    def test_get_dashboard_summary(self, client):
        """Test getting dashboard summary."""
        response = client.get("/api/dashboard/summary")
        assert response.status_code == 200

        data = response.json()
        required_fields = [
            "open_tickets", "avg_resolution_hours", "sla_compliance_pct",
            "agent_utilization", "total_tickets", "resolved_tickets",
            "status_distribution", "priority_distribution", "recent_tickets"
        ]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

    def test_dashboard_data_types(self, client):
        """Test that dashboard values have correct types."""
        response = client.get("/api/dashboard/summary")
        data = response.json()

        assert isinstance(data["open_tickets"], int)
        assert isinstance(data["avg_resolution_hours"], (int, float))
        assert isinstance(data["sla_compliance_pct"], (int, float))
        assert isinstance(data["agent_utilization"], (int, float))
        assert isinstance(data["status_distribution"], dict)
        assert isinstance(data["priority_distribution"], dict)
        assert isinstance(data["recent_tickets"], list)

    def test_dashboard_non_negative_values(self, client):
        """Test that dashboard numeric values are non-negative."""
        response = client.get("/api/dashboard/summary")
        data = response.json()

        assert data["open_tickets"] >= 0
        assert data["avg_resolution_hours"] >= 0
        assert 0 <= data["sla_compliance_pct"] <= 100
        assert 0 <= data["agent_utilization"] <= 100

    def test_dashboard_open_tickets_calculation(self, client):
        """Test that open tickets count matches actual data."""
        tickets_response = client.get("/api/tickets")
        all_tickets = tickets_response.json()

        open_statuses = {"Open", "In Progress", "Waiting on Customer", "Escalated"}
        expected_open = sum(1 for t in all_tickets if t["status"] in open_statuses)

        dashboard_response = client.get("/api/dashboard/summary")
        dashboard = dashboard_response.json()

        assert dashboard["open_tickets"] == expected_open

    def test_dashboard_status_distribution(self, client):
        """Test that status distribution sums to total tickets."""
        response = client.get("/api/dashboard/summary")
        data = response.json()

        total_from_distribution = sum(data["status_distribution"].values())
        assert total_from_distribution == data["total_tickets"]

    def test_dashboard_with_filters(self, client):
        """Test dashboard summary with filters applied."""
        response = client.get("/api/dashboard/summary?priority=Critical")
        assert response.status_code == 200

        data = response.json()
        assert data["total_tickets"] == 3

    def test_dashboard_recent_tickets_limit(self, client):
        """Test that recent tickets returns at most 5."""
        response = client.get("/api/dashboard/summary")
        data = response.json()

        assert len(data["recent_tickets"]) <= 5

    def test_dashboard_recent_tickets_ordered(self, client):
        """Test that recent tickets are ordered by created_at descending."""
        response = client.get("/api/dashboard/summary")
        data = response.json()

        dates = [t["created_at"] for t in data["recent_tickets"]]
        assert dates == sorted(dates, reverse=True)
