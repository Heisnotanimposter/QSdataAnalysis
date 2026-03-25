#!/bin/bash

echo "🚀 Starting QSdataAnalysis Servers..."

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "Port $1 is already in use"
        return 1
    else
        echo "Port $1 is available"
        return 0
    fi
}

# Start API Server
echo "📡 Starting API Server..."
cd "$(dirname "$0")/univrank-app/api"

if check_port 8000; then
    echo "Starting FastAPI server on port 8000..."
    python main.py &
    API_PID=$!
    echo "API Server PID: $API_PID"
    sleep 3
else
    echo "❌ API server is already running on port 8000"
fi

# Start Web App
echo "🌐 Starting Web App..."
cd "../"

if check_port 5173; then
    echo "Starting React app on port 5173..."
    npm run dev &
    WEB_PID=$!
    echo "Web App PID: $WEB_PID"
    sleep 3
else
    echo "❌ Web app is already running on port 5173"
fi

echo ""
echo "✅ Servers started successfully!"
echo "📊 API Server: http://localhost:8000"
echo "🌐 Web App: http://localhost:5173"
echo "📋 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for interrupt signal
trap 'echo "Stopping servers..."; kill $API_PID $WEB_PID 2>/dev/null; exit' INT
wait
