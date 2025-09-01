import streamlit as st
import json
import os
from openai import OpenAI
from .api_manager import api_manager

# Initialize OpenAI client with managed API key
def get_openai_client():
    """Get OpenAI client with current API key"""
    current_key = api_manager.get_current_key()
    if not current_key:
        raise Exception("No API key available")
    return OpenAI(api_key=current_key["key"])

def clean_and_correct_text(text, language="Hindi", context="festival story"):
    """
    Clean and correct text using OpenAI GPT-4o
    
    Args:
        text: Raw text to be cleaned
        language: Language of the text
        context: Context for better correction (e.g., "festival story")
    
    Returns:
        tuple: (success: bool, result: dict)
    """
    try:
        system_prompt = f"""You are an expert in {language} language and Indian cultural stories. 
        Your task is to clean and correct the following {context} text while:
        1. Preserving the original meaning and cultural authenticity
        2. Correcting grammar, spelling, and sentence structure
        3. Maintaining the storytelling tone and emotional essence
        4. Adding appropriate punctuation and formatting
        5. Ensuring cultural sensitivity and accuracy
        
        Please respond with JSON in this exact format:
        {{
            "cleaned_text": "the corrected and cleaned text",
            "improvements_made": ["list of improvements made"],
            "confidence_score": 0.95,
            "cultural_notes": "any important cultural context preserved"
        }}"""
        
        user_prompt = f"Please clean and correct this {language} {context} text:\n\n{text}"
        
        # Show API usage status before making request
        api_manager.show_usage_status()
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        if content:
            result = json.loads(content)
            return True, result
        else:
            return False, {"error": "No content in response"}
    
    except Exception as e:
        return False, {"error": f"Text cleaning failed: {str(e)}"}

def organize_story_sections(text, num_sections=3, language="Hindi"):
    """
    Organize story into sections/pages for virtual book
    
    Args:
        text: Cleaned story text
        num_sections: Number of sections to create
        language: Language of the story
    
    Returns:
        tuple: (success: bool, result: dict)
    """
    try:
        system_prompt = f"""You are an expert storyteller and editor. 
        Your task is to organize the following {language} story into {num_sections} meaningful sections/pages for a virtual book.
        
        Each section should:
        1. Have a natural flow and narrative arc
        2. End at a good stopping point
        3. Be roughly equal in length
        4. Have a descriptive title
        5. Include a brief description for image generation
        
        Please respond with JSON in this exact format:
        {{
            "sections": [
                {{
                    "title": "Section title",
                    "content": "Section content text",
                    "image_description": "Description for generating relevant image",
                    "page_number": 1
                }}
            ],
            "story_title": "Overall story title",
            "story_summary": "Brief summary of the complete story"
        }}"""
        
        user_prompt = f"Please organize this {language} story into {num_sections} sections:\n\n{text}"
        
        # Show API usage status
        api_manager.show_usage_status()
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=3000
        )
        
        content = response.choices[0].message.content
        if content:
            result = json.loads(content)
            # Record successful API usage
            api_manager.record_usage(success=True)
            return True, result
        else:
            return False, {"error": "No content in response"}
    
    except Exception as e:
        error_msg = str(e)
        # Record failed API usage
        api_manager.record_usage(success=False)
        
        # Handle rate limit errors
        if "429" in error_msg:
            if api_manager.handle_rate_limit_error():
                return False, {"error": "Rate limit reached. Switched to backup API key. Please try again."}
            return False, {"error": "Rate limit reached. Please wait before trying again."}
        
        return False, {"error": f"Story organization failed: {error_msg}"}

def generate_image_description(story_content, cultural_context="Indian festival"):
    """
    Generate detailed image description for story illustration
    
    Args:
        story_content: Content of the story section
        cultural_context: Cultural context for accurate representation
    
    Returns:
        tuple: (success: bool, description: str)
    """
    try:
        system_prompt = f"""You are an expert in Indian art and cultural visualization. 
        Create a detailed, culturally accurate image description for illustrating this {cultural_context} story.
        
        The description should:
        1. Be culturally authentic and respectful
        2. Include appropriate traditional elements
        3. Specify colors, clothing, settings typical of Indian festivals
        4. Avoid stereotypes while maintaining cultural accuracy
        5. Be suitable for family-friendly content
        
        Keep the description under 200 words and focus on visual elements that would make a beautiful illustration."""
        
        user_prompt = f"Create an image description for this story content:\n\n{story_content}"
        
        # Show API usage status
        api_manager.show_usage_status()
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500
        )
        
        # Record successful API usage
        api_manager.record_usage(success=True)
        return True, response.choices[0].message.content
    
    except Exception as e:
        error_msg = str(e)
        # Record failed API usage
        api_manager.record_usage(success=False)
        
        # Handle rate limit errors
        if "429" in error_msg:
            if api_manager.handle_rate_limit_error():
                return False, "Rate limit reached. Switched to backup API key. Please try again."
            return False, "Rate limit reached. Please wait before trying again."
        
        return False, f"Image description generation failed: {error_msg}"

def display_text_cleaning_ui(input_text, language="Hindi"):
    """
    Display UI for text cleaning and correction
    
    Args:
        input_text: Text to be cleaned
        language: Language of the text
    
    Returns:
        dict: Cleaned text result or None
    """
    if not input_text or not input_text.strip():
        st.warning("Please provide text to clean and correct.")
        return None
    
    st.subheader("🤖 AI Text Enhancement")
    
    # Show original text
    with st.expander("📝 Original Text", expanded=False):
        st.text_area("Original:", value=input_text, height=150, disabled=True)
    
    # Language and context selection
    col1, col2 = st.columns(2)
    with col1:
        selected_language = st.selectbox(
            "Language:",
            ["Hindi", "English", "Bengali", "Telugu", "Marathi", "Tamil", "Gujarati", "Urdu", "Kannada", "Malayalam"],
            index=0 if language == "Hindi" else (["Hindi", "English", "Bengali", "Telugu", "Marathi", "Tamil", "Gujarati", "Urdu", "Kannada", "Malayalam"].index(language) if language in ["Hindi", "English", "Bengali", "Telugu", "Marathi", "Tamil", "Gujarati", "Urdu", "Kannada", "Malayalam"] else 0)
        )
    
    with col2:
        story_context = st.selectbox(
            "Story Type:",
            ["festival story", "cultural story", "traditional tale", "family story", "religious story"],
            index=0
        )
    
    # Clean text button
    if st.button("✨ Clean & Enhance Text", type="primary"):
        with st.spinner("Enhancing your story with AI... Please wait."):
            success, result = clean_and_correct_text(input_text, selected_language, story_context)
            
            if success and "cleaned_text" in result:
                st.success("✅ Text enhancement completed!")
                
                # Display cleaned text
                cleaned_text = st.text_area(
                    "Enhanced Text:",
                    value=result["cleaned_text"],
                    height=200,
                    key="cleaned_text_output",
                    help="You can further edit this enhanced text if needed"
                )
                
                # Show improvements made
                if "improvements_made" in result and result["improvements_made"]:
                    with st.expander("🔧 Improvements Made", expanded=False):
                        for improvement in result["improvements_made"]:
                            st.write(f"• {improvement}")
                
                # Show confidence score
                if "confidence_score" in result:
                    st.metric("AI Confidence", f"{result['confidence_score'] * 100:.1f}%")
                
                # Show cultural notes
                if "cultural_notes" in result and result["cultural_notes"]:
                    with st.expander("🏛️ Cultural Notes", expanded=False):
                        st.write(result["cultural_notes"])
                
                return result
            else:
                error_msg = result.get("error", "Unknown error occurred") if isinstance(result, dict) else str(result)
                st.error(f"❌ {error_msg}")
                return None
    
    return None
