import streamlit as st
from utils.db import get_all_stories, load_story
import base64
import html

def main():
    """Public Virtual Book Library - Login required"""
    from utils.auth import check_authentication
    
    # Check authentication - login required for public books too
    if not check_authentication():
        st.error("🔒 Please login to explore festival stories")
        if st.button("🔑 Go to Login"):
            st.switch_page("pages/2_Auth.py")
        return
    
    # Custom CSS for the public book library
    st.markdown("""
    <style>
    .public-header {
        background: linear-gradient(135deg, #FF6B35 0%, #F39C12 50%, #D4AF37 100%);
        color: white;
        text-align: center;
        padding: 3rem 1rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .public-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .public-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-bottom: 1rem;
    }
    .story-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    .public-story-card {
        background: linear-gradient(135deg, #FFF8DC 0%, #F0E68C 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #FF6B35;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
    }
    .public-story-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .filter-section {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 2rem 0;
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
        box-shadow: 
            inset 0 0 50px rgba(139,69,19,0.1),
            0 20px 40px rgba(0,0,0,0.15),
            inset -10px 0 20px rgba(0,0,0,0.05);
    }
    .page-content-center {
        grid-column: 1 / -1;
        font-size: 1.2rem;
        line-height: 1.8;
        color: #2F4F4F;
        text-align: justify;
        padding: 1rem;
    }
    .page-image-top {
        grid-column: 1;
        grid-row: 2;
        width: 100%;
        max-height: 300px;
        object-fit: cover;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .page-image-bottom {
        grid-column: 3;
        grid-row: 2;
        width: 100%;
        max-height: 300px;
        object-fit: cover;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        align-self: end;
    }
    .navigation-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0;
        padding: 1rem;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Public header
    st.markdown("""
    <div class="public-header">
        <div class="public-title">📚 Utsav Kathalu AI</div>
        <div class="public-subtitle">Explore Festival Stories from Across India</div>
        <p>Discover authentic cultural stories and traditions shared by storytellers nationwide</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if viewing a specific story
    if 'public_selected_story' in st.session_state:
        show_public_story_viewer()
    else:
        show_public_story_library()

def show_public_story_library():
    """Display all stories for authenticated users"""
    from utils.db import get_all_stories
    
    # Get all text-based stories only (virtual books)
    all_stories = get_all_stories()
    all_stories = [story for story in all_stories if story.get('input_method') == 'text']
    
    if not all_stories:
        st.markdown("""
        <div class="public-story-card">
            <h3>📖 Welcome to Virtual Books!</h3>
            <p>This is where you can explore text-based festival stories from storytellers across India.</p>
            <p>No virtual books have been shared yet. Be the first to contribute by uploading a text-based story!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Create Virtual Book", type="primary", use_container_width=True):
                st.switch_page("pages/3_Upload.py")
        with col2:
            if st.button("🎧 Explore Audio Books", use_container_width=True):
                st.switch_page("pages/7_AudioBooks.py")
        return
    
    # Filtering section
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown("### 🔍 Explore Stories")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        search_query = st.text_input("Search stories:", placeholder="Title, festival, author...")
    
    with col2:
        festivals = sorted(set([story.get('festival', 'Unknown') for story in all_stories]))
        selected_festival = st.selectbox("Festival:", ["All Festivals"] + festivals)
    
    with col3:
        languages = sorted(set([story.get('language', 'Unknown') for story in all_stories]))
        selected_language = st.selectbox("Language:", ["All Languages"] + languages)
    
    col4, col5 = st.columns(2)
    with col4:
        states = sorted(set([story.get('user_state', 'Unknown') for story in all_stories if story.get('user_state', 'Unknown') != 'Unknown']))
        selected_state = st.selectbox("State:", ["All States"] + states)
    
    with col5:
        authors = sorted(set([story.get('user_name', 'Anonymous') for story in all_stories if story.get('user_name', 'Anonymous') != 'Anonymous']))
        selected_author = st.selectbox("Author:", ["All Authors"] + authors)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter stories
    filtered_stories = all_stories
    
    if search_query:
        filtered_stories = [
            story for story in filtered_stories
            if search_query.lower() in story.get('title', '').lower() or
               search_query.lower() in story.get('festival', '').lower() or
               search_query.lower() in story.get('user_name', '').lower()
        ]
    
    if selected_festival != "All Festivals":
        filtered_stories = [s for s in filtered_stories if s.get('festival') == selected_festival]
    
    if selected_language != "All Languages":
        filtered_stories = [s for s in filtered_stories if s.get('language') == selected_language]
    
    if selected_state != "All States":
        filtered_stories = [s for s in filtered_stories if s.get('user_state') == selected_state]
    
    if selected_author != "All Authors":
        filtered_stories = [s for s in filtered_stories if s.get('user_name') == selected_author]
    
    # Display results
    st.markdown(f"### 📖 {len(filtered_stories)} Virtual Books Found")
    
    if filtered_stories:
        # Display stories in grid
        cols = st.columns(2)
        for i, story in enumerate(filtered_stories):
            col = cols[i % 2]
            with col:
                display_public_story_card(story)
    else:
        st.warning("No virtual books match your search criteria.")
        
        # Add button to switch to audio books
        if st.button("🎧 Try Audio Books Instead"):
            st.switch_page("pages/7_AudioBooks.py")

def display_public_story_card(story):
    """Display a story card for public viewing"""
    author_info = f"by {story.get('user_name', 'Anonymous')}"
    if story.get('user_state', 'Unknown') != 'Unknown':
        author_info += f" from {story.get('user_state')}"
    
    created_date = story.get('created_at', '').split('T')[0] if story.get('created_at') else 'Unknown'
    description = story.get('description', 'No description available')
    preview_text = description[:120] + '...' if len(description) > 120 else description
    
    st.markdown(f"""
    <div class="public-story-card">
        <h3>📖 {story.get('title', 'Untitled Story')}</h3>
        <p><em>{author_info}</em></p>
        <p><strong>🎊 Festival:</strong> {story.get('festival', 'Unknown')}</p>
        <p><strong>🗣️ Language:</strong> {story.get('language', 'Unknown')}</p>
        <p><strong>📚 Sections:</strong> {len(story.get('sections', []))}</p>
        <p><strong>📅 Created:</strong> {created_date}</p>
        <p style="margin-top: 1rem; font-style: italic;">{preview_text}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"📖 Read Story", key=f"public_read_{story.get('story_id')}", use_container_width=True):
        st.session_state.public_selected_story = story.get('story_id')
        st.session_state.public_current_page = 0
        st.rerun()

def show_public_story_viewer():
    """Display story reader for public viewing"""
    story_id = st.session_state.public_selected_story
    story = load_story(story_id)
    
    if not story:
        st.error("Story not found")
        if st.button("🔙 Back to Library"):
            del st.session_state.public_selected_story
            st.rerun()
        return
    
    # Initialize page
    if 'public_current_page' not in st.session_state:
        st.session_state.public_current_page = 0
    
    sections = story.get('sections', [])
    total_pages = len(sections) + 1  # +1 for cover
    current_page = st.session_state.public_current_page
    
    # Display current page
    if current_page == 0:
        show_public_book_cover(story)
    else:
        show_public_book_page(story, sections[current_page - 1], current_page)
    
    # Navigation
    show_public_navigation(total_pages)

def show_public_book_cover(story):
    """Display book cover for public viewing"""
    author_info = f"by {story.get('user_name', 'Anonymous')}"
    if story.get('user_state', 'Unknown') != 'Unknown':
        author_info += f" from {story.get('user_state')}"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #4A90E2 0%, #7B68EE 50%, #FF6B6B 100%); 
                color: white; padding: 4rem 2rem; border-radius: 15px; text-align: center; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.3); margin: 2rem 0;">
        <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            📖 {story.get('title', 'Untitled Story')}
        </div>
        <div style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 2rem;">
            🎊 {story.get('festival', 'Festival')} Story
        </div>
        <div style="font-size: 1rem; opacity: 0.8;">
            {author_info}<br>
            Language: {story.get('language', 'Unknown')} | 
            {len(story.get('sections', []))} Sections
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Story description
    description = story.get('description', 'No description available')
    clean_description = html.escape(description).replace('\n', '<br>')
    
    st.markdown(f"""
    <div class="book-page">
        <div style="grid-column: 1 / -1; text-align: center; margin-bottom: 1rem; 
                   font-size: 1.5rem; color: #8B4513; font-weight: bold;">
            📖 About This Story
        </div>
        <div class="page-content-center">
            {clean_description}
        </div>
        <div style="grid-column: -1; text-align: right; margin-top: 1rem; color: #8B4513; font-style: italic;">
            Cover Page
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_public_book_page(story, section, page_number):
    """Display a book page for public viewing"""
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
    
    # Clean content
    content = section.get('content', 'No content available')
    clean_content = html.escape(content).replace('\n', '<br>')
    
    # Create page HTML
    page_html = f"""
    <div class="book-page">
        <div style="grid-column: 1 / -1; text-align: center; margin-bottom: 1rem; 
                   font-size: 1.5rem; color: #8B4513; font-weight: bold;">
            {html.escape(section.get('title', f'Chapter {page_number}'))}
        </div>
    """
    
    # Add top-left image
    if image1_data:
        image1_b64 = base64.b64encode(image1_data).decode()
        page_html += f'<img src="data:image/jpeg;base64,{image1_b64}" class="page-image-top" alt="Illustration 1">'
    
    # Add content
    page_html += f'<div class="page-content-center">{clean_content}</div>'
    
    # Add bottom-right image
    if image2_data:
        image2_b64 = base64.b64encode(image2_data).decode()
        page_html += f'<img src="data:image/jpeg;base64,{image2_b64}" class="page-image-bottom" alt="Illustration 2">'
    
    page_html += f"""
        <div style="grid-column: -1; text-align: right; margin-top: 1rem; color: #8B4513; font-style: italic;">
            Page {page_number}
        </div>
    </div>
    """
    
    st.markdown(page_html, unsafe_allow_html=True)

def show_public_navigation(total_pages):
    """Show navigation controls for public viewing"""
    current_page = st.session_state.public_current_page
    
    st.markdown('<div class="navigation-controls">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if st.button("🔙 Library", use_container_width=True):
            del st.session_state.public_selected_story
            if 'public_current_page' in st.session_state:
                del st.session_state.public_current_page
            st.rerun()
    
    with col2:
        if current_page > 0:
            if st.button("◀ Previous", use_container_width=True):
                st.session_state.public_current_page = current_page - 1
                st.rerun()
    
    with col3:
        st.markdown(f"<p style='text-align: center; margin: 0; padding: 0.5rem;'>Page {current_page + 1} of {total_pages}</p>", unsafe_allow_html=True)
        progress = (current_page + 1) / total_pages
        st.progress(progress)
    
    with col4:
        if current_page < total_pages - 1:
            if st.button("Next ▶", use_container_width=True):
                st.session_state.public_current_page = current_page + 1
                st.rerun()
    
    with col5:
        if st.button("🎧 Audio Books", use_container_width=True):
            st.switch_page("pages/7_AudioBooks.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()