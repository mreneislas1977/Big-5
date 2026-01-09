from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

# --- IMPORT BACKEND LOGIC ---
from backend.assessment import BigFiveAssessment
from backend.team_engine import TeamAnalyzer
from backend.firebase_db import FirestoreDB

app = FastAPI()

# --- INPUT VALIDATION MODELS ---
# These ensure the data coming from React is exactly what we expect.
class AssessmentRequest(BaseModel):
    name: str
    email: str
    answers: dict

class TeamRequest(BaseModel):
    team_name: str
    member_doc_ids: list

# --- CORS SETUP ---
# Allows your React app to talk to this Python server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API ENDPOINTS ---

@app.post("/api/assess")
async def run_assessment(payload: AssessmentRequest):
    """
    Receives answers, calculates score, saves to DB, returns Report.
    """
    try:
        # 1. Run the Math
        assessor = BigFiveAssessment()
        report = assessor.generate_full_report(payload.answers)
        
        # 2. Save to Firebase
        doc_id = FirestoreDB.save_assessment(
            {"name": payload.name, "email": payload.email},
            report, 
            payload.answers
        )
        
        # 3. Return ID and Report to Frontend
        return {"id": doc_id, "report": report}

    except Exception as e:
        print(f"Error in /assess: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/team")
async def analyze_team(payload: TeamRequest):
    """
    Receives list of User IDs, analyzes team dynamics, saves to DB.
    """
    try:
        analyzer = TeamAnalyzer()
        
        # 1. Convert Document IDs to Profile IDs (needed for the bitwise logic)
        profile_ids = []
        for doc_id in payload.member_doc_ids:
            pid = FirestoreDB.get_user_profile_id(doc_id)
            if pid:
                profile_ids.append(pid)
        
        if not profile_ids:
            raise HTTPException(status_code=400, detail="No valid profiles found for these IDs.")
