"""
Quick test script to verify the model and API.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from ml_model.predictor import JobPredictor

def test_predictions():
    """Test the predictor with sample job descriptions."""
    
    print("Initializing predictor...")
    predictor = JobPredictor()
    
    # Test cases
    test_jobs = [
        {
            'name': 'Real Job Posting',
            'text': '''
            Senior Software Engineer
            Location: San Francisco, CA
            
            We are seeking an experienced software engineer with 5+ years of experience
            in full-stack development. You will work with our talented engineering team
            to build and maintain our platform serving millions of users.
            
            Requirements:
            - Bachelor's degree in Computer Science or related field
            - 5+ years of professional software development experience
            - Strong knowledge of Python, JavaScript, and SQL
            - Experience with cloud platforms (AWS, GCP, or Azure)
            - Bachelor's degree in Computer Science or related field
            
            Benefits:
            - Competitive salary: $150k - $200k
            - Health insurance, 401k matching
            - 20 days PTO
            - Remote work options
            
            Apply at: careers.company.com
            '''
        },
        {
            'name': 'Suspicious Job Posting',
            'text': '''
            WORK FROM HOME - NO EXPERIENCE NEEDED!!!
            
            Make $5,000 per WEEK with NO experience needed!
            We hire IMMEDIATELY with guaranteed income!
            
            No interview required - no experience required
            Work from anywhere - work whenever you want
            Get paid TODAY - immediate cash payments
            
            Requirements: NONE! 
            Anyone can apply! We accept everyone!
            
            This is risk-free and guaranteed money.
            If interested, send $99 upfront fee to secure your position.
            
            Start making easy money TODAY!
            '''
        },
        {
            'name': 'Moderate Job',
            'text': '''
            Customer Service Representative
            
            We are looking for friendly and professional customer service representatives.
            Work from home opportunity available.
            
            Responsibilities:
            - Answer customer inquiries via phone, email, and chat
            - Resolve customer complaints professionally
            - Maintain detailed records
            
            Requirements:
            - High school diploma or equivalent
            - 1+ years customer service experience
            - Excellent communication skills
            - Able to work flexible hours
            
            Salary: Competitive based on experience
            Apply today through our website.
            '''
        }
    ]
    
    print("\n" + "="*60)
    for test in test_jobs:
        print(f"\nTesting: {test['name']}")
        print("-"*60)
        
        prediction, confidence, indicators = predictor.predict(test['text'])
        
        print(f"Prediction: {prediction.upper()}")
        print(f"Confidence: {confidence*100:.1f}%")
        print("\nIndicators:")
        for ind in indicators:
            emoji = "⚠️" if ind['type'] == 'fake' else "✅"
            print(f"  {emoji} {ind['text']}")
        print("-"*60)
    
    print("\n" + "="*60)
    print("Test completed!")

if __name__ == '__main__':
    test_predictions()
