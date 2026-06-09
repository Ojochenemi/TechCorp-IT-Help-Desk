# Tests

## Backend Tests

Run all backend tests:

```bash
cd tests
pytest backend/ -v
```

Run a specific test file:

```bash
pytest backend/test_tickets.py -v
```

Run with coverage:

```bash
pytest backend/ --cov=server
```

## Test Structure

- `conftest.py` — Shared fixtures (TestClient, sample data)
- `test_tickets.py` — Ticket CRUD and filtering
- `test_dashboard.py` — Dashboard summary and KPIs
- `test_misc_endpoints.py` — Agents, SLA, escalations, satisfaction, categories, reports
