#!/bin/bash
if [ ! -d "mlenv" ]; then
    python3 -m venv mlenv
fi
source mlenv/bin/activate
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    (sleep 3; xdg-open "http://127.0.0.1:8000/login") &
elif [[ "$OSTYPE" == "darwin"* ]]; then
    (sleep 3; open "http://127.0.0.1:8000/login") &
fi
uvicorn src.main:app --reload