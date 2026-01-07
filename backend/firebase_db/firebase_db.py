import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

# Initialize Firebase
# Ensure 'serviceAccountKey.json' is in your project root
if not firebase_admin._apps:
   cred = credentials.Certificate('serviceAccountKey.json') 
   firebase_admin.initialize_app(cred)

db = firestore.client()

class FirestoreDB:
   
    @staticmethod
   def save_assessment(user_data, assessment_results, raw_answers):
       doc_data = {
           "user_info": {
               "name": user_data.get('name'),
               "email": user_data.get('email')
           },
           "profile": {
               "id": assessment_results['profile_id'],
               "archetype": assessment_results['archetype'],
               "scores": assessment_results['scores'],
               "description": assessment_results['description'],
               "recommendation": assessment_results['recommendation']
           },
           "raw_answers": raw_answers,
           "created_at": datetime.now()
       }

       update_time, doc_ref = db.collection('assessments').add(doc_data)
       print(f"Assessment saved with ID: {doc_ref.id}")
       return doc_ref.id

    @staticmethod
   def save_team(team_name, member_ids, team_analysis):
       doc_data = {
           "name": team_name,
           "members": member_ids,
           "dna": team_analysis['team_fingerprint'],
           "operating_principles": team_analysis['operating_principles'],
           "created_at": datetime.now()
       }

       update_time, doc_ref = db.collection('teams').add(doc_data)
       print(f"Team saved with ID: {doc_ref.id}")
       return doc_ref.id

    @staticmethod
   def get_user_profile_id(doc_id):
       doc = db.collection('assessments').document(doc_id).get()
       if doc.exists:
           return doc.to_dict()['profile']['id']
       return None
