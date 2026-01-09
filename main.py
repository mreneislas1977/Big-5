from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

# Allow connections from your dashboard
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Big 5 Executive Assessment</title>
            <style>
                body { font-family: sans-serif; text-align: center; padding-top: 50px; }
                .status { background-color: #dcfce7; color: #166534; padding: 10px 20px; border-radius: 20px; font-weight: bold; display: inline-block;}
            </style>
        </head>
        <body>
            <h1>Big 5 Executive Profile</h1>
            <div class="status">System Operational</div>
            <p>Ready to connect to frontend.</p>
        </body>
    </html>
    """

@app.get("/health")
def health_check():
    return {"status": "ok"}
