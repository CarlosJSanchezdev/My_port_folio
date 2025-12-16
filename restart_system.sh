#!/bin/bash
# Restart script for Portfolio System

echo "🛑 Deteniendo procesos existentes..."
pkill -f "ng serve"
pkill -f "python3 run_local.py"

echo "✅ Procesos detenidos."
sleep 2

echo "🚀 Iniciando Backend (Puerto 5001)..."
cd backend
source .venv/bin/activate
nohup python3 run_local.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

echo "⏳ Esperando a que el backend inicie..."
sleep 5

echo "🚀 Iniciando Frontend (Puerto 4200)..."
cd ..
nohup ng serve > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

echo ""
echo "🎉 Sistema reiniciado exitosamente!"
echo "    Backend: http://localhost:5001"
echo "   Frontend: http://localhost:4200"
echo ""
echo "📝 Logs disponibles en backend/backend.log y frontend.log"
echo ""
