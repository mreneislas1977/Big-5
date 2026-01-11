import json
import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Optional, List
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

app = FastAPI()

# --- DIAGNOSTIC LOG ---
# We store startup errors here so we can see them in the browser
startup_errors = []

# --- 1. SAFE DATABASE CONNECTION ---
db = None
try:
    from google.cloud import firestore
    db = firestore.Client()
except Exception as e:
    startup_errors.append(f"Database Warning: {str(e)}")

# --- 2. SAFE IMPORTS ---
try:
    # Attempt to import the calculation logic
    from backend.assessment import calculate_big5_scores, determine_archetype
except Exception as e:
    startup_errors.append(f"Import Error (Backend): {str(e)}")
    # specific dummy functions so the app doesn't crash if backend is missing
    def calculate_big5_scores(answers): return {"error": "backend_missing"}
    def determine_archetype(scores, profiles): return {"archetype": "System Error", "description": "Please check logs."}

# --- 3. SAFE DATA LOADING ---
questions_data = []
profiles_data = {}

try:
    if os.path.exists("data/questions.json"):
        with open("data/questions.json", "r") as f:
            questions_data = json.load(f)
    else:
        startup_errors.append("Critical: data/questions.json not found.")

    if os.path.exists("data/profiles.json"):
        with open("data/profiles.json", "r") as f:
            profiles_data = json.load(f)
    else:
        startup_errors.append("Critical: data/profiles.json not found.")
except Exception as e:
    startup_errors.append(f"Data Loading Error: {str(e)}")

# --- DATA MODELS ---
class SurveyResponse(BaseModel):
    name: str
    email: str
    answers: Dict[str, int]

# --- API ENDPOINTS ---

@app.get("/api/questions")
def get_questions():
    if not questions_data:
        return [{"id": "error", "text": "System Error: Questions file missing.", "questions": []}]
    return questions_data

@app.post("/api/submit")
def submit_survey(response: SurveyResponse):
    # 1. Calculate
    scores = calculate_big5_scores(response.answers)
    
    # 2. Archetype
    archetype_result = determine_archetype(scores, profiles_data)
    
    # 3. Save (Safe Mode)
    if db:
        try:
            user_record = {
                "name": response.name,
                "email": response.email,
                "scores": scores,
                "archetype": archetype_result.get("archetype", "Unknown"),
                "timestamp": firestore.SERVER_TIMESTAMP
            }
            db.collection("assessments").add(user_record)
        except Exception as e:
            print(f"Failed to save: {e}")

    return {"status": "success", "report": archetype_result}

@app.get("/api/admin/results")
def get_team_results(admin_key: Optional[str] = Header(None)):
    if admin_key != "crescere-secret-key": 
        raise HTTPException(status_code=403, detail="Unauthorized")
    if not db:
        return []
    
    try:
        docs = db.collection("assessments").stream()
        results = []
        for doc in docs:
            data = doc.to_dict()
            if "timestamp" in data:
                data["timestamp"] = str(data["timestamp"])
            results.append(data)
        return results
    except Exception as e:
        return [{"error": str(e)}]

# --- NEW: DEBUG ENDPOINT ---
# Go here if the site looks broken to see WHY
@app.get("/api/debug")
def debug_system():
    return {
        "status": "online",
        "errors": startup_errors,
        "questions_loaded": len(questions_data),
        "profiles_loaded": len(profiles_data),
        "database_connected": db is not None
    }

# Serve Frontend
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
