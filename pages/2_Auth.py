import streamlit as st
from utils.auth import register_user, login_user, INDIAN_STATES, INDIAN_LANGUAGES

# Page configuration
st.set_page_config(
    page_title="Authentication - Utsav Kathalu AI",
    page_icon="🔐",
    layout="wide"
)

def main():
    st.markdown("""
    <style>
    .auth-header {
        text-align: center;
        color: #D4AF37;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .auth-container {
        background: linear-gradient(135deg, #FFF8DC 0%, #F0E68C 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 2px solid #D4AF37;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .form-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #FF6B35;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="auth-header">🔐 Welcome to Utsav Kathalu AI</h1>', unsafe_allow_html=True)
    
    # Check if user is already logged in
    if st.session_state.get('logged_in', False):
        st.success("🎉 You are already logged in!")
        if st.button("🏠 Go to Dashboard"):
            st.switch_page("app.py")
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        return
    
    # Authentication tabs
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_signup_form()

def show_login_form():
    """Display login form"""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown("### 🔑 Login to Your Account")
    
    with st.form("login_form"):
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        
        email = st.text_input(
            "📧 Email Address",
            placeholder="Enter your email address",
            help="Use the email you registered with"
        )
        
        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Enter your password",
            help="Enter your account password"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("🚀 Login", type="primary", use_container_width=True)
        
        if submit_button:
            if not email or not password:
                st.error("❌ Please fill in all fields")
            else:
                with st.spinner("Logging you in..."):
                    success, message = login_user(email, password)
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_signup_form():
    """Display signup form"""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown("### 📝 Create Your Account")
    st.markdown("Join our community of storytellers and help preserve India's cultural heritage!")
    
    with st.form("signup_form"):
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("**👤 Personal Information**")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(
                "📝 Full Name *",
                placeholder="Enter your full name",
                help="Your name will be associated with your stories"
            )
        
        with col2:
            email = st.text_input(
                "📧 Email Address *",
                placeholder="Enter your email address",
                help="This will be your login username"
            )
        
        password = st.text_input(
            "🔒 Password *",
            type="password",
            placeholder="Create a secure password (min 6 characters)",
            help="Choose a strong password with at least 6 characters"
        )
        
        confirm_password = st.text_input(
            "🔒 Confirm Password *",
            type="password",
            placeholder="Re-enter your password",
            help="Must match the password above"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("**🌍 Cultural Information**")
        
        col1, col2 = st.columns(2)
        with col1:
            preferred_language = st.selectbox(
                "🗣️ Preferred Language *",
                options=INDIAN_LANGUAGES,
                index=0,
                help="Primary language for your stories"
            )
        
        with col2:
            state = st.selectbox(
                "📍 State/UT *",
                options=INDIAN_STATES,
                index=0,
                help="Your state or union territory in India"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Terms and conditions
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        terms_agreed = st.checkbox(
            "✅ I agree to the Terms of Service and Privacy Policy",
            help="By checking this, you agree to our terms and conditions"
        )
        
        newsletter = st.checkbox(
            "📧 Subscribe to updates about new features and cultural events",
            value=True,
            help="Get notified about platform updates and cultural celebrations"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("🎉 Create Account", type="primary", use_container_width=True)
        
        if submit_button:
            # Validation
            if not all([name, email, password, confirm_password, preferred_language, state]):
                st.error("❌ Please fill in all required fields marked with *")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif not terms_agreed:
                st.error("❌ Please agree to the Terms of Service and Privacy Policy")
            else:
                with st.spinner("Creating your account..."):
                    success, message = register_user(name, email, password, preferred_language, state)
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.success("🎉 Welcome to Utsav Kathalu AI! Logging you in automatically...")
                        # Auto-login after successful registration
                        login_success, login_message = login_user(email, password)
                        if login_success:
                            st.balloons()
                            st.rerun()
                        else:
                            st.info("👆 Please switch to the Login tab to access your account.")
                    else:
                        st.error(f"❌ {message}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_back_button():
    """Show back to home button"""
    if st.button("🏠 Back to Home"):
        st.switch_page("app.py")

if __name__ == "__main__":
    main()
