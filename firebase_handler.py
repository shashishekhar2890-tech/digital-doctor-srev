import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import os
import json

# Mock database for demonstration if Firebase creds are missing
MOCK_DB = []

def initialize_firebase():
    """Initializes Firebase app or sets up mock if credentials missing."""
    try:
        # Check if we have credentials (e.g., in env var or file)
        cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            return firestore.client()
        else:
            print("No Firebase credentials found. Using Mock DB.")
            return None
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return None

def save_patient_file(data):
    """Saves the audit data to Firestore or Mock DB."""
    db = initialize_firebase()
    
    # Add timestamp
    data['created_at'] = datetime.datetime.now().isoformat()
    data['patient_id'] = f"pat_{int(datetime.datetime.now().timestamp())}"
    
    if db:
        try:
            db.collection('Patient_Audit').add(data)
            return True, "Saved to Firestore"
        except Exception as e:
            return False, f"Firestore Error: {e}"
    else:
        # Save to Local JSON File (Persistent Mock DB)
        try:
            filename = "srev_db.json"
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    try:
                        current_db = json.load(f)
                    except: 
                        current_db = []
            else:
                current_db = []
            
            current_db.append(data)
            
            with open(filename, "w") as f:
                json.dump(current_db, f, indent=4)
                
            return True, "Saved to Local Admin DB"
        except Exception as e:
            return False, f"Local DB Error: {e}"

def get_all_records():
    """Retrieves all records from Local DB or Firestore."""
    db = initialize_firebase()
    if db:
        # Fetch from Firestore (Simplification)
        return [] 
    else:
        # Fetch from Local File
        if os.path.exists("srev_db.json"):
            with open("srev_db.json", "r") as f:
                try:
                    return json.load(f)
                except:
                    return []
        return []

def trigger_admin_email(data):
    """Simulates sending an email to the admin."""
    # In production, use SendGrid or SMTP
    print(f"--- EMAIL TRIGGERED ---")
    print(f"To: admin@srev-evolution.com")
    print(f"Subject: New Digital Biopsy for {data.get('hospital_info', {}).get('name')}")
    print(f"Body: Health Score {data.get('health_score')}%")
    print("-----------------------")
    return True
