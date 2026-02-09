# Running JobVision - Complete Setup Guide

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Step-by-Step Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Backend API (Terminal 1)
```bash
python backend/app.py
```

**Expected Output:**
```
============================================================
🚀 Starting JobVision API...
============================================================
✅ CORS enabled for http://localhost:8000
📡 API endpoints available:
   - GET  http://localhost:5000/api/health
   - POST http://localhost:5000/api/predict
============================================================
⚠️  Make sure the ML model is trained (models/model.pkl exists)
============================================================
 * Running on http://0.0.0.0:5000
```

### 3. Start the Frontend Server (Terminal 2)
```bash
python serve_frontend.py
```

**Expected Output:**
```
============================================================
🌐 Frontend server running at http://localhost:8000
============================================================
📌 Make sure the backend API is running:
   python backend/app.py
============================================================
Press CTRL+C to stop the server
============================================================
```

### 4. Open Browser
Visit: **http://localhost:8000**

---

## Troubleshooting

### Issue: "Cannot connect to API"
- Make sure the backend is running on Terminal 1
- Check firewall settings
- Verify ports 5000 and 8000 are not in use

### Issue: "API connection warning"
- Wait a few seconds for the backend to fully start
- Check console errors in browser DevTools (F12)

### Issue: "Model files not found"
- Run: `python train_model.py` to train the model
- Wait for completion, then restart the backend

### Checking API Health
Open in browser: **http://localhost:5000/api/health**

Should show:
```json
{
  "status": "healthy",
  "message": "API is running and ready"
}
```

---

## API Endpoints

### Health Check
- **URL:** `GET http://localhost:5000/api/health`
- **Response:** `{"status": "healthy", "message": "API is running and ready"}`

### Predict
- **URL:** `POST http://localhost:5000/api/predict`
- **Request Body:**
  ```json
  {
    "job_description": "Your job posting text here..."
  }
  ```
- **Response:**
  ```json
  {
    "prediction": "fake" or "real",
    "confidence": 0.95,
    "indicators": [
      {"type": "fake", "text": "\"no experience needed\" detected"},
      {"type": "real", "text": "\"salary range\" detected"}
    ]
  }
  ```

---

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:8000` (Frontend)
- `http://localhost:5000` (Direct API testing)
- `http://127.0.0.1:8000`
- `http://127.0.0.1:5000`

If you need to change these, edit [backend/app.py](backend/app.py) line 15-23.
