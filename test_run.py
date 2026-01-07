from backend.assessment import BigFiveAssessment
from backend.firebase_db import FirestoreDB
from backend.team_engine import TeamAnalyzer
import random
import time

def generate_random_answers(skew="random"):
   answers = {}
   traits = ["EXT", "AGR", "CSN", "EST", "OPN"]
   for t in traits:
       for i in range(1, 11): 
           val = random.randint(1, 5)
           if skew == "high_openness" and t == "OPN": val = 5
           if skew == "low_conscientiousness" and t == "CSN": val = 1
           answers[f"{t}_{i}"] = val
   return answers

def main():
   print("--- 1. Simulating 4 Executives ---")
   users = [
       {"name": "Alice (CEO)", "skew": "high_openness"},
       {"name": "Bob (CTO)", "skew": "high_openness"},
       {"name": "Charlie (CFO)", "skew": "low_conscientiousness"},
       {"name": "Dana (CMO)", "skew": "random"}
   ]
   
   doc_ids = []
   assessor = BigFiveAssessment()

   for u in users:
       print(f"Processing {u['name']}...")
       answers = generate_random_answers(u['skew'])
       report = assessor.generate_full_report(answers)
       print(f"   -> Archetype: {report['archetype']}")
       
       doc_id = FirestoreDB.save_assessment(
           {"name": u['name'], "email": f"{u['name'].split()[0].lower()}@test.com"},
           report, answers
       )
       doc_ids.append(doc_id)
       time.sleep(1)

   print("\n--- 2. Building the Team ---")
   analyzer = TeamAnalyzer()
   profile_ids = [FirestoreDB.get_user_profile_id(did) for did in doc_ids]
   charter = analyzer.generate_team_charter(profile_ids)
   
   print("\n[TEAM ANALYSIS RESULT]")
   print(f"DNA: {charter['team_fingerprint']}")
   for rule in charter['operating_principles']:
       print(f" - RULE: {rule['Rule']}")

   print("\n--- 3. Saving to Firebase ---")
   team_id = FirestoreDB.save_team("The Executive Simulation", doc_ids, charter)
   print(f"Team saved. ID: {team_id}")

if __name__ == "__main__":
   main()

Sources
1. https://support.backendless.com/t/problems-building-custom-component/17022
2. https://support.backendless.com/t/problems-building-custom-component/17022
