# JobVision - Fake Job Detector

**Detect fraudulent job postings instantly using Machine Learning!**

## Project Overview

JobVision is a web-based ML application that analyzes job descriptions to identify fake and suspicious job postings. Using Natural Language Processing (NLP) and Logistic Regression, it provides instant predictions with confidence scores and key indicators.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Sample Training Data
```bash
python data/generate_sample_data.py
```

### 3. Train the ML Model
```bash
python train_model.py
```

### 4. Test the Predictor
```bash
python test_predictor.py
```

### 5. Start the Backend API
```bash
python backend/app.py
```

The API will run on `http://localhost:5000`

### 6. Open the Web Interface
Open `frontend/index.html` in your web browser.

Paste a job description and click "Predict Job Reality" to get instant results!

## Project Structure

```
fakejob/
├── frontend/                 # Web UI
│   ├── index.html           # Main HTML page
│   ├── styles.css           # Styling
│   └── script.js            # JavaScript logic
├── backend/                 # Flask API
│   └── app.py               # API endpoints
├── ml_model/                # Machine Learning
│   ├── trainer.py           # Model training & preprocessing
│   ├── predictor.py         # Prediction engine
│   └── __init__.py
├── models/                  # Trained models
│   ├── model.pkl            # Logistic Regression model
│   └── vectorizer.pkl       # TF-IDF vectorizer
├── data/                    # Datasets
│   ├── fake_job_postings.csv
│   └── generate_sample_data.py
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── train_model.py          # Training script
└── test_predictor.py       # Testing script
```

## Features

### 🎯 Core Features
- **Real-time Prediction**: Analyze job postings instantly
- **Confidence Score**: Get confidence percentages for predictions
- **Key Indicators**: See why a job is marked as suspicious
- **Rule-Based Fallback**: Works even without trained model

### 🔧 Technical Features
- **TF-IDF Vectorization**: Advanced text feature extraction
- **Logistic Regression**: Fast and interpretable ML model
- **NLTK Preprocessing**: Text cleaning, tokenization, lemmatization
- **Flask REST API**: Clean API endpoints
- **CORS Enabled**: Cross-origin requests supported

## Machine Learning Pipeline

### Data Preprocessing
1. **Text Cleaning**: Remove URLs, emails, special characters
2. **Tokenization**: Split text into words
3. **Stopword Removal**: Remove common English words
4. **Lemmatization**: Normalize word variations

### Feature Engineering
- **TF-IDF Vectorization**: Convert text to 5000-dimensional vectors
- **Text Combination**: Merge title, description, and requirements

### Model Training
- **Algorithm**: Logistic Regression
- **Train-Test Split**: 80-20 ratio
- **Evaluation Metrics**: Accuracy, Precision, Recall, F1-Score

## API Endpoints

### POST /api/predict
Predict if a job posting is fake or real.

**Request:**
```json
{
    "job_description": "Your job posting text here..."
}
```

**Response:**
```json
{
    "prediction": "real",
    "confidence": 0.92,
    "indicators": [
        {
            "type": "real",
            "text": "\"detailed job description\" detected"
        },
        {
            "type": "real",
            "text": "\"salary range\" detected"
        }
    ]
}
```

### GET /api/health
Health check endpoint.

### GET /
API information endpoint.

## Suspicious Indicators

### 🚨 Fake Job Indicators
- "No experience needed"
- "Immediate cash/payment"
- "Guaranteed income"
- "Work from home with no experience"
- "No interview"
- "Easy money"
- "Risk-free"
- "Upfront payment/fee"
- "Get paid today"

### ✅ Real Job Indicators
- Company website/address/phone
- Detailed job description
- Specific requirements
- Years of experience required
- Educational requirements
- Salary range
- Benefits listed
- Professional hiring process

## Technologies Used

### Frontend
- HTML5
- CSS3 (with Flexbox & Grid)
- Vanilla JavaScript
- Responsive Design

### Backend
- Python 3.8+
- Flask 2.3.0
- Flask-CORS

### Machine Learning
- scikit-learn (ML models, feature extraction)
- pandas (Data manipulation)
- NumPy (Numerical computing)
- NLTK (Natural Language Processing)

## Model Performance

Typical metrics from training:
- **Accuracy**: 92-96%
- **Precision**: 90-95%
- **Recall**: 88-94%
- **F1-Score**: 89-94%

*Metrics vary based on dataset composition*

## Advanced Enhancements (Optional)

1. **Deep Learning**: Use LSTM or BERT for better accuracy
2. **Explainable AI**: Highlight specific risky phrases
3. **User Authentication**: User accounts and history
4. **Browser Extension**: Detect fake jobs on job portals
5. **Real-time Scraping**: Automatically check job sites
6. **Multiple Models**: Ensemble approach with SVM & Random Forest

## Troubleshooting

### Model files not found
The model needs to be trained first. Run:
```bash
python train_model.py
```

### CORS errors
Ensure Flask-CORS is installed and the API is running on `http://localhost:5000`

### Port already in use
Change the port in `backend/app.py`:
```python
app.run(port=5001)  # Use different port
```

## Future Improvements

- [ ] Database integration for user predictions history
- [ ] Automated model retraining pipeline
- [ ] Advanced NLP models (BERT, GPT)
- [ ] Job portal browser extension
- [ ] Real-time job scraping and monitoring
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] A/B testing framework for model improvements

## License

MIT License - Feel free to use this project for learning and development.

## Author

Built as a demonstration of ML, NLP, and web development skills.

---

**Protect yourself from job scams!** 🛡️
