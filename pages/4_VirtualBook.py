import streamlit as st
from utils.auth import check_authentication, get_current_user
from utils.db import get_user_stories, load_story
import base64
import json

# Page configuration
st.set_page_config(
    page_title="Virtual Book - Utsav Kathalu AI",
    page_icon="📖",
    layout="wide"
)

def main():
    """Main virtual book interface"""
    if not check_authentication():
        st.warning("🔒 Please login to access your stories.")
        if st.button("🔑 Go to Login"):
            st.switch_page("pages/2_Auth.py")
        return
    
    user_data = get_current_user()
    user_email = user_data.get('email', '')
    
    if not user_email:
        st.error("❌ User session error. Please login again.")
        if st.button("🔑 Go to Login"):
            st.switch_page("pages/2_Auth.py")
        return
    
    user_stories = get_user_stories(user_email)
    
    if not user_stories:
        st.info("📚 No stories found yet!")
        st.markdown("### 🌟 Get Started")
        st.write("Ready to share your first festival story? Upload it now and watch it come to life as a beautiful virtual book!")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📝 Upload Your First Story", type="primary", use_container_width=True):
                st.switch_page("pages/3_Upload.py")
                
            if st.button("🎭 Try Sample Stories", use_container_width=True):
                st.switch_page("app.py")
        return
    
    show_virtual_book(user_stories)

def show_virtual_book(user_stories):
    """Display the virtual book interface"""
    # Custom CSS for book interface
    st.markdown("""
    <style>
    .book-header {
        text-align: center;
        color: #D4AF37;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .book-container {
        background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
        padding: 3rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        position: relative;
    }
    .book-page {
        background: linear-gradient(135deg, #FFFEF7 0%, #FFF8DC 100%);
        padding: 3rem;
        border-radius: 15px;
        min-height: 800px;
        position: relative;
        border: 1px solid #DEB887;
        margin: 1rem 0;
        display: grid;
        grid-template-columns: 1fr 2fr 1fr;
        grid-template-rows: auto 1fr auto;
        gap: 1rem;
        transform-style: preserve-3d;
        backface-visibility: hidden;
    }
    .page-image-top {
        grid-column: 1;
        grid-row: 1;
        max-width: 200px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .page-image-bottom {
        grid-column: 3;
        grid-row: 3;
        max-width: 200px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        justify-self: end;
    }
    .page-content-center {
        grid-column: 1 / -1;
        grid-row: 2;
        font-size: 1.1rem;
        line-height: 1.8;
        color: #2F4F4F;
        text-align: justify;
        padding: 1rem;
    }
    .page-turn-animation {
        transform-style: preserve-3d;
        transition: transform 0.8s ease-in-out;
        transform-origin: left center;
    }
    
    .page-turning {
        animation: pageTurn 0.8s ease-in-out;
    }
    
    @keyframes pageTurn {
        0% { transform: perspective(1200px) rotateY(0deg); }
        50% { transform: perspective(1200px) rotateY(-90deg); }
        100% { transform: perspective(1200px) rotateY(0deg); }
    }
    
    .page-shadow {
        box-shadow: 
            inset 0 0 50px rgba(139,69,19,0.1),
            0 20px 40px rgba(0,0,0,0.15),
            inset -10px 0 20px rgba(0,0,0,0.05);
    }
    .voice-controls {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: rgba(255,255,255,0.9);
        padding: 0.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .page-header {
        color: #8B4513;
        font-size: 2rem;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 2px solid #D4AF37;
        padding-bottom: 1rem;
    }
    .page-content {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #2F4F4F;
        text-align: justify;
        margin-bottom: 2rem;
    }
    .page-number {
        position: absolute;
        bottom: 1rem;
        right: 2rem;
        color: #8B4513;
        font-style: italic;
    }
    .book-navigation {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 2rem;
        padding: 1rem;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    .story-card {
        background: linear-gradient(135deg, #FFF8DC 0%, #F0E68C 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #FF6B35;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    .story-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .book-cover {
        background: linear-gradient(135deg, #4A90E2 0%, #7B68EE 50%, #FF6B6B 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 2rem 0;
    }
    .cover-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .cover-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    .cover-details {
        font-size: 1rem;
        opacity: 0.8;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please login to view virtual books")
        if st.button("🔑 Go to Login"):
            st.switch_page("pages/2_Auth.py")
        return
    
    st.markdown('<h1 class="book-header">📖 My Virtual Books - Text-Based Stories</h1>', unsafe_allow_html=True)
    
    # Check if a specific story is selected
    if 'selected_story_id' in st.session_state:
        show_story_reader()
    else:
        show_story_library()

def show_story_library():
    """Display user's own stories"""
    # Get current user's email
    user_data = get_current_user()
    user_email = user_data.get('email', '')
    
    # Get only current user's text-based stories (virtual books)
    user_stories = get_user_stories(user_email)
    all_stories = [story for story in user_stories if story.get('input_method') == 'text']
    
    if not all_stories:
        st.markdown("""
        <div class="story-card">
            <h3>📚 No Virtual Books Yet</h3>
            <p>You haven't created any text-based stories yet. Upload a story using text input to see your virtual books here!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Create Text Story", type="primary", use_container_width=True):
                st.switch_page("pages/3_Upload.py")
        with col2:
            if st.button("🎙️ View Audio Books", use_container_width=True):
                st.switch_page("pages/8_MyAudioBooks.py")
        return
    
    st.markdown(f"**📚 Your Virtual Books: {len(all_stories)} text-based stories**")
    
    # Enhanced filtering and search for ALL stories
    col1, col2, col3 = st.columns(3)
    with col1:
        search_query = st.text_input("🔍 Search stories:", placeholder="Search by title, festival, author...")
    
    with col2:
        festivals = list(set([story.get('festival', 'Unknown') for story in all_stories]))
        filter_festival = st.selectbox("Filter by Festival:", ["All Festivals"] + sorted(festivals))
    
    with col3:
        languages = list(set([story.get('language', 'Unknown') for story in all_stories]))
        filter_language = st.selectbox("Filter by Language:", ["All Languages"] + sorted(languages))
    
    # Additional filters
    col4, col5 = st.columns(2)
    with col4:
        states = list(set([story.get('user_state', 'Unknown') for story in all_stories if story.get('user_state', 'Unknown') != 'Unknown']))
        filter_state = st.selectbox("Filter by State:", ["All States"] + sorted(states))
    
    with col5:
        authors = list(set([story.get('user_name', 'Anonymous') for story in all_stories if story.get('user_name', 'Anonymous') != 'Anonymous']))
        filter_author = st.selectbox("Filter by Author:", ["All Authors"] + sorted(authors))
    
    # Filter stories based on all criteria
    filtered_stories = all_stories
    
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
    
    # Display filtered results
    if not filtered_stories:
        st.warning("No stories found matching your search criteria.")
    else:
        st.markdown(f"**📖 Showing {len(filtered_stories)} stories**")
        for story in filtered_stories:
            display_story_card(story)

def display_story_card(story):
    """Display a story card in the library with author information"""
    col1, col2 = st.columns([3, 1])
    
    # Enhanced story card with author info
    author_info = f"by {story.get('user_name', 'Anonymous')}"
    if story.get('user_state', 'Unknown') != 'Unknown':
        author_info += f" from {story.get('user_state')}"
    
    created_date = story.get('created_at', '').split('T')[0] if story.get('created_at') else 'Unknown'
    
    with col1:
        st.markdown(f"""
        <div class="story-card">
            <h3>📖 {story.get('title', 'Untitled Story')}</h3>
            <p><em>{author_info}</em></p>
            <p><strong>🎊 Festival:</strong> {story.get('festival', 'Unknown')}</p>
            <p><strong>🗣️ Language:</strong> {story.get('language', 'Unknown')}</p>
            <p><strong>📚 Type:</strong> {story.get('story_type', 'Unknown')}</p>
            <p><strong>📄 Sections:</strong> {len(story.get('sections', []))}</p>
            <p><strong>📅 Created:</strong> {created_date}</p>
            <p><small>{story.get('description', 'No description available')[:150]}{'...' if len(story.get('description', '')) > 150 else ''}</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button(f"📖 Read Story", key=f"read_{story.get('story_id')}", type="primary"):
            st.session_state.selected_story_id = story.get('story_id')
            st.rerun()
        
        if st.button(f"ℹ️ Details", key=f"details_{story.get('story_id')}"):
            show_story_details(story)

def show_story_details(story):
    """Show detailed story information"""
    with st.expander(f"📋 Story Details: {story.get('title', 'Untitled')}", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Story ID:** {story.get('story_id', 'N/A')}")
            st.write(f"**Title:** {story.get('title', 'N/A')}")
            st.write(f"**Festival:** {story.get('festival', 'N/A')}")
            st.write(f"**Language:** {story.get('language', 'N/A')}")
            st.write(f"**Type:** {story.get('story_type', 'N/A')}")
        
        with col2:
            st.write(f"**Input Method:** {story.get('input_method', 'N/A')}")
            st.write(f"**Sections:** {len(story.get('sections', []))}")
            st.write(f"**Images:** {len(story.get('images', {}))}")
            st.write(f"**Created:** {story.get('created_at', 'N/A')}")
            st.write(f"**Updated:** {story.get('updated_at', 'N/A')}")
        
        st.write(f"**Description:** {story.get('description', 'No description available')}")
        
        # AI Enhancement details
        if story.get('ai_enhancements'):
            with st.expander("🤖 AI Enhancement Details"):
                enhancements = story.get('ai_enhancements', {})
                if 'improvements_made' in enhancements:
                    st.write("**Improvements Made:**")
                    for improvement in enhancements['improvements_made']:
                        st.write(f"• {improvement}")
                
                if 'confidence_score' in enhancements:
                    st.metric("AI Confidence Score", f"{enhancements['confidence_score'] * 100:.1f}%")

def show_story_reader():
    """Display story as virtual book"""
    story_id = st.session_state.selected_story_id
    story = load_story(story_id)
    
    if not story:
        st.error("❌ Story not found")
        if st.button("🔙 Back to Library"):
            del st.session_state.selected_story_id
            st.rerun()
        return
    
    # Initialize page number
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0  # 0 for cover page
    
    # Book navigation
    sections = story.get('sections', [])
    total_pages = len(sections) + 1  # +1 for cover page
    current_page = st.session_state.current_page
    
    # Display current page
    if current_page == 0:
        show_book_cover(story)
    else:
        show_book_page(story, sections[current_page - 1], current_page)
    
    # Navigation controls
    show_book_navigation(total_pages)

def show_book_cover(story):
    """Display book cover page"""
    st.markdown(f"""
    <div class="book-cover">
        <div class="cover-title">📖 {story.get('title', 'Untitled Story')}</div>
        <div class="cover-subtitle">🎊 {story.get('festival', 'Festival')} Story</div>
        <div class="cover-details">
            <p>By: {story.get('user_name', 'Anonymous')}</p>
            <p>Language: {story.get('language', 'Unknown')}</p>
            <p>Story Type: {story.get('story_type', 'Unknown')}</p>
            <p>Created: {story.get('created_at', 'Unknown')[:10] if story.get('created_at') else 'Unknown'}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Story description with consistent sizing and animation
    import html
    animation_class = "page-turning" if st.session_state.get('page_turning') else ""
    
    st.markdown(f"""
    <div class="book-page page-shadow {animation_class}">
        <div class="page-header" style="grid-column: 1 / -1; text-align: center; margin-bottom: 1rem; font-size: 1.5rem; color: #8B4513; font-weight: bold;">📖 About This Story</div>
        <div class="page-content-center">
            {html.escape(story.get('description', 'No description available')).replace(chr(10), '<br>')}
        </div>
        <div class="page-number" style="grid-column: -1; text-align: right; margin-top: 1rem;">Cover Page</div>
    </div>
    """, unsafe_allow_html=True)

def show_book_page(story, section, page_number):
    """Display a book page with improved layout"""
    
    # Voice controls for voice-input stories
    if story.get('input_method') == 'voice':
        show_voice_controls(section, page_number)
    
    # Create the main page layout
    images = story.get('images', {})
    image1_key = f"section_{page_number}_image_1"
    image2_key = f"section_{page_number}_image_2"
    
    # Prepare images
    image1_data = None
    image2_data = None
    
    if image1_key in images:
        try:
            image1_data = base64.b64decode(images[image1_key])
        except Exception:
            pass
    
    if image2_key in images:
        try:
            image2_data = base64.b64decode(images[image2_key])
        except Exception:
            pass
    
    # Add page turning animation class if triggered
    animation_class = "page-turning" if st.session_state.get('page_turning') else ""
    
    # Create page HTML with images positioned correctly
    page_html = f"""
    <div class="book-page page-shadow {animation_class}">
        <div class="page-header" style="grid-column: 1 / -1; text-align: center; margin-bottom: 1rem; font-size: 1.5rem; color: #8B4513; font-weight: bold;">
            {section.get('title', f'Chapter {page_number}')}
        </div>
    """
    
    # Add top-left image if available
    if image1_data:
        image1_b64 = base64.b64encode(image1_data).decode()
        page_html += f"""
        <img src="data:image/jpeg;base64,{image1_b64}" class="page-image-top" alt="Section illustration 1">
        """
    
    # Add content in the center with proper HTML escaping
    import html
    content = section.get('content', 'No content available')
    # Clean content and convert newlines to breaks
    clean_content = html.escape(content).replace('\n', '<br>')
    
    page_html += f"""
        <div class="page-content-center">
            {clean_content}
        </div>
    """
    
    # Add bottom-right image if available
    if image2_data:
        image2_b64 = base64.b64encode(image2_data).decode()
        page_html += f"""
        <img src="data:image/jpeg;base64,{image2_b64}" class="page-image-bottom" alt="Section illustration 2">
        """
    
    page_html += f"""
        <div class="page-number" style="grid-column: -1; text-align: right; margin-top: 1rem;">
            Page {page_number}
        </div>
    </div>
    """
    
    st.markdown(page_html, unsafe_allow_html=True)

def show_voice_controls(section, page_number):
    """Show animated narrator and voice playback controls for audio stories"""
    narrator_gender = section.get('narrator_gender', 'Female')
    
    # CSS for animated avatar
    st.markdown("""
    <style>
    .audio-narrator-container {
        position: relative;
        display: flex;
        align-items: center;
        background: linear-gradient(135deg, #E6F3FF 0%, #CCE7FF 100%);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .narrator-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        margin-right: 1rem;
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        animation: speakingAnimation 0.5s ease-in-out infinite alternate;
    }
    .narrator-avatar.speaking {
        animation: speakingAnimation 0.5s ease-in-out infinite alternate;
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
    }
    .narrator-info {
        flex-grow: 1;
    }
    .audio-controls {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    @keyframes speakingAnimation {
        0% { 
            transform: scale(1);
            box-shadow: 0 0 10px rgba(255, 107, 107, 0.3);
        }
        100% { 
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(255, 107, 107, 0.6);
        }
    }
    .play-button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1rem;
    }
    .pause-button {
        background: linear-gradient(135deg, #f44336 0%, #da190b 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Avatar emoji based on gender
    avatar_emoji = "👨" if narrator_gender == "Male" else "👩"
    narrator_name = "Male Narrator" if narrator_gender == "Male" else "Female Narrator"
    
    # Audio narrator container
    st.markdown(f"""
    <div class="audio-narrator-container">
        <div class="narrator-avatar {'speaking' if st.session_state.get(f'audio_playing_{page_number}', False) else ''}" id="narrator_{page_number}">
            {avatar_emoji}
        </div>
        <div class="narrator-info">
            <h4>🎭 {narrator_name}</h4>
            <p>Ready to narrate Section {page_number}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Audio controls
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"▶️ Play Audio", key=f"play_voice_{page_number}", type="primary"):
            if section.get('audio_data'):
                try:
                    # Set playing state
                    st.session_state[f'audio_playing_{page_number}'] = True
                    
                    # Create audio player
                    audio_bytes = base64.b64decode(section['audio_data'])
                    st.audio(audio_bytes, format='audio/wav')
                    
                    # JavaScript to add animation during playback
                    st.markdown(f"""
                    <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        const narrator = document.getElementById('narrator_{page_number}');
                        if (narrator) {{
                            narrator.classList.add('speaking');
                            
                            // Remove animation after estimated audio duration
                            setTimeout(() => {{
                                narrator.classList.remove('speaking');
                            }}, 10000); // 10 seconds default, adjust based on audio length
                        }}
                    }});
                    </script>
                    """, unsafe_allow_html=True)
                    
                    st.success("🎙️ Audio is playing! Watch the narrator come to life!")
                    
                except Exception as e:
                    st.error(f"Error playing audio: {str(e)}")
            else:
                st.info("No audio data available for this section")
    
    with col2:
        if st.button(f"⏹️ Stop", key=f"stop_voice_{page_number}"):
            # Reset playing state
            st.session_state[f'audio_playing_{page_number}'] = False
            st.info("Audio stopped")
            st.rerun()

def show_book_navigation(total_pages):
    """Display book navigation controls with animations"""
    st.markdown("---")
    
    # Add page turn sound effect (CSS animation)
    st.markdown("""
    <style>
    .nav-button {
        transition: all 0.3s ease;
        transform-origin: center;
    }
    .nav-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .page-indicator {
        text-align: center; 
        font-size: 1.1rem; 
        color: #8B4513; 
        font-weight: bold;
        background: linear-gradient(135deg, #FFF8DC 0%, #F0E68C 100%);
        padding: 0.5rem;
        border-radius: 10px;
        border: 2px solid #D4AF37;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if st.button("🔙 Back to Library", key="back_to_library"):
            del st.session_state.selected_story_id
            if 'current_page' in st.session_state:
                del st.session_state.current_page
            st.rerun()
    
    with col2:
        if st.session_state.current_page > 0:
            if st.button("⬅️ Previous", key="prev_page"):
                st.session_state.current_page -= 1
                # Add page turn animation trigger
                st.session_state.page_turning = True
                st.rerun()
    
    with col3:
        # Page indicator with better styling
        current = st.session_state.current_page
        if current == 0:
            page_info = "📖 Cover Page"
        else:
            page_info = f"📄 Page {current} of {total_pages - 1}"
        
        st.markdown(f'<div class="page-indicator">{page_info}</div>', unsafe_allow_html=True)
    
    with col4:
        if st.session_state.current_page < total_pages - 1:
            if st.button("Next ➡️", key="next_page"):
                st.session_state.current_page += 1
                # Add page turn animation trigger
                st.session_state.page_turning = True
                st.rerun()
    
    with col5:
        # Quick jump to pages
        page_options = ["Cover"] + [f"Page {i}" for i in range(1, total_pages)]
        selected_page = st.selectbox(
            "Jump to:",
            page_options,
            index=st.session_state.current_page,
            key="page_selector"
        )
        
        if selected_page == "Cover":
            target_page = 0
        else:
            target_page = int(selected_page.split()[1])
        
        if target_page != st.session_state.current_page:
            st.session_state.current_page = target_page
            st.session_state.page_turning = True
            st.rerun()
    
    # Enhanced progress bar
    progress = (st.session_state.current_page + 1) / total_pages
    st.progress(progress, text=f"Reading Progress: {int(progress * 100)}%")
    
    # Clear page turning animation flag after a delay
    if st.session_state.get('page_turning'):
        # Use JavaScript to clear the animation after it completes
        st.markdown("""
        <script>
        setTimeout(function() {
            var elements = document.getElementsByClassName('page-turning');
            for (var i = 0; i < elements.length; i++) {
                elements[i].classList.remove('page-turning');
            }
        }, 800);
        </script>
        """, unsafe_allow_html=True)
        st.session_state.page_turning = False

if __name__ == "__main__":
    main()
