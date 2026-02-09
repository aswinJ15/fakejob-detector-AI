"""
Sample script to generate synthetic training data for the fake job detector.
This creates a CSV file with fake and real job postings.
"""

import pandas as pd
import random

# Sample real job postings
real_jobs = [
    {
        'title': 'Senior Python Developer',
        'description': 'We are looking for an experienced Python developer with 5+ years of experience in backend development. You will work with our engineering team to build scalable applications.',
        'requirements': 'BS in Computer Science or related field, 5+ years Python experience, experience with Django or FastAPI',
        'fraudulent': 0
    },
    {
        'title': 'Data Scientist',
        'description': 'Join our data team! We need a skilled data scientist to analyze business metrics and build predictive models. Our company has over 50 years of history.',
        'requirements': 'Masters in Statistics/CS, 3+ years ML experience, proficiency in Python and SQL',
        'fraudulent': 0
    },
    {
        'title': 'UX/UI Designer',
        'description': 'Our design team is expanding. We seek creative designers with strong portfolio. Location: San Francisco, CA. Competitive salary and benefits.',
        'requirements': 'Portfolio required, 3+ years design experience, proficiency in Figma and Adobe Creative Suite',
        'fraudulent': 0
    },
    {
        'title': 'Full Stack Engineer',
        'description': 'Help us build the next generation of web applications. We offer competitive salary, health insurance, 401k, and flexible work arrangements.',
        'requirements': '5+ years experience, strong JavaScript/React background, Node.js and SQL experience',
        'fraudulent': 0
    },
    {
        'title': 'Product Manager',
        'description': 'Lead product strategy at our growing SaaS company. Our team has shipped 3 major products to 100k+ users.',
        'requirements': '5+ years PM experience, proven track record with successful launches, strong analytical skills',
        'fraudulent': 0
    }
]

# Sample fake job postings
fake_jobs = [
    {
        'title': 'WORK FROM HOME - NO EXPERIENCE NEEDED',
        'description': 'Make $5000 per week with no experience needed! We hire immediately. All you need is a phone and email. No interview required.',
        'requirements': 'No experience required. No education needed. Start immediately.',
        'fraudulent': 1
    },
    {
        'title': 'Easy Money - $10k/month',
        'description': 'Get paid $10,000 per month working from home! No skills needed. Guaranteed income. Work whenever you want.',
        'requirements': 'No requirements at all. Anyone can apply. Immediate hiring.',
        'fraudulent': 1
    },
    {
        'title': 'INSTANT HIRING - Work from home',
        'description': 'Risk-free job opportunity! Start working today and get paid tomorrow. We are hiring everyone. Phone interview only, no office visit needed.',
        'requirements': 'No qualifications needed. We accept everyone.',
        'fraudulent': 1
    },
    {
        'title': 'MAKE $50K IN 30 DAYS',
        'description': 'Earn easy money with our simple online job. Work from anywhere. Get immediate cash payments. Guaranteed $50,000 in one month.',
        'requirements': 'None. No experience. No degree required.',
        'fraudulent': 1
    },
    {
        'title': 'High Paying Work From Home',
        'description': 'Start earning $100/hour from your home! No skills needed. Immediate start. Must send $50 deposit to secure position.',
        'requirements': 'Send upfront payment of $50 to get started',
        'fraudulent': 1
    },
    {
        'title': 'Join Our Affiliate Program - EASY MONEY',
        'description': 'Make unlimited money! Get $100 for each person you refer. Work from home with no responsibilities. Immediate payment guaranteed.',
        'requirements': 'Just recruit people and earn passive income',
        'fraudulent': 1
    }
]

# Create dataset
data = real_jobs * 5 + fake_jobs * 5  # Multiply to get more samples
random.shuffle(data)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('data/fake_job_postings.csv', index=False)
print(f"Dataset created with {len(df)} samples")
print(f"Fraud rate: {df['fraudulent'].sum() / len(df) * 100:.1f}%")
