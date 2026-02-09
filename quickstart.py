#!/usr/bin/env python3
"""
JobVision Quick Start Script
Run this to start the entire application automatically
"""

import subprocess
import time
import sys
import os

def run_command(cmd, description):
    """Run a command and report status."""
    print(f"\n{'='*70}")
    print(f"🚀 {description}")
    print(f"{'='*70}")
    print(f"Command: {cmd}\n")
    
    try:
        process = subprocess.Popen(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(timeout=5)
        
        if process.returncode == 0:
            print(f"✅ {description} completed successfully")
            if stdout:
                print(stdout)
            return True
        else:
            print(f"❌ {description} failed")
            if stderr:
                print(f"Error: {stderr}")
            return False
    except subprocess.TimeoutExpired:
        process.kill()
        print(f"⏳ {description} started (running in background)")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Start the application."""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*15 + "JobVision - Fake Job Detector" + " "*24 + "║")
    print("║" + " "*70 + "║")
    print("║" + " Quick Start - Starting all services..." + " "*28 + "║")
    print("╚" + "="*68 + "╝\n")
    
    # Check Python version
    print("📋 System Check")
    print("-" * 70)
    print(f"Python: {sys.version.split()[0]}")
    print(f"OS: {sys.platform}")
    print(f"Current Directory: {os.getcwd()}")
    
    # Verify files exist
    required_files = [
        'backend/app.py',
        'ml_model/predictor.py',
        'models/model.pkl',
        'models/vectorizer.pkl',
        'frontend/index.html',
        'data/fake_job_postings.csv'
    ]
    
    print("\n📂 Checking required files...")
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} NOT FOUND")
            all_exist = False
    
    if not all_exist:
        print("\n❌ Some required files are missing!")
        print("Please ensure you've run the setup steps.")
        return
    
    print("\n" + "="*70)
    print("✅ All checks passed! Ready to start services...")
    print("="*70)
    
    print("\n📌 IMPORTANT: This script will start background processes.")
    print("You'll need to keep this terminal open.")
    print("\nPress Enter to continue...")
    input()
    
    # Start backend
    print("\n" + "="*70)
    print("Starting Backend API Server...")
    print("="*70)
    print("This will run on: http://localhost:5000")
    
    try:
        subprocess.Popen([
            'python', 
            'backend/app.py'
        ], cwd=os.getcwd())
        time.sleep(3)
        print("✅ Backend started!")
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return
    
    # Start frontend
    print("\n" + "="*70)
    print("Starting Frontend HTTP Server...")
    print("="*70)
    print("This will run on: http://localhost:8000")
    
    try:
        subprocess.Popen([
            'python',
            'serve_frontend.py'
        ], cwd=os.getcwd())
        time.sleep(2)
        print("✅ Frontend started!")
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return
    
    # Success message
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*70 + "║")
    print("║" + " ✅ JobVision is now running!" + " "*38 + "║")
    print("║" + " "*70 + "║")
    print("║" + " 🌐 Frontend:  http://localhost:8000" + " "*30 + "║")
    print("║" + " 🔧 Backend:   http://localhost:5000" + " "*30 + "║")
    print("║" + " "*70 + "║")
    print("║" + " Open the frontend URL in your browser to start analyzing jobs!" + " "*5 + "║")
    print("║" + " "*70 + "║")
    print("║" + " Press Ctrl+C to stop all services" + " "*32 + "║")
    print("║" + " "*70 + "║")
    print("╚" + "="*68 + "╝\n")
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("🛑 Shutting down...")
        print("="*70)
        print("All services stopped.")
        print("="*70 + "\n")

if __name__ == '__main__':
    main()
