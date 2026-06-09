# Server - Python FastAPI Backend

## Stack
- FastAPI with Pydantic v2
- Uvicorn (port 8001)
- In-memory data from JSON files

## Key Patterns
- Pydantic models for all response types
- `apply_filters()` helper handles status, priority, category, agent_id
- `filter_by_month()` handles YYYY-MM and Q1-2026 formats
- `calculate_sla_status()` computes response/resolution compliance per ticket
- Case-insensitive comparisons: `.lower()` on both sides
- HTTPException(404) for missing resources

## Data Relationships
- `tickets.assigned_to` -> `agents.id`
- `escalations.ticket_id` -> `tickets.id`
- `satisfaction.ticket_id` -> `tickets.id` (resolved/closed only)
