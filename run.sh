#!/bin/sh

set -e
. .venv/bin/activate

# Run FastAPI backend
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload &

# Run Streamlit frontend
streamlit run streamlit_app.py &

# Wait for both processes to finish
wait
