"""
Training script to train the fake job detection model.
Run this after generating or preparing your dataset.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
from ml_model.trainer import ModelTrainer

def main():
    # Load data
    print("Loading dataset...")
    try:
        df = pd.read_csv('data/fake_job_postings.csv')
    except FileNotFoundError:
        print("Dataset not found. Please run: python data/generate_sample_data.py")
        return
    
    print(f"Dataset loaded: {len(df)} samples")
    print(f"Fraud rate: {df['fraudulent'].sum() / len(df) * 100:.1f}%")
    
    # Initialize trainer
    trainer = ModelTrainer()
    
    # Train model
    print("\nTraining model...")
    metrics = trainer.train(
        df, 
        label_column='fraudulent',
        text_columns=['title', 'description', 'requirements']
    )
    
    # Print metrics
    print("\n" + "="*50)
    print("MODEL PERFORMANCE")
    print("="*50)
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1-Score:  {metrics['f1']:.4f}")
    print("\nConfusion Matrix:")
    print(f"True Negatives:  {metrics['confusion_matrix'][0][0]}")
    print(f"False Positives: {metrics['confusion_matrix'][0][1]}")
    print(f"False Negatives: {metrics['confusion_matrix'][1][0]}")
    print(f"True Positives:  {metrics['confusion_matrix'][1][1]}")
    print("="*50)
    
    # Save model
    print("\nSaving model...")
    trainer.save_model('models/')
    print("Model saved successfully!")
    print("\nYou can now run the Flask app: python backend/app.py")

if __name__ == '__main__':
    main()
