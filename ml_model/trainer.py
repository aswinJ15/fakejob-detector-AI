import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle
import os
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

# Download NLTK data
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

class DataPreprocessor:
    """Preprocesses job posting text data."""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    
    def clean_text(self, text):
        """Clean and normalize text."""
        if isinstance(text, float):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def preprocess(self, text):
        """Full preprocessing pipeline."""
        # Clean text
        text = self.clean_text(text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens 
                 if word not in self.stop_words and len(word) > 2]
        
        return ' '.join(tokens)
    
    def preprocess_dataframe(self, df, text_columns):
        """Preprocess DataFrame text columns."""
        df_copy = df.copy()
        
        for col in text_columns:
            df_copy[col] = df_copy[col].fillna('')
            df_copy[col] = df_copy[col].apply(self.preprocess)
        
        return df_copy

class ModelTrainer:
    """Trains and evaluates the fake job detection model."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, max_df=0.8, min_df=2)
        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.preprocessor = DataPreprocessor()
        
    def prepare_data(self, df, text_columns=['title', 'description', 'requirements']):
        """Prepare data for training."""
        # Preprocess text columns
        df = self.preprocessor.preprocess_dataframe(df, text_columns)
        
        # Combine text columns
        df['combined_text'] = df[text_columns].fillna('').agg(' '.join, axis=1)
        
        return df
    
    def train(self, df, label_column='fraudulent', text_columns=None):
        """Train the model."""
        if text_columns is None:
            text_columns = ['title', 'description', 'requirements']
        
        # Prepare data
        df = self.prepare_data(df, text_columns)
        
        # Get features and labels
        X = df['combined_text']
        y = df[label_column]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Vectorize text
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        # Train model
        self.model.fit(X_train_vec, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_vec)
        y_pred_proba = self.model.predict_proba(X_test_vec)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        return metrics
    
    def save_model(self, model_path='../models/'):
        """Save trained model and vectorizer."""
        os.makedirs(model_path, exist_ok=True)
        
        with open(os.path.join(model_path, 'model.pkl'), 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(os.path.join(model_path, 'vectorizer.pkl'), 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path='../models/'):
        """Load trained model and vectorizer."""
        with open(os.path.join(model_path, 'model.pkl'), 'rb') as f:
            self.model = pickle.load(f)
        
        with open(os.path.join(model_path, 'vectorizer.pkl'), 'rb') as f:
            self.vectorizer = pickle.load(f)
        
        print(f"Model loaded from {model_path}")

if __name__ == '__main__':
    # Example usage
    print("Loading sample data...")
    # Note: Replace with actual data loading
    # df = pd.read_csv('../data/fake_job_postings.csv')
    
    print("Model training script ready.")
    print("To train: Create a dataset and use ModelTrainer class.")
