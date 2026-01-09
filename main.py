from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import traceback
import os

# --- IMPORT BACKEND ---
# We wrap imports in try/except to catch missing library errors
try:
    from backend.assessment import BigFiveAssessment
    from backend.team_engine import TeamAnalyzer
    from backend.firebase_db import FirestoreDB
except Exception as e:
    print(f"IMPORT ERROR: {e}")
    traceback.print_exc()

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

# --- DEBUG API ENDPOINT ---
@app.post("/api/assess")
async def run_assessment(payload: AssessmentRequest):
    print(f"DEBUG: Received request for {payload.email}")
    
    try:
        # 1. Test File Access (Common Crash Cause)
        if not os.path.exists("data/profiles.json"):
            raise FileNotFoundError("CRITICAL: 'data/profiles.json' is missing from the container!")
            
        # 2. Run Assessment
        assessor = BigFiveAssessment()
        report = assessor.generate_full_report(payload.answers)
        
        # 3. Save to DB
        doc_id = FirestoreDB.save_assessment(
            {"name": payload.name, "email": payload.email},
            report, 
            payload.answers
        )
        
        return {"id": doc_id, "report": report}

    except Exception as e:
        # CATCH THE CRASH
        error_msg = str(e)
        detailed_trace = traceback.format_exc()
        print(f"CRASH CAUGHT: {error_msg}")
        
        # Send 200 OK so the frontend displays the error instead of 'Submission Failed'
        return JSONResponse(
            status_code=200, 
            content={
                "report": {
                    "archetype": "SYSTEM ERROR",
                    "description": f"The server crashed with this error: {error_msg}",
                    "recommendation": "Please show this message to your developer.",
                    "scores": {"EXT":0, "AGR":0, "CSN":0, "EST":0, "OPN":0}
                }
            }
        )

@app.post("/api/team")
async def analyze_team(payload: TeamRequest):
    return {"status": "Team endpoints disabled in debug mode"}

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
