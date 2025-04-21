#!/bin/bash

stop_servers() {
    echo "Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

echo "Starting backend..."
cd "$(dirname "$0")" || exit 1
uvicorn GUI.backend.server:app --reload &
BACKEND_PID=$!

echo "Starting frontend..."
cd GUI/frontend || exit 1
npm run dev &
FRONTEND_PID=$!

trap 'stop_servers' SIGINT
echo "Press Ctrl+C to stop the servers..."
wait