import streamlit as st
import tempfile
import os
from openai import OpenAI

def transcribe_audio_file(audio_file):
    """
    Transcribe audio file using OpenAI Whisper
    
    Args:
        audio_file: Streamlit uploaded file object
    
    Returns:
        str: Transcribed text
    """
    try:
        # Check if API key is available
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise Exception("OpenAI API key not configured. Please add your API key to continue.")
        
        client = OpenAI(api_key=api_key)
        
        # Save uploaded file to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(audio_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            # Transcribe audio using OpenAI Whisper
            with open(tmp_file_path, "rb") as audio:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio,
                    language="hi"  # Hindi, can be made dynamic based on user preference
                )
            
            return transcript.text
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
                
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")

def display_transcription_ui():
    """Display UI for audio transcription - kept for backward compatibility"""
    st.info("🎤 Use the voice input option in the upload flow for audio transcription.")