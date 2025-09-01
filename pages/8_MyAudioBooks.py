import streamlit as st
from utils.auth import check_authentication, get_current_user
from utils.db import get_user_stories, load_story
import base64

# Page configuration
st.set_page_config(
    page_title="My Audio Books - Utsav Kathalu AI",
    page_icon="🎙️",
    layout="wide"
)

def main():
    """My personal audio books page"""
    if not check_authentication():
        st.warning("🔒 Please login to access your audio books.")
        if st.button("🔑 Go to Login"):
            st.switch_page("pages/2_Auth.py")
        return
    
    # Custom CSS (same as public audio books)
    st.markdown("""
    <style>
    .my-audio-header {
        text-align: center;
        background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .audio-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .audio-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
    }
    .my-audio-story-card {
        background: linear-gradient(135deg, #E6F3FF 0%, #CCE7FF 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #6B73FF;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    .my-audio-story-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="my-audio-header">
        <div class="audio-title">🎙️ My Audio Books</div>
        <div class="audio-subtitle">Your Personal Collection of Voice-Narrated Stories</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get user's audio stories
    user_data = get_current_user()
    user_email = user_data.get('email', '')
    
    user_stories = get_user_stories(user_email)
    audio_stories = [story for story in user_stories if story.get('input_method') == 'voice']
    
    if not audio_stories:
        st.markdown("""
        <div class="my-audio-story-card">
            <h3>🎙️ No Audio Books Yet</h3>
            <p>You haven't created any voice-narrated stories yet. Upload a story using voice input to see your audio books here!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎤 Create Audio Story", type="primary", use_container_width=True):
                st.switch_page("pages/3_Upload.py")
        with col2:
            if st.button("📖 View Virtual Books", use_container_width=True):
                st.switch_page("pages/4_VirtualBook.py")
        return
    
    st.markdown(f"**🎧 Your Audio Book Collection: {len(audio_stories)} voice-narrated stories**")
    
    # Display audio stories
    for story in audio_stories:
        display_my_audio_story_card(story)

def display_my_audio_story_card(story):
    """Display user's audio story card"""
    col1, col2 = st.columns([3, 1])
    
    created_date = story.get('created_at', '').split('T')[0] if story.get('created_at') else 'Unknown'
    
    with col1:
        st.markdown(f"""
        <div class="my-audio-story-card">
            <h3>🎧 {story.get('title', 'Untitled Audio Story')}</h3>
            <p><strong>🎊 Festival:</strong> {story.get('festival', 'Unknown')}</p>
            <p><strong>🗣️ Language:</strong> {story.get('language', 'Unknown')}</p>
            <p><strong>📚 Type:</strong> {story.get('story_type', 'Unknown')}</p>
            <p><strong>🎙️ Audio Sections:</strong> {len(story.get('sections', []))}</p>
            <p><strong>📅 Created:</strong> {created_date}</p>
            <p><small>{story.get('description', 'No description available')[:150]}{'...' if len(story.get('description', '')) > 150 else ''}</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button(f"🎧 Listen", key=f"my_listen_{story.get('story_id')}", type="primary"):
            # Use the same audio reader as public books
            st.session_state.selected_audio_story_id = story.get('story_id')
            st.switch_page("pages/7_AudioBooks.py")

if __name__ == "__main__":
    main()