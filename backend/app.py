from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_model.predictor import JobPredictor

# Initialize Flask app
app = Flask(__name__)

# Configure CORS with proper settings
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8000", "http://localhost:5000", "http://127.0.0.1:8000", "http://127.0.0.1:5000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Initialize predictor
predictor = JobPredictor()

@app.route('/api/predict', methods=['POST', 'OPTIONS'])
def predict():
    """
    Predict whether a job posting is fake or real.
    
    Request JSON:
    {
        "job_description": "string"
    }
    
    Response JSON:
    {
        "prediction": "fake" or "real",
        "confidence": 0.0 to 1.0,
        "indicators": [
            {
                "type": "fake" or "real",
                "text": "indicator text"
            }
        ]
    }
    """
    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body cannot be empty'}), 400
            
        job_description = data.get('job_description', '').strip()

        if not job_description:
            return jsonify({'error': 'Job description cannot be empty'}), 400

        # Get prediction
        prediction, confidence, indicators = predictor.predict(job_description)
        
        # Ensure we have valid output
        if prediction is None or confidence is None:
            return jsonify({'error': 'Failed to generate prediction'}), 500

        return jsonify({
            'prediction': prediction,
            'confidence': float(confidence),
            'indicators': indicators if indicators else []
        }), 200

    except Exception as e:
        print(f"Error in predict endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health():
    """Health check endpoint."""
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    return jsonify({'status': 'healthy', 'message': 'API is running and ready'}), 200

@app.route('/', methods=['GET'])
def home():
    """Root endpoint."""
    return jsonify({
        'name': 'JobVision API',
        'version': '1.0.0',
        'description': 'Fake Job Detector using ML',
        'endpoints': {
            'predict': 'POST /api/predict',
            'health': 'GET /api/health'
        }
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting JobVision API...")
    print("=" * 60)
    print("✅ CORS enabled for http://localhost:8000")
    print("📡 API endpoints available:")
    print("   - GET  http://localhost:5000/api/health")
    print("   - POST http://localhost:5000/api/predict")
    print("=" * 60)
    print("⚠️  Make sure the ML model is trained (models/model.pkl exists)")
    print("=" * 60)
    app.run(debug=False, host='0.0.0.0', port=5000)
