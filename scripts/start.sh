#!/bin/bash

# Start the IT Help Desk application (backend + frontend)

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}Starting IT Help Desk application...${NC}"

# Kill existing processes on ports
echo -e "${YELLOW}Cleaning up existing processes...${NC}"
lsof -ti:3000,8001 | xargs kill -9 2>/dev/null || true
sleep 1

# Start backend
echo -e "${BLUE}Starting backend (FastAPI on port 8001)...${NC}"
cd "$PROJECT_DIR/server"

if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    uv venv 2>/dev/null || python3 -m venv .venv
fi

if command -v uv &> /dev/null; then
    uv sync 2>/dev/null
    nohup uv run python main.py > /tmp/helpdesk-backend.log 2>&1 &
else
    source .venv/bin/activate
    pip install -r requirements.txt --quiet
    nohup python main.py > /tmp/helpdesk-backend.log 2>&1 &
fi
echo $! > /tmp/helpdesk-backend.pid
echo -e "${GREEN}Backend started (PID: $(cat /tmp/helpdesk-backend.pid))${NC}"

# Start frontend
echo -e "${BLUE}Starting frontend (Vite on port 3000)...${NC}"
cd "$PROJECT_DIR/client"

if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    npm install --silent
fi

nohup npm run dev > /tmp/helpdesk-frontend.log 2>&1 &
echo $! > /tmp/helpdesk-frontend.pid
echo -e "${GREEN}Frontend started (PID: $(cat /tmp/helpdesk-frontend.pid))${NC}"

sleep 2

echo ""
echo -e "${GREEN}IT Help Desk is running:${NC}"
echo -e "  Frontend: ${BLUE}http://localhost:3000${NC}"
echo -e "  Backend:  ${BLUE}http://localhost:8001${NC}"
echo -e "  API Docs: ${BLUE}http://localhost:8001/docs${NC}"
echo ""
echo -e "To stop: ${YELLOW}./scripts/stop.sh${NC}"
