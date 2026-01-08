from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # <--- MAKE SURE THIS IS IMPORTED
from pydantic import BaseModel
from typing import List, Dict

# ... keep your existing imports (assessment, team_engine, etc.) ...

app = FastAPI(title="Big Five Team OS")

# --- SECURITY CONFIGURATION (CORS) ---
origins = [
    "http://localhost:3000",                      # 1. Local Development
    "https://big-five-assessment-app.vercel.app", # 2. Your Vercel Frontend (REPLACE THIS with your actual Vercel URL)
    "https://crescere-strat.com",                 # 3. Your Main Website
    "https://www.crescere-strat.com"              # 4. Your Main Website (WWW version)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],    # Allows all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],    # Allows all headers (Authentication, JSON, etc.)
)

# ... The rest of your code (Data Models and Routes) stays the same ...
