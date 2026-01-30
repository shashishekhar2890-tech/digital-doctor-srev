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
            db.collection('patient_files').add(data)
            return True, "Saved to Firestore"
        except Exception as e:
            return False, f"Firestore Error: {e}"
    else:
        # Mock Save
        MOCK_DB.append(data)
        # In a real app we can't persist mock data across restarts easily without a file, 
        # but for this session it's fine.
        return True, "Saved to Local Mock DB"

def trigger_admin_email(data):
    """Simulates sending an email to the admin."""
    # In production, use SendGrid or SMTP
    print(f"--- EMAIL TRIGGERED ---")
    print(f"To: admin@srev-evolution.com")
    print(f"Subject: New Digital Biopsy for {data.get('hospital_info', {}).get('name')}")
    print(f"Body: Health Score {data.get('health_score')}%")
    print("-----------------------")
    return True
