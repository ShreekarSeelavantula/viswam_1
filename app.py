import streamlit as st
import json
import os
from utils.auth import check_authentication, initialize_session
from utils.db import initialize_database, get_database_stats
from utils.sample_data import initialize_sample_data

# Page configuration
st.set_page_config(
    page_title="🌸 Utsav Kathalu AI",
    page_icon="🪔",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Initialize database and session
    initialize_database()
    initialize_session()
    
    # Custom CSS for Indian cultural theme
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #D4AF37;
        font-size: 3rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .subtitle {
        text-align: center;
        color: #8B4513;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-style: italic;
    }
    .feature-card {
        background: linear-gradient(135deg, #FFF8DC 0%, #F0E68C 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #FF6B35;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .welcome-box {
        background: linear-gradient(135deg, #FFE4B5 0%, #DEB887 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        border: 2px solid #D4AF37;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">🌸 Utsav Kathalu AI 🪔</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Multilingual Festival Story Collector - Preserving India\'s Cultural Heritage</p>', unsafe_allow_html=True)
    
    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        show_welcome_page()
    else:
        show_dashboard()

# Remove the public library homepage function since we don't need it

def show_welcome_page():
    """Display welcome page for non-authenticated users"""
    
    st.markdown("""
    <div class="welcome-box">
        <h2>🙏 Welcome to Utsav Kathalu AI</h2>
        <p>Share your beautiful festival stories and help preserve India's rich cultural heritage for future generations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎤 Voice & Text Stories</h3>
            <p>Upload your festival stories through voice recordings or text input in multiple Indian languages.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Enhancement</h3>
            <p>Our AI automatically cleans and enhances your stories while preserving their cultural authenticity.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📖 Virtual Books</h3>
            <p>Experience your stories as beautiful interactive virtual books with animations and images.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Call to action for non-logged users
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Ready to share your festival stories?")
        if st.button("🎭 Share Your Story", type="primary", use_container_width=True):
            st.switch_page("pages/2_Auth.py")
        
        st.markdown("### Already have an account?")
        if st.button("🔑 Login", use_container_width=True):
            st.switch_page("pages/2_Auth.py")
        
        st.markdown("---")
        st.markdown("**Note:** Login required to explore and contribute stories")

def show_dashboard():
    """Display dashboard for authenticated users"""
    user_data = st.session_state.get('user_data', {})
    
    st.markdown(f"""
    <div class="welcome-box">
        <h2>🙏 Namaste, {user_data.get('name', 'Friend')}!</h2>
        <p>Welcome back to your story collection dashboard.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Explore Stories</h3>
            <p>Choose between Virtual Books (text) or Audio Books (voice narration).</p>
        </div>
        """, unsafe_allow_html=True)
        col1a, col1b = st.columns(2)
        with col1a:
            if st.button("📖 Virtual Books", use_container_width=True):
                st.session_state.book_type_preference = 'virtual'
                st.switch_page("pages/6_PublicBooks.py")
        with col1b:
            if st.button("🎧 Audio Books", use_container_width=True):
                st.session_state.book_type_preference = 'audio'
                st.switch_page("pages/7_AudioBooks.py")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📝 Upload New Story</h3>
            <p>Share a new festival story with voice or text input.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Upload Story", use_container_width=True):
            st.switch_page("pages/3_Upload.py")
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📖 My Stories</h3>
            <p>View your personal collection as Virtual Books or Audio Books.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if user has stories before showing options
        user_email = user_data.get('email', '')
        if user_email:
            from utils.db import get_user_stories
            user_stories = get_user_stories(user_email)
            if user_stories:
                col3a, col3b = st.columns(2)
                with col3a:
                    if st.button("📚 My Virtual Books", use_container_width=True):
                        st.session_state.book_type_preference = 'virtual'
                        st.switch_page("pages/4_VirtualBook.py")
                with col3b:
                    if st.button("🎙️ My Audio Books", use_container_width=True):
                        st.session_state.book_type_preference = 'audio'
                        st.switch_page("pages/8_MyAudioBooks.py")
            else:
                st.info("📝 No stories found. Upload your first festival story to get started!")
        else:
            st.error("❌ User session error. Please login again.")
    
    # User stats
    from utils.db import get_user_stories
    user_stories = get_user_stories(user_data.get('email', ''))
    
    st.markdown("---")
    st.markdown("### 📊 Your Story Statistics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Stories", len(user_stories))
    with col2:
        languages = set([story.get('language', 'Unknown') for story in user_stories])
        st.metric("Languages Used", len(languages))
    with col3:
        festivals = set([story.get('festival', 'Unknown') for story in user_stories])
        st.metric("Festivals Covered", len(festivals))
    
    # Admin options (sample data initialization)
    st.markdown("---")
    st.markdown("### 🛠️ Platform Management")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 View Analytics"):
            st.switch_page("pages/5_Analytics.py")
    
    with col2:
        if st.button("🎭 Add Demo Stories & Users"):
            with st.spinner("Creating 4 sample users and 4 festival stories for demonstration..."):
                success, message = initialize_sample_data()
                if success:
                    st.success(f"✅ {message}")
                    st.info("💡 Demo data added! Visit Analytics to see the new users and stories, or go to Explore Stories to read them.")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    # Sample data info
    stats = get_database_stats()
    if stats['total_users'] > 0 or stats['total_stories'] > 0:
        st.info(f"💡 Platform has {stats['total_users']} users and {stats['total_stories']} stories. Visit Analytics to see detailed insights.")
    
    # Logout option
    st.markdown("---")
    if st.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()
