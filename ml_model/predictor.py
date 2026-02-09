import pickle
import os
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Suspicious keywords and phrases
FAKE_JOB_INDICATORS = {
    'fake': [
        r'\bno\s+experience\b',
        r'\bimmediate\s+(cash|payment|hire)',
        r'\bguaranteed\s+income',
        r'\bwork\s+from\s+home.*\b(no|without|any)\s+(experience|qualification)',
        r'\bno\s+interview',
        r'\beasy\s+money',
        r'\brisk\s+free',
        r'\bno\s+experience\s+required',
        r'\bhigh\s+pay.*\bno\s+skill',
        r'\bphone\s+interview\s+only',
        r'\bupfront\s+(payment|fee|deposit)',
        r'\breferral\s+bonus.*\$',
        r'\bget\s+paid\s+(today|immediately|now)',
        r'\bwork\s+from\s+anywhere',
        r'\bno\s+(qualification|requirement)',
    ],
    'real': [
        r'\bcompany\s+(website|address|phone)',
        r'\bdetailed\s+job\s+description',
        r'\bspecific\s+requirement',
        r'\byears?\s+of\s+experience',
        r'\bqualification',
        r'\bdegree\s+in',
        r'\bsalary\s+range',
        r'\bbenef(it)?s',
        r'\bapply\s+(now|at|via)',
        r'\bhiring\s+team',
    ]
}

class JobPredictor:
    """Predicts if a job posting is fake or real using trained ML model."""
    
    def __init__(self, model_path=None):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
        # Try to load model
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), '..', 'models')
        
        self.model_path = model_path
        self.model = None
        self.vectorizer = None
        
        try:
            self.load_model()
            self.model_available = True
        except:
            print("Warning: Could not load trained model. Using rule-based prediction.")
            self.model_available = False
    
    def clean_text(self, text):
        """Clean and normalize text."""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def preprocess_text(self, text):
        """Preprocess text for model input."""
        # Clean text
        text = self.clean_text(text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens 
                 if word not in self.stop_words and len(word) > 2]
        
        return ' '.join(tokens)
    
    def extract_indicators(self, text):
        """Extract suspicious and positive indicators from text."""
        indicators = []
        text_lower = text.lower()
        
        # Check for fake indicators
        for pattern in FAKE_JOB_INDICATORS['fake']:
            if re.search(pattern, text_lower):
                match = re.search(pattern, text_lower)
                if match:
                    phrase = match.group(0)
                    indicators.append({
                        'type': 'fake',
                        'text': f'"{phrase}" detected'
                    })
        
        # Check for real indicators
        for pattern in FAKE_JOB_INDICATORS['real']:
            if re.search(pattern, text_lower):
                match = re.search(pattern, text_lower)
                if match:
                    phrase = match.group(0)
                    indicators.append({
                        'type': 'real',
                        'text': f'"{phrase}" detected'
                    })
        
        # Remove duplicates
        seen = set()
        unique_indicators = []
        for ind in indicators:
            key = (ind['type'], ind['text'])
            if key not in seen:
                seen.add(key)
                unique_indicators.append(ind)
        
        return unique_indicators[:5]  # Return top 5 indicators
    
    def predict(self, job_description):
        """
        Predict if a job posting is fake or real.
        
        Returns:
            tuple: (prediction, confidence, indicators)
                - prediction: 'fake' or 'real'
                - confidence: float between 0 and 1
                - indicators: list of dicts with 'type' and 'text'
        """
        if not job_description or not isinstance(job_description, str):
            return 'real', 0.5, []
        
        indicators = self.extract_indicators(job_description)
        
        if self.model_available:
            result = self._ml_predict(job_description, indicators)
        else:
            result = self._rule_based_predict(job_description, indicators)
        
        # Ensure all return values are valid
        prediction, confidence, indicators = result
        if prediction is None:
            prediction = 'real'
        if confidence is None or confidence < 0 or confidence > 1:
            confidence = 0.5
        if indicators is None:
            indicators = []
        
        return prediction, confidence, indicators
    
    def _ml_predict(self, job_description, indicators):
        """ML-based prediction."""
        try:
            # Preprocess
            processed_text = self.preprocess_text(job_description)
            
            # Vectorize
            X = self.vectorizer.transform([processed_text])
            
            # Predict
            prediction_prob = self.model.predict_proba(X)[0]
            
            # Model outputs: [probability of real, probability of fake]
            confidence_fake = prediction_prob[1]
            confidence_real = prediction_prob[0]
            
            prediction = 'fake' if confidence_fake > 0.5 else 'real'
            confidence = max(confidence_fake, confidence_real)
            
            return prediction, confidence, indicators
        except Exception as e:
            print(f"ML prediction error: {e}")
            return self._rule_based_predict(job_description, indicators)
    
    def _rule_based_predict(self, job_description, indicators):
        """Rule-based fallback prediction."""
        fake_count = sum(1 for ind in indicators if ind['type'] == 'fake')
        real_count = sum(1 for ind in indicators if ind['type'] == 'real')
        
        if fake_count > real_count:
            prediction = 'fake'
            confidence = min(0.95, 0.5 + (fake_count * 0.15))
        else:
            prediction = 'real'
            confidence = min(0.95, 0.5 + (real_count * 0.15))
        
        return prediction, confidence, indicators
    
    def load_model(self):
        """Load trained model and vectorizer from disk."""
        model_file = os.path.join(self.model_path, 'model.pkl')
        vectorizer_file = os.path.join(self.model_path, 'vectorizer.pkl')
        
        if os.path.exists(model_file) and os.path.exists(vectorizer_file):
            with open(model_file, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(vectorizer_file, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            self.model_available = True
            print("Model loaded successfully!")
        else:
            raise FileNotFoundError(f"Model files not found in {self.model_path}")
