// DOM Elements
const jobInput = document.getElementById('job-description');
const predictBtn = document.getElementById('predict-btn');
const spinner = document.getElementById('spinner');
const landingSection = document.querySelector('.landing-section');
const resultsSection = document.getElementById('results');
const backBtn = document.getElementById('back-btn');

// Results Elements
const predictionLabel = document.getElementById('prediction-label');
const statusBadge = document.getElementById('status-badge');
const confidencePercentage = document.getElementById('confidence-percentage');
const confidenceFill = document.getElementById('confidence-fill');
const predictionMessage = document.getElementById('prediction-message');
const indicatorsList = document.getElementById('indicators-list');

// API Configuration
const API_URL = 'http://localhost:5000/api/predict';

// App State
let isLoading = false;

// Event Listeners
predictBtn.addEventListener('click', handlePredict);
backBtn.addEventListener('click', handleBack);

// Check API health on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAPIHealth();
    updateNavBar();
});

async function checkAPIHealth() {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);
        
        const response = await fetch('http://localhost:5000/api/health', {
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        
        if (response.ok) {
            console.log('✅ API is healthy');
            const data = await response.json();
            console.log('API Status:', data);
        } else {
            console.warn('⚠️ API responded with status:', response.status);
            showNotification('API is running but may have issues (Status: ' + response.status + ')', 'warning');
        }
    } catch (error) {
        console.warn('⚠️ Cannot connect to API:', error.message);
        if (error.name === 'AbortError') {
            showNotification('⚠️ Backend not responding. Start the backend with: python backend/app.py', 'warning');
        } else {
            showNotification('⚠️ Cannot connect to backend API at http://localhost:5000', 'warning');
        }
    }
}

async function handlePredict() {
    if (isLoading) return;

    const jobDescription = jobInput.value.trim();

    if (!jobDescription) {
        showNotification('Please paste a job description to analyze.', 'error');
        jobInput.focus();
        return;
    }

    if (jobDescription.length < 50) {
        showNotification('Please provide a more detailed job description (at least 50 characters).', 'warning');
        return;
    }

    // Show spinner
    isLoading = true;
    spinner.classList.remove('hidden');
    predictBtn.disabled = true;
    predictBtn.innerHTML = '⏳ Analyzing...';

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);
        
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ job_description: jobDescription }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);

        if (!response.ok) {
            if (response.status === 400) {
                throw new Error('Invalid job description');
            } else if (response.status === 500) {
                throw new Error('Server error. Please try again.');
            } else {
                throw new Error(`HTTP Error: ${response.status}`);
            }
        }

        const data = await response.json();
        
        // Validate response
        if (!data.prediction || data.confidence === undefined) {
            throw new Error('Invalid response from server');
        }
        
        displayResults(data);
        scrollToResults();

    } catch (error) {
        console.error('Error:', error);
        
        let errorMessage = 'An error occurred during prediction.';
        if (error.name === 'AbortError') {
            errorMessage = 'Request timeout. Backend might be slow. Make sure the backend API is running on http://localhost:5000';
        } else if (error.message.includes('Failed to fetch')) {
            errorMessage = 'Cannot connect to API. Make sure the backend is running on http://localhost:5000';
        } else if (error.message.includes('NetworkError')) {
            errorMessage = 'Network error. Check backend connection at http://localhost:5000';
        } else if (error.message) {
            errorMessage = error.message;
        }
        
        showNotification(errorMessage, 'error');
    } finally {
        isLoading = false;
        spinner.classList.add('hidden');
        predictBtn.disabled = false;
        predictBtn.innerHTML = '🔍 Predict Job Reality';
    }
}

function displayResults(data) {
    const isPredictionReal = data.prediction === 'real';
    const confidence = Math.round(data.confidence * 100);

    // Update prediction label and badge
    predictionLabel.textContent = isPredictionReal ? '✓ REAL JOB' : '✗ FAKE JOB';
    statusBadge.className = `status-badge ${isPredictionReal ? 'real' : 'fake'}`;

    // Update confidence
    confidencePercentage.textContent = confidence + '%';
    const circumference = 2 * Math.PI * 50; // radius = 50
    const offset = circumference - (confidence / 100) * circumference;
    confidenceFill.style.strokeDashoffset = offset;
    confidenceFill.style.stroke = isPredictionReal ? '#10b981' : '#ef4444';

    // Update message
    const predictionText = isPredictionReal ? 
        'This job posting appears to be REAL. It matches characteristics of legitimate job listings.' :
        'This job posting appears to be FAKE. Please be cautious and verify before applying.';
    
    const confidenceLevel = confidence > 85 ? 'very high' : 
                           confidence > 70 ? 'high' : 
                           confidence > 50 ? 'moderate' : 'low';
    
    predictionMessage.textContent = `${predictionText} (${confidenceLevel} confidence)`;

    // Update indicators
    displayIndicators(data.indicators);

    // Show results section
    landingSection.style.display = 'none';
    resultsSection.classList.remove('hidden');
    
    // Animate confidence ring
    animateConfidenceRing(confidence);
}

function animateConfidenceRing(percentage) {
    const circumference = 2 * Math.PI * 50;
    const offset = circumference - (percentage / 100) * circumference;
    
    confidenceFill.style.transition = 'none';
    confidenceFill.style.strokeDashoffset = circumference;
    
    setTimeout(() => {
        confidenceFill.style.transition = 'stroke-dashoffset 0.8s ease-out';
        confidenceFill.style.strokeDashoffset = offset;
    }, 100);
}

function displayIndicators(indicators) {
    indicatorsList.innerHTML = '';

    if (indicators && indicators.length > 0) {
        indicators.forEach(indicator => {
            const div = document.createElement('div');
            div.className = `indicator ${indicator.type}`;
            div.innerHTML = `
                <span class="icon">${indicator.type === 'fake' ? '⚠️' : '✅'}</span>
                <span class="text">${indicator.text}</span>
            `;
            indicatorsList.appendChild(div);
        });
    } else {
        indicatorsList.innerHTML = '<p style="color: #64748b; padding: 1rem;">No specific indicators found.</p>';
    }
}

function handleBack() {
    landingSection.style.display = 'flex';
    resultsSection.classList.add('hidden');
    jobInput.value = '';
    jobInput.focus();
}

function scrollToResults() {
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 300);
}

function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    const icons = {
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'success': '✅'
    };
    notification.innerHTML = `
        <div class="notification-content">
            <span>${icons[type] || 'ℹ️'} ${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    document.body.insertBefore(notification, document.body.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Allow prediction with Ctrl+Enter
jobInput.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter' && !isLoading) {
        handlePredict();
    }
});

// Handle Sign In form submission
const signinForm = document.getElementById('signin-form');
if (signinForm) {
    signinForm.addEventListener('submit', (e) => {
        e.preventDefault();
        handleSignIn();
    });
}

let isSignUpMode = false;

function toggleAuthMode() {
    isSignUpMode = !isSignUpMode;
    const formTitle = document.getElementById('form-title');
    const toggleText = document.getElementById('toggle-text');
    const toggleLink = document.getElementById('toggle-link');
    const nameGroup = document.getElementById('name-group');
    const submitBtn = document.getElementById('form-submit-btn');
    const fullnameInput = document.getElementById('fullname');

    if (isSignUpMode) {
        formTitle.textContent = 'Create Account';
        toggleText.textContent = 'Already have an account?';
        toggleLink.textContent = 'Sign in';
        nameGroup.style.display = 'flex';
        submitBtn.textContent = 'Create Account';
        fullnameInput.required = true;
    } else {
        formTitle.textContent = 'Sign In';
        toggleText.textContent = 'Don\'t have an account?';
        toggleLink.textContent = 'Create one';
        nameGroup.style.display = 'none';
        submitBtn.textContent = 'Sign In';
        fullnameInput.required = false;
    }
}

function handleSignIn() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const fullname = document.getElementById('fullname').value.trim();

    if (!email || !password) {
        showNotification('Please fill in all fields', 'error');
        return;
    }

    if (isSignUpMode) {
        if (!fullname) {
            showNotification('Please enter your full name', 'error');
            return;
        }
        // Create account (local storage)
        const users = JSON.parse(localStorage.getItem('jobvision_users') || '{}');
        if (users[email]) {
            showNotification('Email already registered!', 'error');
            return;
        }
        
        users[email] = {
            fullname: fullname,
            password: password,
            createdAt: new Date().toISOString()
        };
        localStorage.setItem('jobvision_users', JSON.stringify(users));
        showNotification(`✅ Account created successfully! Welcome ${fullname}`, 'success');
        
        // Auto login
        loginUser(email, fullname);
    } else {
        // Sign in
        const users = JSON.parse(localStorage.getItem('jobvision_users') || '{}');
        const user = users[email];

        if (!user || user.password !== password) {
            showNotification('❌ Invalid email or password', 'error');
            return;
        }

        loginUser(email, user.fullname);
    }
}

function loginUser(email, fullname) {
    // Save session
    localStorage.setItem('jobvision_current_user', JSON.stringify({
        email: email,
        fullname: fullname,
        loginTime: new Date().toISOString()
    }));

    showNotification(`👋 Welcome back, ${fullname}!`, 'success');
    updateNavBar();
    
    // Redirect to home
    setTimeout(() => {
        document.querySelector('a[href="#home"]').click();
        isSignUpMode = false;
        signinForm.reset();
    }, 1500);
}

function logoutUser() {
    localStorage.removeItem('jobvision_current_user');
    showNotification('👋 You have been logged out', 'info');
    updateNavBar();
    document.querySelector('a[href="#home"]').click();
}

function updateNavBar() {
    const navSignin = document.getElementById('nav-signin');
    const navProfile = document.getElementById('nav-profile');
    const userName = document.getElementById('user-name');
    const logoutBtn = document.getElementById('logout-btn');
    const currentUser = JSON.parse(localStorage.getItem('jobvision_current_user') || 'null');

    if (currentUser) {
        navSignin.style.display = 'none';
        navProfile.style.display = 'flex';
        userName.textContent = `👤 ${currentUser.fullname}`;
        logoutBtn.onclick = logoutUser;
    } else {
        navSignin.style.display = 'block';
        navProfile.style.display = 'none';
    }
}


// Add keyboard shortcut hint on input focus
jobInput.addEventListener('focus', () => {
    if (!jobInput.value) {
        const hint = document.querySelector('.shortcut-hint');
        if (!hint) {
            const div = document.createElement('div');
            div.className = 'shortcut-hint';
            div.textContent = 'Tip: Press Ctrl+Enter to predict quickly';
            jobInput.parentElement.appendChild(div);
        }
    }
});

jobInput.addEventListener('blur', () => {
    const hint = document.querySelector('.shortcut-hint');
    if (hint) hint.remove();
});
