import streamlit as st
from utils.auth import check_authentication, get_current_user
from utils.db import get_database_stats, get_all_stories, load_users
import json
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Analytics - Utsav Kathalu AI",
    page_icon="📊",
    layout="wide"
)

def main():
    # Check authentication
    if not check_authentication():
        st.warning("🔒 Please login to access analytics.")
        if st.button("🔑 Go to Login"):
            st.switch_page("pages/2_Auth.py")
        return
    
    # Custom CSS
    st.markdown("""
    <style>
    .analytics-header {
        text-align: center;
        color: #D4AF37;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #FFF8DC 0%, #F0E68C 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #FF6B35;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .user-card {
        background: linear-gradient(135deg, #E6F3FF 0%, #CCE7FF 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #4A90E2;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="analytics-header">📊 Platform Analytics</h1>', unsafe_allow_html=True)
    
    # Get database statistics
    stats = get_database_stats()
    users_data = load_users()
    all_stories = get_all_stories()
    
    # Overview metrics
    st.markdown("## 📈 Platform Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color: #FF6B35; margin: 0;">{stats['total_users']}</h2>
            <p style="margin: 0; font-size: 1.1rem;">Total Users</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color: #FF6B35; margin: 0;">{stats['total_stories']}</h2>
            <p style="margin: 0; font-size: 1.1rem;">Total Stories</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color: #FF6B35; margin: 0;">{len(stats['languages'])}</h2>
            <p style="margin: 0; font-size: 1.1rem;">Languages</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color: #FF6B35; margin: 0;">{len(stats['festivals'])}</h2>
            <p style="margin: 0; font-size: 1.1rem;">Festivals</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Detailed analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🗣️ Language Distribution")
        if stats['languages']:
            lang_data = pd.DataFrame(list(stats['languages'].items()))
            lang_data.columns = ['Language', 'Stories']
            st.bar_chart(lang_data.set_index('Language'))
        else:
            st.info("No language data available yet.")
    
    with col2:
        st.markdown("### 🎊 Festival Distribution")
        if stats['festivals']:
            fest_data = pd.DataFrame(list(stats['festivals'].items()))
            fest_data.columns = ['Festival', 'Stories']
            st.bar_chart(fest_data.set_index('Festival'))
        else:
            st.info("No festival data available yet.")
    
    st.markdown("---")
    
    # User details
    st.markdown("## 👥 User Details")
    
    if users_data:
        for email, user_info in users_data.items():
            user_stories = [story for story in all_stories if story.get('user_email') == email]
            
            st.markdown(f"""
            <div class="user-card">
                <h4>👤 {user_info.get('name', 'Unknown')}</h4>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Language:</strong> {user_info.get('preferred_language', 'Unknown')}</p>
                <p><strong>State:</strong> {user_info.get('state', 'Unknown')}</p>
                <p><strong>Stories:</strong> {len(user_stories)}</p>
                <p><strong>Joined:</strong> {user_info.get('created_at', 'Unknown')[:10] if user_info.get('created_at') else 'Unknown'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if user_stories:
                with st.expander(f"📚 Stories by {user_info.get('name', 'Unknown')} ({len(user_stories)})"):
                    for story in user_stories:
                        st.write(f"**{story.get('title', 'Untitled')}** - {story.get('festival', 'Unknown')} ({story.get('language', 'Unknown')})")
                        st.write(f"   Created: {story.get('created_at', 'Unknown')[:10] if story.get('created_at') else 'Unknown'}")
                        st.write(f"   Sections: {len(story.get('sections', []))}")
                        st.write("---")
    else:
        st.info("No users have registered yet.")
    
    st.markdown("---")
    
    # Recent activity
    st.markdown("## 🕒 Recent Activity")
    
    if all_stories:
        # Sort stories by creation date
        sorted_stories = sorted(all_stories, key=lambda x: x.get('created_at', ''), reverse=True)
        recent_stories = sorted_stories[:10]  # Show last 10 stories
        
        for story in recent_stories:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{story.get('title', 'Untitled')}** by {story.get('user_name', 'Unknown')}")
            
            with col2:
                st.write(f"{story.get('festival', 'Unknown')} ({story.get('language', 'Unknown')})")
            
            with col3:
                st.write(f"{story.get('created_at', 'Unknown')[:10] if story.get('created_at') else 'Unknown'}")
    else:
        st.info("No stories have been uploaded yet.")

if __name__ == "__main__":
    main()