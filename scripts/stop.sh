#!/bin/bash

# Stop the IT Help Desk application

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Stopping IT Help Desk application...${NC}"

# Stop backend
if [ -f /tmp/helpdesk-backend.pid ]; then
    kill "$(cat /tmp/helpdesk-backend.pid)" 2>/dev/null
    rm -f /tmp/helpdesk-backend.pid
    echo -e "${GREEN}Backend stopped${NC}"
else
    echo "No backend PID file found"
fi

# Stop frontend
if [ -f /tmp/helpdesk-frontend.pid ]; then
    kill "$(cat /tmp/helpdesk-frontend.pid)" 2>/dev/null
    rm -f /tmp/helpdesk-frontend.pid
    echo -e "${GREEN}Frontend stopped${NC}"
else
    echo "No frontend PID file found"
fi

# Fallback: kill by port
lsof -ti:3000,8001 | xargs kill -9 2>/dev/null || true

echo -e "${GREEN}All processes stopped${NC}"
