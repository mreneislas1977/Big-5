from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import traceback # Added for debugging

# Import backend logic
from backend.assessment import BigFiveAssessment
from backend.team_engine import TeamAnalyzer
from backend.firebase_db import FirestoreDB

app = FastAPI()

# Input Models
class AssessmentRequest(BaseModel):
    name: str
    email: str
    answers: dict

class TeamRequest(BaseModel):
    team_name: str
    member_doc_ids: list

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
    # --- DEBUG WRAPPER START ---
    try:
        print(f"Received assessment request for: {payload.email}")
        
        # 1. Initialize Logic
        assessor = BigFiveAssessment()
        
        # 2. Generate Report
        report = assessor.generate_full_report(payload.answers)
        
        # 3. Save to DB (Safe Mode handles the crash if offline)
        doc_id = FirestoreDB.save_assessment(
            {"name": payload.name, "email": payload.email},
            report, 
            payload.answers
        )
        
        return {"id": doc_id, "report": report}

    except Exception as e:
        # If ANYTHING crashes, we catch it here and send it to the browser
        error_details = traceback.format_exc()
        print(f"CRASH DETECTED: {error_details}")
        # Return a 200 OK with the error details so the frontend can see it
        return {
            "error": "Backend Crash",
            "message": str(e),
            "traceback": error_details
        }
    # --- DEBUG WRAPPER END ---

@app.post("/api/team")
async def analyze_team(payload: TeamRequest):
    try:
        analyzer = TeamAnalyzer()
        profile_ids = []
        for doc_id in payload.member_doc_ids:
            pid = FirestoreDB.get_user_profile_id(doc_id)
            if pid:
                profile_ids.append(pid)
        
        charter = analyzer.generate_team_charter(profile_ids)
        team_id = FirestoreDB.save_team(payload.team_name, payload.member_doc_ids, charter)
        return {"team_id": team_id, "charter": charter}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- SERVE FRONTEND ---
if os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
else:
    @app.get("/")
    def read_root():
        return {"status": "Backend running. Frontend build not found."}
