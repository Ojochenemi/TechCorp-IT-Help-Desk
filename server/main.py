from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from mock_data import tickets, agents, sla_rules, escalations, categories, satisfaction_ratings, comments

app = FastAPI(title="IT Help Desk System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Pydantic Models ---

class Ticket(BaseModel):
    id: str
    subject: str
    description: str
    status: str
    priority: str
    category: str
    requester_name: str
    requester_email: str
    requester_department: str
    assigned_to: str
    created_at: str
    updated_at: str
    resolved_at: Optional[str] = None
    closed_at: Optional[str] = None
    first_response_at: Optional[str] = None
    sla_priority: str
    tags: List[str]


class CreateTicketRequest(BaseModel):
    subject: str
    description: str
    priority: str
    category: str
    requester_name: str
    requester_email: str
    requester_department: str
    assigned_to: Optional[str] = None


class Agent(BaseModel):
    id: str
    name: str
    email: str
    role: str
    department: str
    status: str
    skills: List[str]
    hire_date: str
    avatar_initials: str


class SLARule(BaseModel):
    id: str
    priority: str
    first_response_minutes: int
    resolution_minutes: int
    description: str


class Escalation(BaseModel):
    id: str
    ticket_id: str
    escalated_from: str
    escalated_to: str
    reason: str
    escalated_at: str
    resolved_at: Optional[str] = None
    status: str
    notes: Optional[str] = None


class Category(BaseModel):
    id: str
    name: str
    description: str


class Comment(BaseModel):
    id: str
    ticket_id: str
    author_name: str
    author_email: str
    body: str
    created_at: str


class CreateCommentRequest(BaseModel):
    author_name: str
    author_email: str
    body: str


class SatisfactionRating(BaseModel):
    id: str
    ticket_id: str
    agent_id: str
    rating: int
    comment: str
    submitted_at: str


# --- Helper Functions ---

def apply_filters(items: list, status: Optional[str] = None, priority: Optional[str] = None,
                  category: Optional[str] = None, agent_id: Optional[str] = None) -> list:
    """Apply common filters to a list of items."""
    filtered = items

    if status and status != 'all':
        filtered = [item for item in filtered if item.get('status', '').lower() == status.lower()]

    if priority and priority != 'all':
        filtered = [item for item in filtered if item.get('priority', '').lower() == priority.lower()]

    if category and category != 'all':
        filtered = [item for item in filtered if item.get('category', '').lower() == category.lower()]

    if agent_id and agent_id != 'all':
        filtered = [item for item in filtered if item.get('assigned_to') == agent_id]

    return filtered


def filter_by_month(items: list, month: Optional[str], date_field: str = 'created_at') -> list:
    """Filter items by month (YYYY-MM format) or quarter (Q1-2026)."""
    if not month or month == 'all':
        return items

    quarter_map = {
        'Q1-2026': ['2026-01', '2026-02', '2026-03'],
        'Q4-2025': ['2025-10', '2025-11', '2025-12'],
    }

    if month.startswith('Q'):
        if month in quarter_map:
            months = quarter_map[month]
            return [item for item in items if any(m in item.get(date_field, '') for m in months)]
    else:
        return [item for item in items if month in item.get(date_field, '')]

    return items


def get_sla_rule(priority: str) -> Optional[dict]:
    """Get the SLA rule for a given priority."""
    for rule in sla_rules:
        if rule['priority'].lower() == priority.lower():
            return rule
    return None


def calculate_sla_status(ticket: dict) -> dict:
    """Calculate SLA compliance for a ticket."""
    rule = get_sla_rule(ticket.get('sla_priority', ticket.get('priority', '')))
    if not rule:
        return {'response_met': None, 'resolution_met': None}

    result = {'response_met': None, 'resolution_met': None}

    created = datetime.fromisoformat(ticket['created_at'])

    if ticket.get('first_response_at'):
        response_time = datetime.fromisoformat(ticket['first_response_at'])
        diff_minutes = (response_time - created).total_seconds() / 60
        result['response_met'] = diff_minutes < rule['first_response_minutes']
        result['response_minutes'] = round(diff_minutes, 1)
        result['response_target'] = rule['first_response_minutes']

    if ticket.get('resolved_at'):
        resolve_time = datetime.fromisoformat(ticket['resolved_at'])
        diff_minutes = (resolve_time - created).total_seconds() / 60
        result['resolution_met'] = diff_minutes < rule['resolution_minutes']
        result['resolution_minutes'] = round(diff_minutes, 1)
        result['resolution_target'] = rule['resolution_minutes']

    return result


# --- API Endpoints ---

@app.get("/")
def root():
    return {"message": "IT Help Desk System API", "version": "1.0.0"}


@app.get("/api/tickets", response_model=List[Ticket])
def get_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    agent_id: Optional[str] = None,
    month: Optional[str] = None
):
    """Get all tickets with optional filtering."""
    filtered = apply_filters(tickets, status, priority, category, agent_id)
    filtered = filter_by_month(filtered, month)
    return filtered


@app.get("/api/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    """Get a specific ticket with SLA status."""
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    result = dict(ticket)
    result['sla_status'] = calculate_sla_status(ticket)

    agent = next((a for a in agents if a["id"] == ticket.get("assigned_to")), None)
    if agent:
        result['agent_name'] = agent['name']

    return result


@app.post("/api/tickets", response_model=Ticket)
def create_ticket(request: CreateTicketRequest):
    """Create a new ticket."""
    max_num = max((int(t["id"].split("-")[1]) for t in tickets), default=0)
    new_id = f"TKT-{max_num + 1:03d}"

    now = datetime.now().isoformat(timespec='seconds')

    assigned = request.assigned_to
    if not assigned:
        for agent in agents:
            if agent['status'] == 'Available' and request.category in agent.get('skills', []):
                assigned = agent['id']
                break
        if not assigned:
            assigned = agents[0]['id']

    new_ticket = {
        "id": new_id,
        "subject": request.subject,
        "description": request.description,
        "status": "Open",
        "priority": request.priority,
        "category": request.category,
        "requester_name": request.requester_name,
        "requester_email": request.requester_email,
        "requester_department": request.requester_department,
        "assigned_to": assigned,
        "created_at": now,
        "updated_at": now,
        "resolved_at": None,
        "closed_at": None,
        "first_response_at": None,
        "sla_priority": request.priority,
        "tags": []
    }

    tickets.append(new_ticket)
    return new_ticket


@app.get("/api/agents", response_model=List[Agent])
def get_agents(
    status: Optional[str] = None,
    role: Optional[str] = None
):
    """Get all agents with optional filtering."""
    filtered = agents

    if status and status != 'all':
        filtered = [a for a in filtered if a.get('status', '').lower() == status.lower()]

    if role and role != 'all':
        filtered = [a for a in filtered if a.get('role', '').lower() == role.lower()]

    return filtered


@app.get("/api/agents/{agent_id}")
def get_agent(agent_id: str):
    """Get a specific agent with workload statistics."""
    agent = next((a for a in agents if a["id"] == agent_id), None)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent_tickets = [t for t in tickets if t.get('assigned_to') == agent_id]
    resolved = [t for t in agent_tickets if t['status'] in ('Resolved', 'Closed')]
    agent_ratings = [r for r in satisfaction_ratings if r.get('agent_id') == agent_id]

    avg_resolution_hours = 0
    if resolved:
        total_hours = 0
        count = 0
        for t in resolved:
            if t.get('resolved_at') and t.get('created_at'):
                created = datetime.fromisoformat(t['created_at'])
                resolved_dt = datetime.fromisoformat(t['resolved_at'])
                total_hours += (resolved_dt - created).total_seconds() / 3600
                count += 1
        if count > 0:
            avg_resolution_hours = round(total_hours / count, 1)

    avg_satisfaction = 0
    if agent_ratings:
        avg_satisfaction = round(sum(r['rating'] for r in agent_ratings) / len(agent_ratings), 1)

    result = dict(agent)
    result['assigned_tickets'] = len(agent_tickets)
    result['resolved_tickets'] = len(resolved)
    result['open_tickets'] = len([t for t in agent_tickets if t['status'] in ('Open', 'In Progress', 'Waiting on Customer', 'Escalated')])
    result['avg_resolution_hours'] = avg_resolution_hours
    result['avg_satisfaction'] = avg_satisfaction

    return result


@app.get("/api/escalations", response_model=List[Escalation])
def get_escalations(
    status: Optional[str] = None,
    priority: Optional[str] = None
):
    """Get escalation records with optional filtering."""
    filtered = escalations

    if status and status != 'all':
        filtered = [e for e in filtered if e.get('status', '').lower() == status.lower()]

    if priority and priority != 'all':
        ticket_ids = {t['id'] for t in tickets if t.get('priority', '').lower() == priority.lower()}
        filtered = [e for e in filtered if e.get('ticket_id') in ticket_ids]

    return filtered


@app.get("/api/sla/compliance")
def get_sla_compliance():
    """Get SLA compliance summary per priority level."""
    result = []

    for rule in sla_rules:
        priority = rule['priority']
        priority_tickets = [t for t in tickets if t.get('priority') == priority and t['status'] in ('Resolved', 'Closed')]

        response_met = 0
        resolution_met = 0
        total = len(priority_tickets)

        for ticket in priority_tickets:
            sla = calculate_sla_status(ticket)
            if sla.get('response_met'):
                response_met += 1
            if sla.get('resolution_met'):
                resolution_met += 1

        result.append({
            'priority': priority,
            'total_tickets': total,
            'response_compliance_pct': round((response_met / total * 100), 1) if total > 0 else 0,
            'resolution_compliance_pct': round((resolution_met / total * 100), 1) if total > 0 else 0,
            'response_target_minutes': rule['first_response_minutes'],
            'resolution_target_minutes': rule['resolution_minutes']
        })

    return result


@app.get("/api/sla/breaches")
def get_sla_breaches():
    """Get tickets that breached SLA targets."""
    breaches = []

    for ticket in tickets:
        if ticket['status'] not in ('Resolved', 'Closed'):
            continue

        sla = calculate_sla_status(ticket)
        if sla.get('response_met') is False or sla.get('resolution_met') is False:
            breach = dict(ticket)
            breach['sla_status'] = sla
            breaches.append(breach)

    return breaches


@app.get("/api/dashboard/summary")
def get_dashboard_summary(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    agent_id: Optional[str] = None,
    month: Optional[str] = None
):
    """Get summary statistics for dashboard with optional filtering."""
    filtered = apply_filters(tickets, status, priority, category, agent_id)
    filtered = filter_by_month(filtered, month)

    open_statuses = ('Open', 'In Progress', 'Escalated')
    open_tickets = len([t for t in filtered if t['status'] in open_statuses])

    resolved = [t for t in filtered if t['status'] in ('Resolved', 'Closed')]
    avg_resolution_hours = 0
    if resolved:
        total_hours = 0
        count = 0
        for t in resolved:
            if t.get('resolved_at') and t.get('created_at'):
                created = datetime.fromisoformat(t['created_at'])
                resolved_dt = datetime.fromisoformat(t['resolved_at'])
                total_hours += (resolved_dt - created).total_seconds() / 3600
                count += 1
        if count > 0:
            avg_resolution_hours = round(total_hours / count, 1)

    sla_met = 0
    sla_total = 0
    for t in resolved:
        sla = calculate_sla_status(t)
        if sla.get('resolution_met') is not None:
            sla_total += 1
            if sla['resolution_met']:
                sla_met += 1
    sla_compliance_pct = round((sla_met / sla_total * 100), 1) if sla_total > 0 else 0

    busy_agents = len([a for a in agents if a['status'] == 'Busy'])
    total_agents = len(agents)
    agent_utilization = round((busy_agents / total_agents * 100), 1) if total_agents > 0 else 0

    status_distribution = {}
    for t in filtered:
        s = t['status']
        status_distribution[s] = status_distribution.get(s, 0) + 1

    priority_distribution = {}
    for t in filtered:
        p = t['priority']
        priority_distribution[p] = priority_distribution.get(p, 0) + 1

    recent = sorted(filtered, key=lambda t: t.get('created_at', ''), reverse=True)[:5]

    return {
        'open_tickets': open_tickets,
        'avg_resolution_hours': avg_resolution_hours,
        'sla_compliance_pct': sla_compliance_pct,
        'agent_utilization': agent_utilization,
        'total_tickets': len(filtered),
        'resolved_tickets': len(resolved),
        'status_distribution': status_distribution,
        'priority_distribution': priority_distribution,
        'recent_tickets': recent
    }


@app.get("/api/reports/monthly-trends")
def get_monthly_trends():
    """Get month-over-month ticket trends."""
    months = {}

    for ticket in tickets:
        created = ticket.get('created_at', '')
        if not created:
            continue

        month = created[:7]

        if month not in months:
            months[month] = {
                'month': month,
                'created_count': 0,
                'resolved_count': 0,
                'escalated_count': 0
            }

        months[month]['created_count'] += 1

        if ticket['status'] in ('Resolved', 'Closed'):
            resolved_month = (ticket.get('resolved_at') or '')[:7]
            if resolved_month and resolved_month in months:
                months[resolved_month]['resolved_count'] += 1
            elif resolved_month:
                months[resolved_month] = {
                    'month': resolved_month,
                    'created_count': 0,
                    'resolved_count': 1,
                    'escalated_count': 0
                }

    for esc in escalations:
        esc_month = (esc.get('escalated_at') or '')[:7]
        if esc_month in months:
            months[esc_month]['escalated_count'] += 1

    result = list(months.values())
    result.sort(key=lambda x: x['month'])
    return result


@app.get("/api/reports/agent-performance")
def get_agent_performance():
    """Get performance metrics for each agent."""
    result = []

    for agent in agents:
        agent_tickets = [t for t in tickets if t.get('assigned_to') == agent['id']]
        resolved = [t for t in agent_tickets if t['status'] in ('Resolved', 'Closed')]
        agent_ratings = [r for r in satisfaction_ratings if r.get('agent_id') == agent['id']]

        avg_resolution_hours = 0
        if resolved:
            total_hours = 0
            count = 0
            for t in resolved:
                if t.get('resolved_at') and t.get('created_at'):
                    created = datetime.fromisoformat(t['created_at'])
                    resolved_dt = datetime.fromisoformat(t['resolved_at'])
                    total_hours += (resolved_dt - created).total_seconds() / 3600
                    count += 1
            if count > 0:
                avg_resolution_hours = round(total_hours / count, 1)

        avg_satisfaction = 0
        if agent_ratings:
            avg_satisfaction = round(sum(r['rating'] for r in agent_ratings) / len(agent_ratings), 1)

        sla_met = 0
        for t in resolved:
            sla = calculate_sla_status(t)
            if sla.get('resolution_met'):
                sla_met += 1

        result.append({
            'agent_id': agent['id'],
            'agent_name': agent['name'],
            'role': agent['role'],
            'total_assigned': len(agent_tickets),
            'total_resolved': len(resolved),
            'open_tickets': len(agent_tickets) - len(resolved),
            'avg_resolution_hours': avg_resolution_hours,
            'avg_satisfaction': avg_satisfaction,
            'sla_compliance_pct': round((sla_met / len(resolved) * 100), 1) if resolved else 0
        })

    return result


@app.get("/api/satisfaction/summary")
def get_satisfaction_summary():
    """Get customer satisfaction summary statistics."""
    if not satisfaction_ratings:
        return {'avg_rating': 0, 'total_ratings': 0, 'distribution': {}}

    total = len(satisfaction_ratings)
    avg = round(sum(r['rating'] for r in satisfaction_ratings) / total, 2)

    distribution = {str(i): 0 for i in range(1, 6)}
    for r in satisfaction_ratings:
        distribution[str(r['rating'])] = distribution.get(str(r['rating']), 0) + 1

    recent = sorted(satisfaction_ratings, key=lambda r: r.get('submitted_at', ''), reverse=True)[:5]

    return {
        'avg_rating': avg,
        'total_ratings': total,
        'distribution': distribution,
        'recent_ratings': recent
    }


@app.get("/api/categories", response_model=List[Category])
def get_categories():
    """Get all ticket categories."""
    return categories


@app.get("/api/tickets/{ticket_id}/comments", response_model=List[Comment])
def get_ticket_comments(ticket_id: str):
    """Get all comments for a ticket."""
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return [c for c in comments if c["ticket_id"] == ticket_id]


@app.post("/api/tickets/{ticket_id}/comments", response_model=Comment)
def create_ticket_comment(ticket_id: str, request: CreateCommentRequest):
    """Add a comment to a ticket."""
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    new_comment = {
        "id": f"CMT-{len(comments) + 1:03d}",
        "ticket_id": ticket_id,
        "author_name": request.author_name,
        "author_email": request.author_email,
        "body": request.body,
        "created_at": datetime.now().isoformat(timespec='seconds')
    }
    comments.append(new_comment)
    return new_comment


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
