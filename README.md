# IT Help Desk & Ticket Tracker

A full-stack demo application for a Claude Code workshop — ticket management, SLA tracking, agent workload, escalation monitoring, and analytics for IT support operations.

## Tech Stack

- **Frontend**: Vue 3 + Vite (port 3000)
- **Backend**: Python FastAPI (port 8001)
- **Data**: In-memory mock data (no database)

## Features

- Dashboard with KPIs, status distribution, and priority breakdown
- Ticket management with 6-stage status workflow
- Agent roster with workload and performance metrics
- SLA compliance tracking with breach detection
- Escalation monitoring
- Monthly trends and agent performance reports

## Quick Start

**One-command startup:**
```bash
./scripts/start.sh
# Starts both backend and frontend
# Backend: http://localhost:8001
# Frontend: http://localhost:3000
# API Docs: http://localhost:8001/docs
```

**Manual startup:**

Backend:
```bash
cd server
uv venv && uv sync
uv run python main.py
```

Frontend:
```bash
cd client
npm install
npm run dev
```

## API Endpoints

All ticket endpoints support optional filtering via query params: `status`, `priority`, `category`, `agent_id`, `month`

- `GET /api/tickets` — All tickets
- `GET /api/tickets/{id}` — Single ticket with SLA status
- `POST /api/tickets` — Create ticket
- `GET /api/agents` — Agents (filter: status, role)
- `GET /api/agents/{id}` — Agent with workload stats
- `GET /api/escalations` — Escalation records
- `GET /api/sla/compliance` — SLA compliance per priority
- `GET /api/sla/breaches` — Tickets that breached SLA
- `GET /api/dashboard/summary` — Summary statistics
- `GET /api/reports/monthly-trends` — Monthly aggregations
- `GET /api/reports/agent-performance` — Per-agent metrics
- `GET /api/satisfaction/summary` — Customer satisfaction stats
- `GET /api/categories` — Ticket categories

## Demo Data

Mock data includes:
- 35 tickets across 6 statuses and 4 priority levels
- 7 support agents (L1, L2, L3)
- 6 ticket categories (Network, Hardware, Software, Access/Permissions, Email, Other)
- SLA rules with response and resolution time targets
- 8 escalation records
- 15 customer satisfaction ratings

Data files: `server/data/*.json`

## Tests

```bash
# Run all backend tests (43 tests)
cd server && source .venv/bin/activate && cd ..
pytest tests/backend/ -v
```

## Platform Notes

**macOS/Linux:** The startup scripts (`./scripts/start.sh` and `./scripts/stop.sh`) work out of the box.

**Windows:** Use the manual startup commands — run each in a separate terminal.

---

**Note:** Demo application with in-memory data. Not production-ready without database, authentication, and security implementation.
