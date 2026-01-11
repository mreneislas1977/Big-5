cd Big-5

cat > main.py <<EOF
import json
import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Optional
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore

app = FastAPI()

# --- 1. SAFE DATABASE CONNECTION ---
db = None
try:
    db = firestore.Client()
except Exception as e:
    print(f"Warning: Database failed to connect. {e}")

# --- 2. SAFE DATA LOADING ---
questions_data = []
profiles_data = {}

# We check if files exist before trying to open them
if os.path.exists("data/questions.json"):
    with open("data/questions.json", "r") as f:
        questions_data = json.load(f)
else:
    print("CRITICAL: questions.json not found")
    # Load dummy question so app doesn't look empty
    questions_data = [{"id": "error", "questions": [{"id":"q1", "text":"System Error: Data file missing. Please check logs."}]}]

if os.path.exists("data/profiles.json"):
    with open("data/profiles.json", "r") as f:
        profiles_data = json.load(f)

# --- 3. DUMMY BACKEND LOGIC (Prevents Import Crashes) ---
# We use simple logic here to ensure the server starts even if backend files are missing
def calculate_scores(answers):
    return {"stability": 3.0, "openness": 3.0, "conscientiousness": 3.0, "extraversion": 3.0, "agreeableness": 3.0}

def get_archetype(scores):
    return {"archetype": "System Online", "description": "The system is running in safe mode.", "recommendation": "Check logs."}

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
    scores = calculate_scores(response.answers)
    result = get_archetype(scores)
    
    if db:
        try:
            db.collection("assessments").add({
                "name": response.name,
                "email": response.email,
                "result": result,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
        except Exception as e:
            print(f"Save failed: {e}")

    return {"status": "success", "report": result}

@app.get("/api/admin/results")
def get_team_results(admin_key: Optional[str] = Header(None)):
    if admin_key != "crescere-secret-key": 
        raise HTTPException(status_code=403, detail="Unauthorized")
    if not db: return []
    
    docs = db.collection("assessments").stream()
    return [doc.to_dict() for doc in docs]

# Serve Frontend
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
EOF
