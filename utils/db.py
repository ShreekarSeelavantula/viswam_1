import json
import os
import streamlit as st
from datetime import datetime
import uuid

# Data directory paths
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
STORIES_DIR = os.path.join(DATA_DIR, "stories")

def initialize_database():
    """Initialize database directories and files"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(STORIES_DIR, exist_ok=True)
        
        # Create users.json if it doesn't exist
        if not os.path.exists(USERS_FILE):
            save_users({})
        
        return True
    except Exception as e:
        st.error(f"Failed to initialize database: {str(e)}")
        return False

def load_users():
    """Load users data from JSON file"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        st.error(f"Failed to load users: {str(e)}")
        return {}

def save_users(users_data):
    """Save users data to JSON file"""
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Failed to save users: {str(e)}")
        return False

def save_story(user_email, story_data):
    """
    Save a story for a user
    
    Args:
        user_email: Email of the user
        story_data: Dictionary containing story information
    
    Returns:
        tuple: (success: bool, story_id: str)
    """
    try:
        # Generate unique story ID
        story_id = str(uuid.uuid4())
        
        # Add metadata to story
        story_data.update({
            'story_id': story_id,
            'user_email': user_email,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        })
        
        # Save story to individual file
        story_file = os.path.join(STORIES_DIR, f"{story_id}.json")
        with open(story_file, 'w', encoding='utf-8') as f:
            json.dump(story_data, f, indent=2, ensure_ascii=False)
        
        # Update user's story list
        users = load_users()
        if user_email in users:
            if 'stories' not in users[user_email]:
                users[user_email]['stories'] = []
            users[user_email]['stories'].append(story_id)
            save_users(users)
        
        return True, story_id
    except Exception as e:
        st.error(f"Failed to save story: {str(e)}")
        return False, None

def load_story(story_id):
    """Load a specific story by ID"""
    try:
        story_file = os.path.join(STORIES_DIR, f"{story_id}.json")
        if os.path.exists(story_file):
            with open(story_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        st.error(f"Failed to load story: {str(e)}")
        return None

def get_user_stories(user_email):
    """Get all stories for a specific user"""
    try:
        users = load_users()
        if user_email not in users:
            return []
        
        story_ids = users[user_email].get('stories', [])
        stories = []
        
        for story_id in story_ids:
            story = load_story(story_id)
            if story:
                stories.append(story)
        
        return stories
    except Exception as e:
        st.error(f"Failed to get user stories: {str(e)}")
        return []

def update_story(story_id, updated_data):
    """Update an existing story"""
    try:
        story = load_story(story_id)
        if not story:
            return False
        
        # Update data
        story.update(updated_data)
        story['updated_at'] = datetime.now().isoformat()
        
        # Save updated story
        story_file = os.path.join(STORIES_DIR, f"{story_id}.json")
        with open(story_file, 'w', encoding='utf-8') as f:
            json.dump(story, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        st.error(f"Failed to update story: {str(e)}")
        return False

def delete_story(story_id, user_email):
    """Delete a story"""
    try:
        # Remove story file
        story_file = os.path.join(STORIES_DIR, f"{story_id}.json")
        if os.path.exists(story_file):
            os.remove(story_file)
        
        # Remove from user's story list
        users = load_users()
        if user_email in users and 'stories' in users[user_email]:
            if story_id in users[user_email]['stories']:
                users[user_email]['stories'].remove(story_id)
                save_users(users)
        
        return True
    except Exception as e:
        st.error(f"Failed to delete story: {str(e)}")
        return False

def get_all_stories():
    """Get ALL stories from ALL users with author information - Core Feature"""
    try:
        stories = []
        users_data = load_users()
        
        for filename in os.listdir(STORIES_DIR):
            if filename.endswith('.json'):
                story_id = filename[:-5]  # Remove .json extension
                story = load_story(story_id)
                if story:
                    # Add user information to story
                    user_email = story.get('user_email')
                    if user_email and user_email in users_data:
                        user_info = users_data[user_email]
                        story['user_name'] = user_info.get('name', 'Anonymous')
                        story['user_state'] = user_info.get('state', 'Unknown')
                        story['user_language'] = user_info.get('language', 'Unknown')
                    else:
                        story['user_name'] = 'Anonymous'
                        story['user_state'] = 'Unknown'
                        story['user_language'] = 'Unknown'
                    
                    stories.append(story)
        
        # Sort stories by creation date (newest first)
        stories.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return stories
    except Exception as e:
        st.error(f"Failed to get all stories: {str(e)}")
        return []

def search_stories(query, user_email=None):
    """Search stories by content or title"""
    try:
        if user_email:
            stories = get_user_stories(user_email)
        else:
            stories = get_all_stories()
        
        matching_stories = []
        query_lower = query.lower()
        
        for story in stories:
            # Search in title, content, festival, language
            searchable_text = f"{story.get('title', '')} {story.get('festival', '')} {story.get('language', '')}"
            
            # Search in story sections
            if 'sections' in story:
                for section in story['sections']:
                    searchable_text += f" {section.get('title', '')} {section.get('content', '')}"
            
            if query_lower in searchable_text.lower():
                matching_stories.append(story)
        
        return matching_stories
    except Exception as e:
        st.error(f"Failed to search stories: {str(e)}")
        return []

def get_database_stats():
    """Get database statistics"""
    try:
        users = load_users()
        all_stories = get_all_stories()
        
        # Language distribution
        languages = {}
        festivals = {}
        
        for story in all_stories:
            lang = story.get('language', 'Unknown')
            languages[lang] = languages.get(lang, 0) + 1
            
            fest = story.get('festival', 'Unknown')
            festivals[fest] = festivals.get(fest, 0) + 1
        
        return {
            'total_users': len(users),
            'total_stories': len(all_stories),
            'languages': languages,
            'festivals': festivals
        }
    except Exception as e:
        st.error(f"Failed to get database stats: {str(e)}")
        return {
            'total_users': 0,
            'total_stories': 0,
            'languages': {},
            'festivals': {}
        }
