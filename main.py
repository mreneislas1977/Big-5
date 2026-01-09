from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
[cite_start]from fastapi.staticfiles import StaticFiles # [cite: 1]
from fastapi.responses import FileResponse
import os

# Import your actual backend logic
from backend.assessment import BigFiveAssessment
from backend.team_engine import TeamAnalyzer

app = FastAPI()

# 1. CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. API Endpoints (The missing link between web and logic)
@app.post("/api/assess")
async def run_assessment(answers: dict):
    try:
        assessor = BigFiveAssessment()
        report = assessor.generate_full_report(answers)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "modules_loaded": ["assessment", "team_engine"]}

# 3. Serve Frontend (Must be last)
# Check if the build directory exists before trying to mount it
if os.path.exists("frontend/dist"):  # Ensure your React build outputs to 'dist' or 'build'
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
else:
    # Fallback if frontend isn't built yet
    @app.get("/")
    def read_root():
        return {"status": "Backend running, but frontend build not found."}
