import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# --- 1. NEW: Import Firestore ---
from google.cloud import firestore

app = FastAPI()

# --- 2. NEW: Initialize Database ---
# (Google Cloud automatically handles authentication)
try:
    db = firestore.Client()
except Exception as e:
    print(f"Warning: Firestore not connected. {e}")
    db = None

# Load Questions & Profiles
with open("data/questions.json", "r") as f:
    questions_data = json.load(f)

with open("data/profiles.json", "r") as f:
    profiles_data = json.load(f)

from backend.assessment import calculate_big5_scores, determine_archetype

class SurveyResponse(BaseModel):
    name: str
    email: str
    answers: Dict[str, int]

@app.get("/api/questions")
def get_questions():
    return questions_data

@app.post("/api/submit")
def submit_survey(response: SurveyResponse):
    # 1. Calculate Scores
    scores = calculate_big5_scores(response.answers)
    
    # 2. Determine Archetype
    archetype_result = determine_archetype(scores, profiles_data)
    
    # 3. Create the Record
    user_record = {
        "name": response.name,
        "email": response.email,
        "scores": scores,
        "archetype": archetype_result["archetype"],
        "timestamp": firestore.SERVER_TIMESTAMP
    }

    # --- 4. NEW: Save to Firestore ---
    if db:
        try:
            # Save to a collection named 'assessments'
            db.collection("assessments").add(user_record)
            print(f"Saved result for {response.email}")
        except Exception as e:
            print(f"Failed to save to Firestore: {e}")

    return {
        "status": "success",
        "report": archetype_result
    }

# Serve Frontend
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
