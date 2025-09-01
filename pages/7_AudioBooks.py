import streamlit as st
from utils.auth import check_authentication, get_current_user
from utils.db import get_all_stories, load_story
import base64
import json

# Page configuration
st.set_page_config(
    page_title="Audio Books - Utsav Kathalu AI",
    page_icon="🎧",
    layout="wide"
)

def main():
    """Main page for exploring all public audio books"""
    if not check_authentication():
        st.warning("🔒 Please login to explore audio books.")
        if st.button("🔑 Go to Login"):
            st.switch_page("pages/2_Auth.py")
        return
    
    # Custom CSS for audio books
    st.markdown("""
    <style>
    .audio-header {
        text-align: center;
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
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
    .audio-story-card {
        background: linear-gradient(135deg, #E6F3FF 0%, #CCE7FF 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #4ECDC4;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    .audio-story-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .audio-book-page {
        background: linear-gradient(135deg, #F0F8FF 0%, #E6F3FF 100%);
        padding: 3rem;
        border-radius: 15px;
        min-height: 800px;
        position: relative;
        border: 2px solid #4ECDC4;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .narrator-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 2rem 0;
        padding: 2rem;
        background: linear-gradient(135deg, #FFE5E5 0%, #E5F5FF 100%);
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    .narrator-avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin-right: 2rem;
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .narrator-avatar::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.3) 25%, transparent 25%, transparent 50%, rgba(255,255,255,0.3) 50%, rgba(255,255,255,0.3) 75%, transparent 75%);
        background-size: 20px 20px;
        animation: shimmer 2s linear infinite;
        opacity: 0;
    }
    .narrator-avatar.speaking {
        animation: pulse 0.8s ease-in-out infinite alternate;
        box-shadow: 0 0 30px rgba(255, 107, 107, 0.7);
    }
    .narrator-avatar.speaking::before {
        opacity: 1;
    }
    @keyframes pulse {
        0% { 
            transform: scale(1);
            box-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
        }
        100% { 
            transform: scale(1.1);
            box-shadow: 0 0 40px rgba(255, 107, 107, 0.8);
        }
    }
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    .narrator-info {
        flex-grow: 1;
        text-align: center;
    }
    .narrator-name {
        font-size: 2rem;
        font-weight: bold;
        color: #2C3E50;
        margin-bottom: 0.5rem;
    }
    .narrator-status {
        font-size: 1.2rem;
        color: #7F8C8D;
        margin-bottom: 1rem;
    }
    .audio-controls {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 2rem;
    }
    .audio-btn {
        padding: 1rem 2rem;
        border-radius: 25px;
        border: none;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .play-btn {
        background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%);
        color: white;
    }
    .play-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.3);
    }
    .pause-btn {
        background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%);
        color: white;
    }
    .pause-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.3);
    }
    .story-content {
        font-size: 1.3rem;
        line-height: 1.8;
        color: #2C3E50;
        text-align: justify;
        margin: 2rem 0;
        padding: 2rem;
        background: rgba(255,255,255,0.7);
        border-radius: 15px;
        border-left: 5px solid #3498DB;
    }
    .page-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0;
        padding: 1rem;
        background: rgba(255,255,255,0.5);
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="audio-header">
        <div class="audio-title">🎧 Audio Books Collection</div>
        <div class="audio-subtitle">Experience Stories with Voice Narration & Animated Avatars</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if a specific story is selected
    if 'selected_audio_story_id' in st.session_state:
        show_audio_book_reader()
    else:
        show_audio_book_library()

def show_audio_book_library():
    """Display ALL voice-based stories from ALL users"""
    # Get ALL voice-based stories from the entire platform
    all_stories = get_all_stories()
    audio_stories = [story for story in all_stories if story.get('input_method') == 'voice']
    
    if not audio_stories:
        st.markdown("""
        <div class="audio-story-card">
            <h3>🎙️ No Audio Books Yet</h3>
            <p>No voice-narrated stories have been shared yet. Be the first to upload an audio story!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎤 Create Audio Story", type="primary"):
            st.switch_page("pages/3_Upload.py")
        return
    
    st.markdown(f"**🎧 Discover {len(audio_stories)} audio books from storytellers across India!**")
    
    # Filtering options
    col1, col2, col3 = st.columns(3)
    with col1:
        search_query = st.text_input("🔍 Search audio stories:", placeholder="Search by title, festival, author...")
    
    with col2:
        festivals = list(set([story.get('festival', 'Unknown') for story in audio_stories]))
        filter_festival = st.selectbox("Filter by Festival:", ["All Festivals"] + sorted(festivals))
    
    with col3:
        languages = list(set([story.get('language', 'Unknown') for story in audio_stories]))
        filter_language = st.selectbox("Filter by Language:", ["All Languages"] + sorted(languages))
    
    # Additional filters
    col4, col5 = st.columns(2)
    with col4:
        states = list(set([story.get('user_state', 'Unknown') for story in audio_stories if story.get('user_state', 'Unknown') != 'Unknown']))
        filter_state = st.selectbox("Filter by State:", ["All States"] + sorted(states))
    
    with col5:
        authors = list(set([story.get('user_name', 'Anonymous') for story in audio_stories if story.get('user_name', 'Anonymous') != 'Anonymous']))
        filter_author = st.selectbox("Filter by Author:", ["All Authors"] + sorted(authors))
    
    # Filter stories
    filtered_stories = audio_stories
    
    if search_query:
        filtered_stories = [
            story for story in filtered_stories
            if search_query.lower() in story.get('title', '').lower() or
               search_query.lower() in story.get('festival', '').lower() or
               search_query.lower() in story.get('description', '').lower() or
               search_query.lower() in story.get('user_name', '').lower()
        ]
    
    if filter_festival != "All Festivals":
        filtered_stories = [story for story in filtered_stories if story.get('festival') == filter_festival]
    
    if filter_language != "All Languages":
        filtered_stories = [story for story in filtered_stories if story.get('language') == filter_language]
    
    if filter_state != "All States":
        filtered_stories = [story for story in filtered_stories if story.get('user_state') == filter_state]
    
    if filter_author != "All Authors":
        filtered_stories = [story for story in filtered_stories if story.get('user_name') == filter_author]
    
    # Display results
    if not filtered_stories:
        st.warning("No audio stories found matching your search criteria.")
    else:
        st.markdown(f"**🎧 Showing {len(filtered_stories)} audio books**")
        for story in filtered_stories:
            display_audio_story_card(story)

def display_audio_story_card(story):
    """Display an audio story card"""
    col1, col2 = st.columns([3, 1])
    
    author_info = f"by {story.get('user_name', 'Anonymous')}"
    if story.get('user_state', 'Unknown') != 'Unknown':
        author_info += f" from {story.get('user_state')}"
    
    created_date = story.get('created_at', '').split('T')[0] if story.get('created_at') else 'Unknown'
    
    with col1:
        st.markdown(f"""
        <div class="audio-story-card">
            <h3>🎧 {story.get('title', 'Untitled Audio Story')}</h3>
            <p><em>{author_info}</em></p>
            <p><strong>🎊 Festival:</strong> {story.get('festival', 'Unknown')}</p>
            <p><strong>🗣️ Language:</strong> {story.get('language', 'Unknown')}</p>
            <p><strong>📚 Type:</strong> {story.get('story_type', 'Unknown')}</p>
            <p><strong>🎙️ Audio Sections:</strong> {len(story.get('sections', []))}</p>
            <p><strong>📅 Created:</strong> {created_date}</p>
            <p><small>{story.get('description', 'No description available')[:150]}{'...' if len(story.get('description', '')) > 150 else ''}</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button(f"🎧 Listen Now", key=f"listen_{story.get('story_id')}", type="primary"):
            st.session_state.selected_audio_story_id = story.get('story_id')
            st.rerun()

def show_audio_book_reader():
    """Display audio book reader with animated narrator"""
    story_id = st.session_state.selected_audio_story_id
    story = load_story(story_id)
    
    if not story:
        st.error("❌ Audio story not found")
        if st.button("🔙 Back to Audio Library"):
            del st.session_state.selected_audio_story_id
            st.rerun()
        return
    
    # Initialize page number
    if 'current_audio_page' not in st.session_state:
        st.session_state.current_audio_page = 0
    
    sections = story.get('sections', [])
    total_pages = len(sections) + 1
    current_page = st.session_state.current_audio_page
    
    # Display current page
    if current_page == 0:
        show_audio_book_cover(story)
    else:
        show_audio_book_page(story, sections[current_page - 1], current_page)
    
    # Navigation
    show_audio_navigation(total_pages)

def show_audio_book_cover(story):
    """Display audio book cover"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 4rem 2rem; border-radius: 15px; text-align: center; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.3); margin: 2rem 0;">
        <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            🎧 {story.get('title', 'Untitled Audio Story')}
        </div>
        <div style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 2rem;">
            🎊 {story.get('festival', 'Festival')} Audio Book
        </div>
        <div style="font-size: 1rem; opacity: 0.8;">
            <p>Narrated by: {story.get('user_name', 'Anonymous')}</p>
            <p>Language: {story.get('language', 'Unknown')}</p>
            <p>Audio Sections: {len(story.get('sections', []))}</p>
            <p>Created: {story.get('created_at', 'Unknown')[:10] if story.get('created_at') else 'Unknown'}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_audio_book_page(story, section, page_number):
    """Display an audio book page with images and realistic animated narrator"""
    narrator_gender = section.get('narrator_gender', 'Female')
    
    # Get playing state
    is_playing = st.session_state.get(f'audio_playing_page_{page_number}', False)
    
    # Section title
    st.markdown(f"""
    <h2 style="text-align: center; color: #2C3E50; margin-bottom: 2rem; font-size: 2.5rem;">
        🎧 {section.get('title', f'Chapter {page_number}')}
    </h2>
    """, unsafe_allow_html=True)
    
    # Main layout with images and narrator
    images = section.get('images', [])
    
    # Create the main layout
    main_col1, main_col2, main_col3 = st.columns([1, 2, 1])
    
    # Top-left image
    if len(images) >= 1:
        with main_col1:
            try:
                image_bytes = base64.b64decode(images[0])
                st.image(image_bytes, width=120, caption="")
            except:
                st.info("📷 Image 1")
    
    # Center section with animated narrator
    with main_col2:
        # Create realistic animated avatar
        narrator_name = f"Male Narrator" if narrator_gender == "Male" else "Female Narrator"
        
        # Realistic avatar SVG based on gender
        if narrator_gender == "Male":
            avatar_svg = create_male_avatar_svg(is_playing)
        else:
            avatar_svg = create_female_avatar_svg(is_playing)
        
        # Display narrator info
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem; font-weight: bold; color: #2C3E50; margin-bottom: 0.5rem;">
                {narrator_name}
            </div>
            <div style="font-size: 1rem; color: #7F8C8D;">
                {'🎙️ Currently Speaking...' if is_playing else '⏸️ Ready to Narrate'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display animated avatar using HTML component
        st.components.v1.html(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; 
                    background: linear-gradient(135deg, #FFE5E5 0%, #E5F5FF 100%); 
                    border-radius: 20px; padding: 2rem; margin: 1rem 0;
                    box-shadow: 0 8px 20px rgba(0,0,0,0.1); position: relative;">
            
            <div id="narrator_page_{page_number}" style="margin-bottom: 1rem; transition: all 0.3s ease;">
                {avatar_svg}
            </div>
        </div>
        """, height=250)
    
    # Volume control on the right
    with main_col3:
        st.markdown("**🔊 Volume**")
        volume = st.slider("Volume", min_value=0, max_value=100, value=70, key=f"volume_page_{page_number}", help="Adjust audio volume", label_visibility="hidden")
        
        # Bottom-right image (smaller size for audio books)
        if len(images) >= 2:
            try:
                image_bytes = base64.b64decode(images[1])
                st.image(image_bytes, width=120, caption="")
            except:
                st.info("📷 Image 2")
        elif len(images) == 1 and len(images) < 2:
            # Use first image again if only one available
            try:
                image_bytes = base64.b64decode(images[0])
                st.image(image_bytes, width=120, caption="")
            except:
                st.info("📷 Image")
    
    # Story content section
    st.markdown(f"""
    <div style="font-size: 1.3rem; line-height: 1.8; color: #2C3E50; text-align: justify; 
                margin: 2rem 0; padding: 2rem; background: rgba(255,255,255,0.9); 
                border-radius: 15px; border-left: 5px solid #3498DB; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        {section.get('content', 'No content available')}
    </div>
    """, unsafe_allow_html=True)
    
    # Advanced Audio Controls
    st.markdown("---")
    st.markdown(f"<h3 style='text-align: center; color: #2C3E50;'>🎵 Audio Controls</h3>", unsafe_allow_html=True)
    
    # Audio controls in a centered layout
    control_col1, control_col2, control_col3 = st.columns([1, 2, 1])
    
    with control_col2:
        # Create 4 columns for audio controls
        ctrl1, ctrl2, ctrl3, ctrl4 = st.columns(4)
        
        with ctrl1:
            if st.button("⏪ -10s", key=f"backward_10s_page_{page_number}", use_container_width=True, help="Skip backward 10 seconds"):
                st.info("⏪ Skipped backward 10 seconds")
        
        with ctrl2:
            if section.get('audio_data'):
                if st.button("▶️ Play", key=f"play_audio_page_{page_number}", use_container_width=True, type="primary"):
                    try:
                        st.session_state[f'audio_playing_page_{page_number}'] = True
                        
                        # Create temporary audio file for better playback
                        import tempfile
                        import os
                        
                        audio_bytes = base64.b64decode(section['audio_data'])
                        
                        # Create temporary file
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                            temp_file.write(audio_bytes)
                            temp_file_path = temp_file.name
                        
                        # Display audio player with custom controls
                        st.audio(audio_bytes, format='audio/wav', start_time=0)
                        
                        # Clean up temporary file
                        try:
                            os.unlink(temp_file_path)
                        except:
                            pass
                        
                        st.success("🎙️ Audio is playing! Watch the narrator speak!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error playing audio: {str(e)}")
            else:
                st.button("▶️ Play", disabled=True, use_container_width=True, help="No audio available")
        
        with ctrl3:
            if st.button("⏸️ Pause", key=f"pause_audio_page_{page_number}", use_container_width=True):
                st.session_state[f'audio_playing_page_{page_number}'] = False
                st.info("⏸️ Audio paused")
                st.rerun()
        
        with ctrl4:
            if st.button("⏩ +10s", key=f"forward_10s_page_{page_number}", use_container_width=True, help="Skip forward 10 seconds"):
                st.info("⏩ Skipped forward 10 seconds")


def create_male_avatar_svg(is_speaking=False):
    """Create realistic male avatar with enhanced lip-sync animation like Talking Tom"""
    mouth_path = "M60,85 Q75,100 90,85 Q80,95 75,97 Q70,95 60,85 Z" if is_speaking else "M68,90 Q75,93 82,90"
    blink_class = "eyes-blink" if is_speaking else ""
    speaking_class = "mouth-speaking" if is_speaking else ""
    
    return f"""
    <svg width="150" height="150" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <radialGradient id="faceGradient" cx="50%" cy="30%" r="70%">
                <stop offset="0%" style="stop-color:#FFDBAC;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#F4A460;stop-opacity:1" />
            </radialGradient>
            <style>
                .mouth-speaking {{
                    animation: talkingMouth 0.3s ease-in-out infinite;
                    transform-origin: 75px 90px;
                }}
                .eyes-blink {{
                    animation: naturalBlink 3s ease-in-out infinite;
                }}
                .speaking-glow {{
                    animation: speakingGlow 1s ease-in-out infinite alternate;
                }}
                @keyframes talkingMouth {{
                    0% {{ 
                        d: path("M68,90 Q75,93 82,90"); 
                        fill: none;
                    }}
                    25% {{ 
                        d: path("M65,88 Q75,95 85,88 Q78,92 75,94 Q72,92 65,88 Z"); 
                        fill: #FF6B6B;
                    }}
                    50% {{ 
                        d: path("M60,85 Q75,100 90,85 Q80,95 75,97 Q70,95 60,85 Z"); 
                        fill: #FF4444;
                    }}
                    75% {{ 
                        d: path("M65,88 Q75,95 85,88 Q78,92 75,94 Q72,92 65,88 Z"); 
                        fill: #FF6B6B;
                    }}
                    100% {{ 
                        d: path("M68,90 Q75,93 82,90"); 
                        fill: none;
                    }}
                }}
                @keyframes naturalBlink {{
                    0%, 85%, 100% {{ transform: scaleY(1); }}
                    90% {{ transform: scaleY(0.2); }}
                    95% {{ transform: scaleY(1); }}
                }}
                @keyframes speakingGlow {{
                    0% {{ 
                        stroke: #FF6B6B; 
                        stroke-width: 2; 
                        opacity: 0.4; 
                        r: 60;
                    }}
                    100% {{ 
                        stroke: #FF3333; 
                        stroke-width: 4; 
                        opacity: 0.8; 
                        r: 65;
                    }}
                }}
            </style>
        </defs>
        
        <!-- Speaking glow effect -->
        {'<circle cx="75" cy="75" r="60" fill="none" class="speaking-glow"/>' if is_speaking else ''}
        
        <!-- Face -->
        <circle cx="75" cy="75" r="60" fill="url(#faceGradient)" stroke="#D2691E" stroke-width="2"/>
        
        <!-- Hair -->
        <path d="M20,45 Q40,20 75,25 Q110,20 130,45 Q120,35 75,15 Q30,35 20,45 Z" fill="#8B4513"/>
        
        <!-- Eyes -->
        <g class="{blink_class}">
            <ellipse cx="55" cy="65" rx="8" ry="6" fill="white"/>
            <ellipse cx="95" cy="65" rx="8" ry="6" fill="white"/>
            <circle cx="55" cy="65" r="4" fill="#4169E1"/>
            <circle cx="95" cy="65" r="4" fill="#4169E1"/>
            <circle cx="57" cy="63" r="1.5" fill="white"/>
            <circle cx="97" cy="63" r="1.5" fill="white"/>
        </g>
        
        <!-- Eyebrows -->
        <path d="M45,55 Q55,50 65,55" stroke="#654321" stroke-width="3" fill="none"/>
        <path d="M85,55 Q95,50 105,55" stroke="#654321" stroke-width="3" fill="none"/>
        
        <!-- Nose -->
        <path d="M75,70 L75,85 M70,82 Q75,85 80,82" stroke="#CD853F" stroke-width="2" fill="none"/>
        
        <!-- Mouth with enhanced animation -->
        <path d="{mouth_path}" stroke="#8B4513" stroke-width="3" fill="{'#FF6B6B' if is_speaking else 'none'}" 
              class="{speaking_class}"/>
        
        <!-- Tongue for speaking effect -->
        {'<ellipse cx="75" cy="92" rx="8" ry="3" fill="#FF9999" opacity="0.7" class="mouth-speaking"/>' if is_speaking else ''}
    </svg>
    """


def create_female_avatar_svg(is_speaking=False):
    """Create realistic female avatar with lip-sync animation"""
    mouth_shape = "M65,90 Q80,100 95,90" if is_speaking else "M70,95 Q80,98 90,95"
    blink_class = "blink" if is_speaking else ""
    
    return f"""
    <svg width="150" height="150" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <radialGradient id="femaleGradient" cx="50%" cy="30%" r="70%">
                <stop offset="0%" style="stop-color:#FFEAA7;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#FAB1A0;stop-opacity:1" />
            </radialGradient>
            <style>
                .mouth-speaking {{
                    animation: speak 0.5s ease-in-out infinite alternate;
                }}
                .eyes-blink {{
                    animation: blink 2s ease-in-out infinite;
                }}
                @keyframes speak {{
                    0% {{ d: path("M70,95 Q80,98 90,95"); }}
                    100% {{ d: path("M65,90 Q80,105 95,90"); }}
                }}
                @keyframes blink {{
                    0%, 90%, 100% {{ transform: scaleY(1); }}
                    5% {{ transform: scaleY(0.1); }}
                }}
                .pulse {{
                    animation: pulse-glow 1s ease-in-out infinite alternate;
                }}
                @keyframes pulse-glow {{
                    0% {{ opacity: 0.3; }}
                    100% {{ opacity: 0.7; }}
                }}
            </style>
        </defs>
        
        <!-- Face -->
        <circle cx="75" cy="75" r="58" fill="url(#femaleGradient)" stroke="#E17055" stroke-width="2"/>
        
        <!-- Hair (longer, more feminine) -->
        <path d="M15,50 Q30,15 75,20 Q120,15 135,50 Q140,70 130,90 Q120,70 110,85 Q100,75 95,90 Q85,80 80,95 Q75,85 70,95 Q65,80 55,90 Q45,75 40,85 Q30,70 20,90 Q10,70 15,50 Z" fill="#D63031"/>
        
        <!-- Eyes (larger, more feminine) -->
        <g class="{blink_class}">
            <ellipse cx="55" cy="65" rx="10" ry="7" fill="white"/>
            <ellipse cx="95" cy="65" rx="10" ry="7" fill="white"/>
            <circle cx="55" cy="65" r="5" fill="#00B894"/>
            <circle cx="95" cy="65" r="5" fill="#00B894"/>
            <circle cx="57" cy="63" r="2" fill="white"/>
            <circle cx="97" cy="63" r="2" fill="white"/>
        </g>
        
        <!-- Eyelashes -->
        <path d="M45,60 L50,58 M47,63 L52,60 M48,66 L53,64" stroke="#2D3436" stroke-width="1"/>
        <path d="M105,60 L100,58 M103,63 L98,60 M102,66 L97,64" stroke="#2D3436" stroke-width="1"/>
        
        <!-- Eyebrows (more arched) -->
        <path d="M43,52 Q55,47 67,52" stroke="#A29BFE" stroke-width="2" fill="none"/>
        <path d="M83,52 Q95,47 107,52" stroke="#A29BFE" stroke-width="2" fill="none"/>
        
        <!-- Nose (smaller, more delicate) -->
        <path d="M75,70 L75,83 M72,80 Q75,83 78,80" stroke="#FDCB6E" stroke-width="1.5" fill="none"/>
        
        <!-- Mouth (with lipstick) -->
        <path d="{mouth_shape}" stroke="#E84393" stroke-width="2" fill="{'#FD79A8' if is_speaking else '#FDCB6E'}" 
              class="{'mouth-speaking' if is_speaking else ''}"/>
        
        <!-- Blush -->
        <circle cx="50" cy="80" r="6" fill="#FD79A8" opacity="0.3"/>
        <circle cx="100" cy="80" r="6" fill="#FD79A8" opacity="0.3"/>
        
        <!-- Speaking animation glow -->
        {'<circle cx="75" cy="75" r="65" fill="none" stroke="#FD79A8" stroke-width="3" opacity="0.6" class="pulse"/>' if is_speaking else ''}
    </svg>
    """

def show_audio_navigation(total_pages):
    """Display audio book navigation controls"""
    current_page = st.session_state.current_audio_page
    
    st.markdown("---")
    
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if st.button("🔙 Back to Audio Library", key="back_to_audio_library"):
            del st.session_state.selected_audio_story_id
            if 'current_audio_page' in st.session_state:
                del st.session_state.current_audio_page
            st.rerun()
    
    with col2:
        if current_page > 0:
            if st.button("⬅️ Previous", key="prev_audio_page"):
                st.session_state.current_audio_page -= 1
                st.rerun()
    
    with col3:
        if current_page == 0:
            page_info = "🎧 Audio Book Cover"
        else:
            page_info = f"🎙️ Chapter {current_page} of {total_pages - 1}"
        
        st.markdown(f'<div style="text-align: center; font-size: 1.1rem; color: #2C3E50; font-weight: bold; background: rgba(255,255,255,0.7); padding: 0.5rem; border-radius: 10px;">{page_info}</div>', unsafe_allow_html=True)
    
    with col4:
        if current_page < total_pages - 1:
            if st.button("Next ➡️", key="next_audio_page"):
                st.session_state.current_audio_page += 1
                st.rerun()
    
    with col5:
        if st.button("📖 View Virtual Books", key="switch_to_virtual"):
            st.switch_page("pages/6_PublicBooks.py")
    
    # Progress bar
    progress = (current_page + 1) / total_pages
    st.progress(progress, text=f"Listening Progress: {int(progress * 100)}%")

if __name__ == "__main__":
    main()