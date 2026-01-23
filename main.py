import json
import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Optional
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore

# --- IMPORT REAL BACKEND LOGIC ---
# We bring in the actual calculation engine and DB helper
from backend.assessment import BigFiveAssessment
from backend.firebase_db import FirestoreDB

app = FastAPI()

# --- 1. SAFE DATABASE CONNECTION ---
# We still keep the 'Safe Mode' check in case credentials aren't set up yet
try:
    if not FirestoreDB.client:
        FirestoreDB.client = firestore.Client()
except Exception as e:
    print(f"Warning: Database failed to connect. {e}")

# --- 2. INITIALIZE LOGIC ENGINE ---
assessor = BigFiveAssessment()

# --- 3. DATA LOADING (Questions) ---
questions_data = []
if os.path.exists("data/questions.json"):
    with open("data/questions.json", "r") as f:
        questions_data = json.load(f)
else:
    print("CRITICAL: questions.json not found. Using fallback.")
    questions_data = [{"id": "error", "questions": [{"id":"q1", "text":"Error: Questions file missing."}]}]

# --- DATA MODELS ---
class SurveyResponse(BaseModel):
    name: str
    email: str
    answers: Dict[str, int]

# --- API ENDPOINTS ---

@app.get("/api/questions")
def get_questions():
    return questions_data

@app.post("/api/submit")
def submit_survey(response: SurveyResponse):
    try:
        # 1. Run the Real Math (Calculates Scores + Archetype)
        report = assessor.generate_full_report(response.answers)

        # 2. Save to Database using your helper class
        # This handles the timestamp and structure automatically
        user_info = {"name": response.name, "email": response.email}
        doc_id = FirestoreDB.save_assessment(user_info, report, response.answers)

        # 3. Return the report to the frontend immediately
        return {"status": "success", "report": report, "id": doc_id}

    except Exception as e:
        print(f"Submission Failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/results")
def get_team_results(admin_key: Optional[str] = Header(None)):
    if admin_key != "crescere-secret-key": 
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # Use the helper to fetch raw data if possible, or direct stream
    try:
        docs = FirestoreDB.client.collection("assessments").stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        return []

# Serve Frontend (Must be last)
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
