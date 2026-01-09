from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict

# Initialize the App
app = FastAPI(title="Big Five Team OS")

# --- SECURITY CONFIGURATION (CORS) ---
# This allows your frontend to talk to this backend
origins = [
    "http://localhost:3000",
    "https://big-five-assessment-app.vercel.app", # Replace with your actual Vercel URL when ready
    "https://crescere-strat.com",
    "https://www.crescere-strat.com",
    "*" # TEMPORARY: Allows all connections for testing. Remove before final production.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    This is the default page that loads when you visit the URL.
    It confirms the API is running.
    """
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Big 5 Executive Assessment</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; text-align: center; padding-top: 50px; background-color: #f8fafc; color: #1e293b; }
                .container { background: white; max-width: 600px; margin: auto; padding: 40px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
                h1 { color: #0f172a; margin-bottom: 10px; }
                p { color: #64748b; line-height: 1.6; margin-bottom: 30px; }
                .status { display: inline-block; background-color: #dcfce7; color: #166534; padding: 6px 12px; border-radius: 9999px; font-weight: 600; font-size: 14px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Big 5 Executive Profile</h1>
                <p>The API is active and ready to process assessments.</p>
                <div class="status">● System Operational</div>
            </div>
        </body>
    </html>
    """

@app.get("/health")
def health_check():
    """Google Cloud Run checks this to see if the app is alive."""
    return {"status": "ok"}

# --- PLACEHOLDER FOR FUTURE LOGIC ---
# You will paste your assessment logic, scoring engine, and Firebase code below here later.
