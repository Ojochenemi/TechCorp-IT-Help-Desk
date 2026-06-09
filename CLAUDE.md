# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Stack

- **Frontend**: Vue 3 + Composition API + Vite (port 3000)
- **Backend**: Python FastAPI (port 8001)
- **Data**: JSON files in `server/data/` loaded via `server/mock_data.py`

## Quick Start

```bash
# Backend
cd server
uv run python main.py

# Frontend
cd client
npm install && npm run dev
```

## File Locations
- Views: `client/src/views/*.vue`
- Components: `client/src/components/*.vue`
- API Client: `client/src/api.js`
- Composables: `client/src/composables/*.js`
- Backend: `server/main.py`, `server/mock_data.py`
- Data: `server/data/*.json`
- Tests: `tests/backend/*.py`

## Tests

Tests live in `tests/backend/` and use pytest with FastAPI's `TestClient`.

```bash
cd tests
pytest backend/ -v                                                        # all 43 tests
pytest backend/test_tickets.py -v                                         # one file
pytest backend/test_tickets.py::TestTicketEndpoints::test_get_all_tickets # one test
pytest backend/ --cov=server                                              # with coverage
```

`pytest.ini` sets `testpaths = backend` and `pythonpath = ../server`, so run pytest from the `tests/` directory.

## API Endpoints
- `GET /api/tickets`: Filters: status, priority, category, agent_id, month
- `GET /api/tickets/{id}`: Single ticket with SLA status
- `POST /api/tickets`: Create new ticket
- `GET /api/agents`: Filters: status, role
- `GET /api/agents/{id}`: Agent with workload stats
- `GET /api/escalations`: Filters: status, priority
- `GET /api/sla/compliance`: SLA compliance per priority
- `GET /api/dashboard/summary`: All filters supported
- `GET /api/tickets/{id}/comments`: All comments for a ticket
- `POST /api/tickets/{id}/comments`: Add a comment (`author_name`, `author_email`, `body`)

## Architecture

**Data flow**: Vue component → `client/src/api.js` (axios, base URL `http://localhost:8001/api`) → FastAPI endpoint in `server/main.py` → in-memory list filtered by query params → Pydantic-validated response.

**Backend** (`server/main.py`) is a single file containing all 15 endpoints, Pydantic models, and two shared helpers:
- `apply_filters(tickets, status, priority, category, agent_id)` — common filter logic reused across endpoints
- `filter_by_month(items, month)` — supports `YYYY-MM` and quarter strings (`Q1-2026`)

SLA compliance is computed in real time by comparing ticket timestamps against priority-based rules (minutes: 15, 60, 240, 480, 1440, 2880) loaded from `data/sla_rules.json`.

**Frontend** state pattern: raw API data stored in `ref()`, derived values in `computed()`. The five filter values (Status, Priority, Category, Agent, Period) live in `composables/useFilters.js` and are passed as query params on every fetch.

**i18n**: `composables/useI18n.js` reads `locales/en.js` and `locales/ja.js`. Any new UI strings need entries in both files.

## Common Issues
1. Use unique keys in v-for (`ticket.id`, `agent.id`, never `index`)
2. Validate dates before `.getMonth()` calls
3. Update Pydantic models when changing JSON data structure
4. Filter comparisons are case-insensitive on the backend
5. SLA times are in minutes (15, 60, 240, 480, 1440, 2880)
