# PocketSmart AI

PocketSmart AI is a Flask web application with three planners:
- Home Interior Planner
- Party Planner
- Jewelry Planner

## 1. Create virtual environment

Windows:
```powershell
python -m venv .venv
.venv\Scripts\activate
```

## 2. Install packages
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Run immediately in demo mode

The included `.env` starts in mock mode, so an API key is not required for the first run.

```powershell
python app.py
```

Open:
http://127.0.0.1:5000

Health:
http://127.0.0.1:5000/api/health

## 4. Run tests
```powershell
pytest -q
```

## 5. Enable Gemini

Put your Gemini API key in `.env`:
```text
GEMINI_API_KEY=your_key_here
USE_MOCK_AI=false
```

If the selected model is unavailable for your account/API, change `GEMINI_MODEL` to a model available in your Google AI Studio/API account.

Never commit `.env` or your API key to GitHub.
