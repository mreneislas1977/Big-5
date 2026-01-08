import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# 1. Load variables from .env (for local testing)
load_dotenv()

# 2. Initialize Firebase
# This logic allows the code to work on BOTH your computer and the Cloud
if not firebase_admin._apps:
    
    # PRIORITY 1: Check for Cloud Environment Variables (Production)
    if os.environ.get("FIREBASE_PRIVATE_KEY"):
        cred_dict = {
            "type": "service_account",
            "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
            "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
            "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
            "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_CERT_URL")
        }
        cred = credentials.Certificate(cred_dict)
        print("Firebase initialized with Environment Variables (Cloud Mode).")
        
    # PRIORITY 2: Check for local JSON file (Local Development)
    elif os.path.exists("serviceAccountKey.json"):
        cred = credentials.Certificate("serviceAccountKey.json")
        print("Firebase initialized with local JSON file (Local Mode).")
        
    else:
        # If neither exists, stop everything.
        raise ValueError("CRITICAL ERROR: No Firebase credentials found! Set environment variables or add serviceAccountKey.json.")

    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- Database Methods (These remain exactly the same) ---
class FirestoreDB:
    
    @staticmethod
    def save_assessment(user_data, assessment_results, raw_answers):
        # Prepare Data
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
            "created_at": firestore.SERVER_TIMESTAMP # Use server time for accuracy
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
            "created_at": firestore.SERVER_TIMESTAMP
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
