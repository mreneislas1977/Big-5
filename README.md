# Big-5
/big-five-app
├── requirements.txt
├── test_run.py
├── /data
│   ├── questions.json
│   └── profiles.json
├── /backend
│   ├── __init__.py         # (Empty file to make this a package)
│   ├── main.py             # The API Entry Point
│   ├── assessment.py       # Core Scoring Logic
│   ├── team_engine.py      # Team Analysis Logic
│   ├── comparator.py       # 1-on-1 Comparison Logic
│   ├── firebase_db.py      # Database Handler
│   └── pdf_generator.py    # PDF Creator
├── /frontend
│   ├── /src
│   │   ├── apiService.js
│   │   ├── scoring.js
│   │   ├── BigFiveChart.jsx
│   │   └── AssessmentView.jsx
Last updated: Jan 10
