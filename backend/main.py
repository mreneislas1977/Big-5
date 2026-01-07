from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

# Local imports
from .assessment import BigFiveAssessment
from .team_engine import TeamAnalyzer
from .firebase_db import FirestoreDB

app = FastAPI(title="Big Five Team OS")

class AssessmentSubmission(BaseModel):
   name: str
   email: str
   answers: Dict[str, int]

class TeamRequest(BaseModel):
   team_name: str
   member_doc_ids: List[str]

@app.get("/")
def health_check():
   return {"status": "operational", "system": "Big Five OS"}

@app.post("/submit-assessment")
def submit_assessment(submission: AssessmentSubmission):
   try:
       assessor = BigFiveAssessment()
       full_report = assessor.generate_full_report(submission.answers)
       
       user_info = {"name": submission.name, "email": submission.email}
       doc_id = FirestoreDB.save_assessment(user_info, full_report, submission.answers)
       
       return {
           "message": "Success",
           "doc_id": doc_id,
           "report": full_report
       }
   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-team")
def analyze_team(request: TeamRequest):
   try:
       profile_ids = []
       for doc_id in request.member_doc_ids:
           pid = FirestoreDB.get_user_profile_id(doc_id)
           if pid is None:
               raise HTTPException(status_code=404, detail=f"User {doc_id} not found")
           profile_ids.append(pid)
           
       analyzer = TeamAnalyzer()
       team_charter = analyzer.generate_team_charter(profile_ids)
       
       team_id = FirestoreDB.save_team(request.team_name, request.member_doc_ids, team_charter)
       
       return {
           "team_id": team_id,
           "charter": team_charter
       }
   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))
