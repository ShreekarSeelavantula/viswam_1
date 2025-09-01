import streamlit as st
from utils.auth import check_authentication, get_current_user
from utils.db import save_story
import base64
from PIL import Image
import io
import uuid
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Upload Story - Utsav Kathalu AI",
    page_icon="📝",
    layout="wide"
)

def main():
    # Custom CSS
    st.markdown("""
    <style>
    .upload-header {
        text-align: center;
        color: #D4AF37;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .section-container {
        background: linear-gradient(135deg, #FFF8DC 0%, #F0E68C 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #FF6B35;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .step-header {
        color: #8B4513;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .section-box {
        background: #FFFEF7;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #D4AF37;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please login to upload stories")
        if st.button("🔑 Go to Login"):
            st.switch_page("pages/2_Auth.py")
        return
    
    st.markdown('<h1 class="upload-header">📝 Share Your Festival Story</h1>', unsafe_allow_html=True)
    
    user_data = get_current_user()
    st.markdown(f"**Storyteller:** {user_data.get('name', 'Friend')} | **Language:** {user_data.get('preferred_language', 'Hindi')}")
    
    # Initialize session state
    if 'upload_step' not in st.session_state:
        st.session_state.upload_step = 1
    
    # Main upload flow
    if st.session_state.upload_step == 1:
        show_story_setup()
    elif st.session_state.upload_step == 2:
        show_input_method_selection()
    elif st.session_state.upload_step == 3:
        show_multi_section_input()
    elif st.session_state.upload_step == 4:
        show_image_upload_for_sections()
    elif st.session_state.upload_step == 5:
        show_final_review_and_save()

def show_story_setup():
    """Step 1: Story details and number of sections"""
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-header">📝 Step 1: Story Setup</div>', unsafe_allow_html=True)
    
    with st.form("story_setup"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("🏷️ Story Title", placeholder="Give your story a beautiful title")
            festival = st.selectbox("🎊 Festival", [
                "Diwali", "Holi", "Dussehra", "Navratri", "Karva Chauth", "Raksha Bandhan",
                "Eid", "Christmas", "Ganesh Chaturthi", "Krishna Janmashtami", "Durga Puja",
                "Onam", "Pongal", "Baisakhi", "Makar Sankranti", "Other"
            ])
            language = st.selectbox("🗣️ Language", [
                "Hindi", "English", "Bengali", "Tamil", "Telugu", "Marathi", 
                "Gujarati", "Kannada", "Malayalam", "Punjabi", "Urdu", "Other"
            ])
        
        with col2:
            story_type = st.selectbox("📚 Story Type", [
                "Personal Experience", "Family Tradition", "Childhood Memory",
                "Cultural Practice", "Religious Story", "Community Celebration"
            ])
            
            num_sections = st.selectbox("📖 Number of Story Sections", 
                options=[2, 3, 4, 5, 6], 
                help="How many parts/chapters does your story have?"
            )
            
        description = st.text_area("📄 Story Description", 
            placeholder="Brief description of your festival story",
            height=100
        )
        
        if st.form_submit_button("Next: Choose Input Method ➡️", type="primary"):
            if title and festival and description:
                # Store story details in session
                st.session_state.story_data = {
                    'title': title,
                    'festival': festival,
                    'language': language,
                    'story_type': story_type,
                    'description': description,
                    'num_sections': num_sections,
                    'sections': [],
                    'images': {}
                }
                st.session_state.upload_step = 2
                st.rerun()
            else:
                st.error("Please fill in all required fields (Title, Festival, Description)")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_input_method_selection():
    """Step 2: Choose input method"""
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-header">🎤 Step 2: Choose Input Method</div>', unsafe_allow_html=True)
    
    story_data = st.session_state.story_data
    
    st.info("Choose how you want to input your story content. You can use text or voice input for each section.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📝 Text Input
        - Type your story directly
        - Easy editing and formatting
        - Perfect for detailed stories
        """)
        if st.button("📝 Use Text Input", type="primary", use_container_width=True):
            st.session_state.story_data['input_method'] = 'text'
            st.session_state.upload_step = 3
            st.rerun()
    
    with col2:
        st.markdown("""
        ### 🎤 Voice Input
        - Record your story by speaking
        - Natural storytelling experience
        - Includes voice playback in virtual book
        """)
        if st.button("🎤 Use Voice Input", type="primary", use_container_width=True):
            st.session_state.story_data['input_method'] = 'voice'
            st.session_state.upload_step = 3
            st.rerun()
    
    # Back button
    if st.button("⬅️ Back to Story Setup"):
        st.session_state.upload_step = 1
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_multi_section_input():
    """Step 3: Input content for all sections"""
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-header">📖 Step 3: Create Your Story Sections</div>', unsafe_allow_html=True)
    
    story_data = st.session_state.story_data
    num_sections = story_data['num_sections']
    input_method = story_data.get('input_method', 'text')
    
    if input_method == 'text':
        st.info(f"Please write your {num_sections} story sections below. Each section should be a complete part of your festival story.")
    else:
        st.info(f"Please record your {num_sections} story sections below. Speak naturally and we'll transcribe it for you.")
    
    if input_method == 'text':
        show_text_input_sections()
    else:
        show_voice_input_sections()

def show_text_input_sections():
    """Handle text input for sections"""
    story_data = st.session_state.story_data
    num_sections = story_data['num_sections']
    
    with st.form("story_sections"):
        sections = []
        
        for i in range(num_sections):
            st.markdown(f'<div class="section-box">', unsafe_allow_html=True)
            st.markdown(f"### 📝 Section {i+1}")
            
            section_title = st.text_input(
                f"Section {i+1} Title", 
                placeholder=f"Title for section {i+1}",
                key=f"section_title_{i}"
            )
            
            section_content = st.text_area(
                f"Section {i+1} Content",
                placeholder=f"Write the content for section {i+1} of your story...",
                height=150,
                key=f"section_content_{i}"
            )
            
            image_description = st.text_input(
                f"Image Description for Section {i+1}",
                placeholder="Describe what kind of image would go well with this section",
                key=f"image_desc_{i}"
            )
            
            sections.append({
                'title': section_title,
                'content': section_content,
                'image_description': image_description
            })
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # AI Enhancement Option
        use_ai_enhancement = st.checkbox(
            "🤖 Use AI Enhancement (Optional)", 
            help="AI will improve grammar, cultural context, and story flow. This uses API credits."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("⬅️ Back to Input Method"):
                st.session_state.upload_step = 2
                st.rerun()
        
        with col2:
            if st.form_submit_button("Next: Upload Images ➡️", type="primary"):
                # Validate sections
                valid_sections = []
                for i, section in enumerate(sections):
                    if section['title'] and section['content']:
                        valid_sections.append(section)
                    else:
                        st.error(f"Please fill in title and content for Section {i+1}")
                        return
                
                if len(valid_sections) == num_sections:
                    # Apply AI enhancement if requested
                    if use_ai_enhancement:
                        enhanced_sections = apply_ai_enhancement(valid_sections)
                        st.session_state.story_data['sections'] = enhanced_sections
                        st.session_state.story_data['ai_enhanced'] = True
                    else:
                        st.session_state.story_data['sections'] = valid_sections
                        st.session_state.story_data['ai_enhanced'] = False
                    
                    st.session_state.upload_step = 4
                    st.rerun()

def show_voice_input_sections():
    """Handle voice input for sections"""
    story_data = st.session_state.story_data
    num_sections = story_data['num_sections']
    
    st.info("🎤 Voice Recording Mode: Record each section by speaking into your microphone.")
    
    sections = []
    for i in range(num_sections):
        st.markdown(f'<div class="section-box">', unsafe_allow_html=True)
        st.markdown(f"### 🎤 Section {i+1}")
        
        section_title = st.text_input(
            f"Section {i+1} Title", 
            placeholder=f"Title for section {i+1}",
            key=f"voice_section_title_{i}"
        )
        
        # Voice recording interface
        st.info("📢 **Supported Audio Formats:** WAV, MP3, M4A only. OPUS/OGG files are not supported.")
        audio_file = st.file_uploader(
            f"Upload Audio for Section {i+1}",
            type=['wav', 'mp3', 'm4a'],
            key=f"voice_section_{i}",
            help="Upload your audio story section (WAV, MP3, or M4A format only)"
        )
        
        # Gender selection for audio book narrator
        narrator_gender = st.selectbox(
            f"Narrator Voice for Section {i+1}",
            options=["Male", "Female"],
            key=f"narrator_gender_{i}",
            help="Choose the gender of the animated narrator for this section"
        )
        
        if audio_file:
            st.success(f"✅ Audio uploaded for Section {i+1}!")
            st.audio(audio_file, format=f"audio/{audio_file.type.split('/')[-1]}")
        
        section_content = st.text_area(
            f"Story Text for Section {i+1}",
            placeholder=f"Write the story text that matches your audio for section {i+1}...",
            height=150,
            key=f"section_content_voice_{i}",
            help="This text will be displayed alongside the audio in the audio book"
        )
        
        image_description = st.text_input(
            f"Image Description for Section {i+1}",
            placeholder="Describe what kind of image would go well with this section",
            key=f"voice_image_desc_{i}"
        )
        
        audio_data = None
        if audio_file:
            audio_data = base64.b64encode(audio_file.getvalue()).decode()
        
        sections.append({
            'title': section_title,
            'content': section_content,
            'image_description': image_description,
            'audio_data': audio_data,
            'narrator_gender': narrator_gender
        })
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Enhancement Option
    use_ai_enhancement = st.checkbox(
        "🤖 Use AI Enhancement (Optional)", 
        help="AI will improve grammar, cultural context, and story flow. This uses API credits."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Input Method"):
            st.session_state.upload_step = 2
            st.rerun()
    
    with col2:
        if st.button("Next: Upload Images ➡️", type="primary"):
            # Validate sections
            valid_sections = []
            for i, section in enumerate(sections):
                if section['title'] and (section['content'] or section['audio_data']):
                    valid_sections.append(section)
                else:
                    st.error(f"Please provide title and either audio or text content for Section {i+1}")
                    return
            
            if len(valid_sections) == num_sections:
                # Apply AI enhancement if requested
                if use_ai_enhancement:
                    enhanced_sections = apply_ai_enhancement(valid_sections)
                    st.session_state.story_data['sections'] = enhanced_sections
                    st.session_state.story_data['ai_enhanced'] = True
                else:
                    st.session_state.story_data['sections'] = valid_sections
                    st.session_state.story_data['ai_enhanced'] = False
                
                st.session_state.upload_step = 4
                st.rerun()

def apply_ai_enhancement(sections):
    """Apply AI enhancement to story sections"""
    enhanced_sections = []
    
    try:
        from utils.text_cleaner import clean_and_correct_text
        
        for section in sections:
            with st.spinner(f"Enhancing: {section['title']}..."):
                enhanced_content = clean_and_correct_text(
                    section['content'],
                    f"This is a section titled '{section['title']}' from a festival story."
                )
                
                enhanced_sections.append({
                    'title': section['title'],
                    'content': enhanced_content.get('cleaned_text', section['content']) if isinstance(enhanced_content, dict) else section['content'],
                    'image_description': section['image_description'],
                    'audio_data': section.get('audio_data'),
                    'narrator_gender': section.get('narrator_gender'),
                    'ai_improvements': enhanced_content.get('improvements_made', []) if isinstance(enhanced_content, dict) else []
                })
        
        st.success("✅ AI enhancement completed!")
        return enhanced_sections
        
    except Exception as e:
        st.error(f"AI enhancement failed: {str(e)}. Using original content.")
        return sections
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("⬅️ Back to Input Method"):
                st.session_state.upload_step = 2
                st.rerun()
        
        with col2:
            if st.form_submit_button("Next: Upload Images ➡️", type="primary"):
                # Validate sections
                valid_sections = []
                for i, section in enumerate(sections):
                    if section['title'] and section['content']:
                        valid_sections.append(section)
                    else:
                        st.error(f"Please fill in title and content for Section {i+1}")
                        return
                
                if len(valid_sections) == num_sections:
                    st.session_state.story_data['sections'] = valid_sections
                    st.session_state.upload_step = 3
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_image_upload_for_sections():
    """Step 4: Upload images for each section"""
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-header">🖼️ Step 4: Upload Images for Each Section</div>', unsafe_allow_html=True)
    
    story_data = st.session_state.story_data
    sections = story_data['sections']
    
    st.info("Upload at least 2 images for each section. Images help bring your story to life!")
    
    images = {}
    
    for i, section in enumerate(sections):
        st.markdown(f'<div class="section-box">', unsafe_allow_html=True)
        st.markdown(f"### 📸 Images for Section {i+1}: {section['title']}")
        st.write(f"**Image suggestion:** {section['image_description']}")
        
        # Upload multiple images for this section
        uploaded_files = st.file_uploader(
            f"Choose images for Section {i+1}",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            key=f"images_section_{i}"
        )
        
        if uploaded_files:
            if len(uploaded_files) >= 2:
                st.success(f"✅ {len(uploaded_files)} images uploaded for Section {i+1}")
                # Store first 2 images (or first one if only one uploaded)
                for j, uploaded_file in enumerate(uploaded_files[:2]):
                    image = Image.open(uploaded_file)
                    # Resize image if too large
                    if image.size[0] > 800 or image.size[1] > 600:
                        image.thumbnail((800, 600), Image.Resampling.LANCZOS)
                    
                    buffer = io.BytesIO()
                    image.save(buffer, format="JPEG", quality=85)
                    image_base64 = base64.b64encode(buffer.getvalue()).decode()
                    
                    images[f"section_{i+1}_image_{j+1}"] = image_base64
                    st.image(image, caption=f"Section {i+1} - Image {j+1}", width=200)
            else:
                st.warning(f"Please upload at least 2 images for Section {i+1}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Story Sections"):
            st.session_state.upload_step = 3
            st.rerun()
    
    with col2:
        if st.button("Next: Review & Save ➡️", type="primary"):
            # Check if all sections have at least 1 image
            missing_images = []
            for i in range(len(sections)):
                section_images = [key for key in images.keys() if key.startswith(f"section_{i+1}_")]
                if not section_images:
                    missing_images.append(i+1)
            
            if missing_images:
                st.error(f"Please upload at least one image for sections: {', '.join(map(str, missing_images))}")
            else:
                st.session_state.story_data['images'] = images
                st.session_state.upload_step = 5
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_final_review_and_save():
    """Step 5: Review and save the story"""
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-header">👀 Step 5: Review & Save Your Story</div>', unsafe_allow_html=True)
    
    story_data = st.session_state.story_data
    
    # Show story summary
    st.markdown("### 📖 Story Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Title:** {story_data['title']}")
        st.write(f"**Festival:** {story_data['festival']}")
        st.write(f"**Language:** {story_data['language']}")
    with col2:
        st.write(f"**Type:** {story_data['story_type']}")
        st.write(f"**Sections:** {len(story_data['sections'])}")
        st.write(f"**Images:** {len(story_data['images'])}")
    
    st.write(f"**Description:** {story_data['description']}")
    
    # Show sections preview
    st.markdown("### 📝 Sections Preview")
    for i, section in enumerate(story_data['sections']):
        with st.expander(f"Section {i+1}: {section['title']}"):
            st.write(section['content'])
            st.write(f"**Image Description:** {section['image_description']}")
    
    # Navigation and save
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Images"):
            st.session_state.upload_step = 4
            st.rerun()
    
    with col2:
        if st.button("💾 Save Story", type="primary"):
            # Save the story
            user_data = get_current_user()
            story_id = str(uuid.uuid4())
            
            # Prepare story data for saving
            final_story = {
                'story_id': story_id,
                'user_email': user_data.get('email'),
                'user_name': user_data.get('name'),
                'title': story_data['title'],
                'festival': story_data['festival'],
                'language': story_data['language'],
                'story_type': story_data['story_type'],
                'description': story_data['description'],
                'sections': story_data['sections'],
                'images': story_data['images'],
                'input_method': story_data.get('input_method', 'text'),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Save to database
            success, story_id = save_story(user_data.get('email'), final_story)
            
            if success:
                st.success("🎉 Story saved successfully!")
                st.balloons()
                
                # Clear session data
                for key in ['story_data', 'upload_step']:
                    if key in st.session_state:
                        del st.session_state[key]
                
                # Navigation options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📖 View My Story", type="primary"):
                        st.session_state.selected_story_id = story_id
                        st.switch_page("pages/4_VirtualBook.py")
                
                with col2:
                    if st.button("📝 Upload Another Story"):
                        st.rerun()
            else:
                st.error(f"❌ Error saving story: {story_id}")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()