# SREV Digital Health Audit App

## Deployment Instructions

If you are deploying this app to Streamlit Cloud, ensure your repository contains **ALL** of the following files and folders. The `utils` folder is critical for the app to work.

### Required File Structure
```text
/ (Root Directory)
├── app.py                  <-- Main Application File
├── requirements.txt        <-- Dependencies
├── style.css               <-- Styling
├── ui_components.py        <-- UI Logic
├── run_app.bat             <-- Local Run Script
└── utils/                  <-- REQUIRED FOLDER
    ├── __init__.py
    ├── audit_logic.py
    └── firebase_handler.py
```

### Common Errors
**ModuleNotFoundError: No module named 'utils'**:
This means you did not upload the `utils` folder to GitHub. Ensure the folder and its contents are committed.
