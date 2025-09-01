import streamlit as st
import json
import hashlib
import os
from datetime import datetime
from .db import load_users, save_users

def initialize_session():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Basic email validation"""
    return '@' in email and '.' in email.split('@')[1]

def validate_password(password):
    """Password validation - minimum 6 characters"""
    return len(password) >= 6

def register_user(name, email, password, preferred_language, state):
    """Register a new user"""
    users = load_users()
    
    # Check if user already exists
    if email in users:
        return False, "User with this email already exists"
    
    # Validate inputs
    if not validate_email(email):
        return False, "Please enter a valid email address"
    
    if not validate_password(password):
        return False, "Password must be at least 6 characters long"
    
    if not name.strip():
        return False, "Name cannot be empty"
    
    # Create new user
    users[email] = {
        'name': name.strip(),
        'email': email,
        'password': hash_password(password),
        'preferred_language': preferred_language,
        'state': state,
        'created_at': datetime.now().isoformat(),
        'stories': []
    }
    
    # Save users
    if save_users(users):
        return True, "User registered successfully"
    else:
        return False, "Failed to save user data"

def login_user(email, password):
    """Login user with email and password"""
    users = load_users()
    
    if email not in users:
        return False, "User not found"
    
    user = users[email]
    if user['password'] != hash_password(password):
        return False, "Incorrect password"
    
    # Set session state
    st.session_state.logged_in = True
    st.session_state.user_data = {
        'name': user['name'],
        'email': user['email'],
        'preferred_language': user['preferred_language'],
        'state': user['state']
    }
    
    return True, "Login successful"

def logout_user():
    """Logout current user"""
    st.session_state.logged_in = False
    st.session_state.user_data = {}

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get('logged_in', False)

def get_current_user():
    """Get current user data"""
    return st.session_state.get('user_data', {})

# Indian states and languages
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", 
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", 
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", 
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Puducherry", "Chandigarh",
    "Andaman and Nicobar Islands", "Dadra and Nagar Haveli and Daman and Diu",
    "Lakshadweep"
]

INDIAN_LANGUAGES = [
    "Hindi", "English", "Bengali", "Telugu", "Marathi", "Tamil", "Gujarati", 
    "Urdu", "Kannada", "Odia", "Malayalam", "Punjabi", "Assamese", "Maithili", 
    "Sanskrit", "Nepali", "Konkani", "Sindhi", "Dogri", "Manipuri", "Bodo", 
    "Santhali", "Kashmiri"
]
