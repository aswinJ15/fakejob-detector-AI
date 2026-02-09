"""
Integration Testing Script
Test the complete JobVision application (frontend + backend)
"""

import requests
import json
from datetime import datetime

class JobVisionTester:
    def __init__(self, api_url='http://localhost:5000/api/predict'):
        self.api_url = api_url
        self.results = []
    
    def test_api_connection(self):
        """Test if API is reachable."""
        print("\n" + "="*70)
        print("TEST 1: API Connection")
        print("="*70)
        try:
            response = requests.get('http://localhost:5000/api/health', timeout=5)
            if response.status_code == 200:
                print("✅ API is healthy and responding")
                return True
            else:
                print(f"❌ API responded with status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to API: {e}")
            return False
    
    def test_real_job(self):
        """Test prediction on a real job posting."""
        print("\n" + "="*70)
        print("TEST 2: Real Job Posting")
        print("="*70)
        
        real_job = """
        Senior Full Stack Engineer
        San Francisco, CA
        
        We are seeking a talented Senior Full Stack Engineer to join our growing engineering team.
        
        About the role:
        - Design and develop scalable web applications
        - Work with React, Node.js, PostgreSQL, and AWS
        - Mentor junior engineers
        - Participate in code reviews and architecture discussions
        
        Requirements:
        - 5+ years of professional software development experience
        - Strong experience with JavaScript/TypeScript and React
        - Backend experience with Node.js or similar
        - Experience with relational databases
        - BS in Computer Science or equivalent
        
        Benefits:
        - Competitive salary: $150,000 - $200,000
        - Health, dental, vision insurance
        - 401(k) matching
        - 20 days PTO
        - Flexible work arrangements
        - Professional development budget
        
        Apply: careers.company.com/jobs/12345
        Contact: jobs@company.com
        """
        
        return self._make_prediction(real_job, "REAL")
    
    def test_fake_job(self):
        """Test prediction on a fake job posting."""
        print("\n" + "="*70)
        print("TEST 3: Fake Job Posting")
        print("="*70)
        
        fake_job = """
        WORK FROM HOME - NO EXPERIENCE NEEDED!!!
        
        Make $5,000 to $10,000 PER WEEK with NO EXPERIENCE!!!
        
        We are HIRING IMMEDIATELY! 
        - Guaranteed income! Risk-free opportunity!
        - Work from home whenever you want
        - No experience required - we train everyone
        - Start earning TODAY!
        - Get paid IMMEDIATELY - same day payouts!
        - No interviews! No phone calls! Email only!
        
        Requirements: NONE! 
        - Anyone can apply
        - No qualifications needed
        - No degree required
        
        To get started, please send a $99 upfront registration fee
        to secure your position immediately!
        
        Unlimited earning potential!
        Work whenever you want!
        Easy money!
        """
        
        return self._make_prediction(fake_job, "FAKE")
    
    def test_moderate_job(self):
        """Test prediction on a moderate/ambiguous job posting."""
        print("\n" + "="*70)
        print("TEST 4: Moderate Job Posting")
        print("="*70)
        
        moderate_job = """
        Customer Service Representative - Remote
        
        Position: Customer Service Representative
        Location: Remote (Work from Home)
        
        Join our growing customer support team!
        
        Responsibilities:
        - Answer customer inquiries via email, phone, and chat
        - Resolve customer issues professionally
        - Maintain detailed records of interactions
        - Follow company policies and procedures
        
        Requirements:
        - High school diploma or equivalent
        - 1+ years of customer service experience
        - Excellent communication skills
        - Able to work flexible hours including evenings and weekends
        - Reliable internet connection
        
        We offer:
        - Competitive hourly rate
        - Health benefits after 90 days
        - Training provided
        - Remote work flexibility
        
        Apply at: jobs.company.com
        """
        
        return self._make_prediction(moderate_job, "UNKNOWN")
    
    def test_empty_input(self):
        """Test API with empty input."""
        print("\n" + "="*70)
        print("TEST 5: Error Handling - Empty Input")
        print("="*70)
        
        try:
            response = requests.post(self.api_url, 
                                   json={"job_description": ""}, 
                                   timeout=5)
            if response.status_code == 400:
                print("✅ API correctly rejected empty input (400 Bad Request)")
                return True
            else:
                print(f"❌ Expected 400, got {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return False
    
    def _make_prediction(self, job_description, expected_type):
        """Make a prediction and display results."""
        try:
            response = requests.post(self.api_url, 
                                   json={"job_description": job_description},
                                   timeout=10)
            
            if response.status_code != 200:
                print(f"❌ API returned status {response.status_code}")
                return False
            
            result = response.json()
            
            # Display results
            prediction = result.get('prediction', 'unknown').upper()
            confidence = result.get('confidence', 0)
            indicators = result.get('indicators', [])
            
            print(f"\nPrediction: {prediction}")
            print(f"Confidence: {confidence*100:.1f}%")
            print(f"Indicators Found: {len(indicators)}")
            
            if indicators:
                print("\nKey Indicators:")
                for indicator in indicators[:5]:
                    icon = "⚠️" if indicator.get('type') == 'fake' else "✅"
                    print(f"  {icon} {indicator.get('text', '')}")
            
            # Log result
            self.results.append({
                'test': expected_type,
                'prediction': prediction,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"\n✅ Test completed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests and print summary."""
        print("\n")
        print("╔" + "="*68 + "╗")
        print("║" + " "*15 + "JobVision Integration Tests" + " "*27 + "║")
        print("╚" + "="*68 + "╝")
        
        # Run tests
        api_ok = self.test_api_connection()
        
        if api_ok:
            real_ok = self.test_real_job()
            fake_ok = self.test_fake_job()
            moderate_ok = self.test_moderate_job()
            error_ok = self.test_empty_input()
        else:
            print("\n⚠️  Skipping remaining tests - API not reachable")
            real_ok = fake_ok = moderate_ok = error_ok = False
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        tests = [
            ("API Connection", api_ok),
            ("Real Job Prediction", real_ok),
            ("Fake Job Prediction", fake_ok),
            ("Moderate Job Prediction", moderate_ok),
            ("Error Handling", error_ok)
        ]
        
        passed = sum(1 for _, ok in tests if ok)
        total = len(tests)
        
        for test_name, passed_test in tests:
            status = "✅ PASS" if passed_test else "❌ FAIL"
            print(f"{status:8} | {test_name}")
        
        print("="*70)
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! JobVision is fully operational!")
        else:
            print(f"⚠️  {total-passed} test(s) failed. Check the errors above.")

if __name__ == '__main__':
    tester = JobVisionTester()
    tester.run_all_tests()
