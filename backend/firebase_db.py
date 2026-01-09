import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

# --- SAFE INITIALIZATION ---
db = None
try:
    if os.environ.get("FIREBASE_PRIVATE_KEY"):
        # Cloud Mode
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
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("SUCCESS: Connected to Firebase Database.")
    elif os.path.exists("serviceAccountKey.json"):
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("SUCCESS: Connected to Firebase (Local).")
    else:
        print("WARNING: No Database Credentials found. Running in OFFLINE MODE.")
except Exception as e:
    print(f"WARNING: Database connection failed ({e}). Running in OFFLINE MODE.")
    db = None

class FirestoreDB:
    @staticmethod
    def save_assessment(user_data, assessment_results, raw_answers):
        if db is None:
            print("OFFLINE MODE: Skipping database save.")
            return "offline_id_123"
        try:
            doc_data = {
                "user_info": user_data,
                "profile": assessment_results,
                "raw_answers": raw_answers,
                "created_at": firestore.SERVER_TIMESTAMP
            }
            update_time, doc_ref = db.collection('assessments').add(doc_data)
            return doc_ref.id
        except Exception as e:
            print(f"Error saving to DB: {e}")
            return "error_id"

    @staticmethod
    def save_team(team_name, member_ids, team_analysis):
        if db is None:
            return "offline_team_id"
        try:
            doc_data = {
                "name": team_name,
                "members": member_ids,
                "dna": team_analysis,
                "created_at": firestore.SERVER_TIMESTAMP
            }
            update_time, doc_ref = db.collection('teams').add(doc_data)
            return doc_ref.id
        except Exception as e:
            return "error_team_id"

    @staticmethod
    def get_user_profile_id(doc_id):
        if db is None: return 0
        try:
            doc = db.collection('assessments').document(doc_id).get()
            if doc.exists: return doc.to_dict()['profile']['id']
        except: return None
        return None
