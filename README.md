# Project Structure

## Directories

### `/frontend`
- `index.html` - Main HTML page
- `styles.css` - Styling
- `script.js` - Client-side JavaScript

### `/backend`
- `app.py` - Flask API server

### `/ml_model`
- `trainer.py` - Model training and data preprocessing
- `predictor.py` - Prediction logic and rule-based fallback

### `/models`
- `model.pkl` - Trained Logistic Regression model
- `vectorizer.pkl` - TF-IDF vectorizer

### `/data`
- `fake_job_postings.csv` - Training dataset
- `generate_sample_data.py` - Script to generate sample data

## Key Files

- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

## Workflow

1. **Data Generation**: Run `data/generate_sample_data.py` to create training data
2. **Model Training**: Use `ml_model/trainer.py` to train the ML model
3. **Backend Server**: Run `python backend/app.py` to start Flask API
4. **Frontend**: Open `frontend/index.html` in browser
5. **Make Predictions**: Submit job descriptions via web UI

## Next Steps

- Generate training data
- Train the ML model
- Start the Flask backend
- Open the web interface
