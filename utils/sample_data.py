import json
import uuid
from datetime import datetime
from .db import save_story, save_users, load_users

def create_sample_users():
    """Create sample users for demo purposes"""
    sample_users = {
        "priya.sharma@email.com": {
            "name": "Priya Sharma",
            "email": "priya.sharma@email.com",
            "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # "password"
            "preferred_language": "Hindi",
            "state": "Rajasthan",
            "created_at": "2024-01-15T10:30:00",
            "stories": []
        },
        "rajesh.kumar@email.com": {
            "name": "Rajesh Kumar",
            "email": "rajesh.kumar@email.com",
            "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # "password"
            "preferred_language": "Bengali",
            "state": "West Bengal",
            "created_at": "2024-01-20T14:15:00",
            "stories": []
        },
        "anita.patel@email.com": {
            "name": "Anita Patel",
            "email": "anita.patel@email.com",
            "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # "password"
            "preferred_language": "Gujarati",
            "state": "Gujarat",
            "created_at": "2024-02-01T09:45:00",
            "stories": []
        },
        "meera.reddy@email.com": {
            "name": "Meera Reddy",
            "email": "meera.reddy@email.com",
            "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # "password"
            "preferred_language": "Telugu",
            "state": "Andhra Pradesh",
            "created_at": "2024-02-05T16:20:00",
            "stories": []
        }
    }
    
    existing_users = load_users()
    existing_users.update(sample_users)
    save_users(existing_users)
    
    return sample_users

def create_sample_stories():
    """Create sample festival stories"""
    sample_stories = [
        {
            "title": "Diwali ki Roshni - The Light of Hope",
            "festival": "Diwali",
            "language": "Hindi",
            "story_type": "Family Tradition",
            "num_sections": 3,
            "description": "A heartwarming story about how Diwali brought light to our family during difficult times.",
            "user_email": "priya.sharma@email.com",
            "user_name": "Priya Sharma",
            "input_method": "text",
            "enhanced_story_text": "This is the story of how Diwali's light guided our family through the darkest of times...",
            "sections": [
                {
                    "title": "The Dark Before the Light",
                    "content": "It was 2019, and our family had faced many challenges. My father had lost his job, and we were struggling financially. As Diwali approached, we wondered if we could celebrate at all. The house felt darker than usual, and hope seemed distant.",
                    "image_description": "A dimly lit traditional Indian home with worried family members sitting together, shadows cast by a single oil lamp",
                    "page_number": 1
                },
                {
                    "title": "Community's Embrace",
                    "content": "On the morning of Diwali, our neighbors began arriving with sweets, rangoli colors, and warm smiles. Mrs. Gupta brought homemade ladoos, while the Agarwal family gifted us beautiful diyas. The entire community came together, reminding us that festivals are about togetherness, not just expenses.",
                    "image_description": "Neighbors of different ages gathering in a courtyard, sharing sweets and colorful rangoli patterns, children playing with sparklers",
                    "page_number": 2
                },
                {
                    "title": "The Light Returns",
                    "content": "As evening fell, our home was transformed. Hundreds of diyas flickered in the darkness, and our hearts were full once again. That Diwali taught us that the real light of the festival comes from love, community, and hope. Today, whenever someone in our neighborhood faces difficulties, we remember that Diwali lesson and reach out with open hearts.",
                    "image_description": "A beautifully illuminated Indian home with rows of oil lamps, family members in traditional attire celebrating together, fireworks in the distant sky",
                    "page_number": 3
                }
            ],
            "images": {},
            "ai_enhancements": {
                "improvements_made": ["Enhanced emotional depth", "Improved narrative flow", "Added cultural context"],
                "confidence_score": 0.95,
                "cultural_notes": "Story beautifully captures the community spirit of Diwali celebrations"
            }
        },
        {
            "title": "Durga Puja: Mayer Ashirbad",
            "festival": "Durga Puja",
            "language": "Bengali",
            "story_type": "Community Celebration",
            "num_sections": 4,
            "description": "The magical five days of Durga Puja in our Kolkata neighborhood, where tradition meets modernity.",
            "user_email": "rajesh.kumar@email.com",
            "user_name": "Rajesh Kumar",
            "input_method": "text",
            "enhanced_story_text": "Every year, as the autumn breeze carries the scent of shiuli flowers...",
            "sections": [
                {
                    "title": "Shashthi: The Awakening",
                    "content": "The dhak beats echo through the narrow lanes of our para as Maa Durga arrives. The pandal, crafted by local artisans over months, reveals itself in all its glory. Children in new clothes run around excitedly while elders perform the ritual awakening of the goddess. The air is thick with incense and anticipation.",
                    "image_description": "A magnificent Bengali Durga pandal with intricate decorations, crowds of devotees in traditional attire, dhakis playing drums",
                    "page_number": 1
                },
                {
                    "title": "Saptami to Ashtami: Divine Celebrations",
                    "content": "The next two days blur into a beautiful chaos of prayers, cultural programs, and endless adda. The para comes alive with young artists performing classical dances, poets reciting verses, and musicians filling the night with soulful melodies. Food stalls offer everything from puchka to traditional sweets.",
                    "image_description": "Cultural programs on a decorated stage, young dancers in colorful costumes, families enjoying street food under festive lights",
                    "page_number": 2
                },
                {
                    "title": "Navami: The Grand Celebration",
                    "content": "On Navami, the celebration reaches its peak. The entire community participates in the evening aarti, thousands of voices joining in harmony. The sindoor khela brings women together in joyful abandon, their white sarees transformed with vermillion, symbolizing the goddess's blessings.",
                    "image_description": "Women in white sarees playing with sindoor, covering each other with vermillion, laughing and celebrating together",
                    "page_number": 3
                },
                {
                    "title": "Dashami: The Tearful Farewell",
                    "content": "As Dashami arrives, tears mix with celebration. Maa Durga's immersion in the Ganges is both an ending and a promise of return. The entire para accompanies her to the river, dancing and chanting 'Dugga Mai ki Jay!' The goddess leaves, but her blessings and the memories of these five magical days remain in our hearts until next year.",
                    "image_description": "A procession carrying Durga idol towards the river, devotees dancing and chanting, Ganga ghat with floating flowers and lamps",
                    "page_number": 4
                }
            ],
            "images": {},
            "ai_enhancements": {
                "improvements_made": ["Enhanced Bengali cultural references", "Improved chronological structure", "Added sensory details"],
                "confidence_score": 0.92,
                "cultural_notes": "Authentic portrayal of Bengali Durga Puja traditions and community involvement"
            }
        },
        {
            "title": "Navratri: Nine Nights of Divine Dance",
            "festival": "Navratri",
            "language": "Gujarati",
            "story_type": "Personal Experience",
            "num_sections": 3,
            "description": "My first Navratri in Gujarat, where I discovered the true meaning of devotion through dance.",
            "user_email": "anita.patel@email.com",
            "user_name": "Anita Patel",
            "input_method": "text",
            "enhanced_story_text": "I was a newcomer to Gujarat, and Navratri was my first introduction to the state's soul...",
            "sections": [
                {
                    "title": "The Rhythmic Welcome",
                    "content": "As a newcomer to Ahmedabad, I was nervous about participating in Navratri. But when I heard the dhol-tasha and saw hundreds of people moving in perfect harmony to the garba steps, my feet began to move on their own. An elderly aunty grabbed my hand, smiled, and whispered, 'Aaje to aapo ne raas ramva na din che!' (Today is the day to play and celebrate!)",
                    "image_description": "A vibrant Navratri celebration with people in colorful traditional Gujarati attire dancing garba in concentric circles",
                    "page_number": 1
                },
                {
                    "title": "Learning the Sacred Steps",
                    "content": "Each night, I learned new steps and met new friends. The garba taught me patience, the dandiya taught me coordination, and the community taught me belonging. Young children would giggle as they corrected my steps, while elders shared stories of Navratris from their youth. By the fifth night, I was no longer a spectator but a participant in this divine dance.",
                    "image_description": "People of all ages teaching and learning garba steps, children laughing, colorful dandiya sticks creating patterns in the air",
                    "page_number": 2
                },
                {
                    "title": "Nine Nights, One Soul",
                    "content": "On the final night, as I danced the aarti, I understood why Navratri is called a celebration of the divine feminine. It wasn't just about the steps or the music; it was about the collective energy, the shared devotion, and the community that embraces everyone as family. Those nine nights transformed me from an outsider to a daughter of Gujarat.",
                    "image_description": "The grand finale of Navratri with elaborate decorations, hundreds of dancers in perfect formation, Garba queen being crowned",
                    "page_number": 3
                }
            ],
            "images": {},
            "ai_enhancements": {
                "improvements_made": ["Added authentic Gujarati phrases", "Enhanced cultural immersion narrative", "Improved emotional progression"],
                "confidence_score": 0.94,
                "cultural_notes": "Beautiful representation of Gujarati hospitality and Navratri's inclusive spirit"
            }
        },
        {
            "title": "Ganesh Chaturthi: Bappa's Homecoming",
            "festival": "Ganesh Chaturthi",
            "language": "Telugu",
            "story_type": "Childhood Memory",
            "num_sections": 3,
            "description": "Childhood memories of Ganesh Chaturthi in our Hyderabad colony, where Bappa brought the community together.",
            "user_email": "meera.reddy@email.com",
            "user_name": "Meera Reddy",
            "input_method": "text",
            "enhanced_story_text": "Every year in our Hyderabad colony, Ganesh Chaturthi was the most awaited festival...",
            "sections": [
                {
                    "title": "Bappa's Grand Arrival",
                    "content": "The whole colony would wait for weeks as uncles and aunties planned the grandest welcome for Ganesha. The pandal would be decorated with fresh marigolds and jasmine, and the most beautiful Ganesha idol would be installed with great pomp. As children, we would compete to be the first to seek Bappa's blessings and receive the coveted modak prasadam.",
                    "image_description": "A beautifully decorated Ganesha pandal with a magnificent idol, children and adults offering prayers, fresh flower garlands",
                    "page_number": 1
                },
                {
                    "title": "Ten Days of Joy",
                    "content": "For ten magical days, our colony transformed into a cultural hub. Every evening brought new performances - classical dances, devotional songs, and skits about Ganesha's stories. The ladies would organize cooking competitions, making different varieties of modaks and undrallu. We children would participate in rangoli competitions and quiz contests about Lord Ganesha.",
                    "image_description": "Community cultural programs with children performing dances, women displaying various traditional sweets, colorful rangoli patterns",
                    "page_number": 2
                },
                {
                    "title": "The Tearful Farewell",
                    "content": "On Anant Chaturdashi, the entire colony would accompany Bappa to the Hussain Sagar lake for visarjan. The procession would be filled with drums, dancing, and chants of 'Ganpati Bappa Morya!' As we watched our beloved Ganesha disappear into the waters, we would cry and promise to bring him back next year with even more love and devotion.",
                    "image_description": "A grand procession towards a lake, people carrying Ganesha idol, devotees dancing and celebrating, lake with floating flowers",
                    "page_number": 3
                }
            ],
            "images": {},
            "ai_enhancements": {
                "improvements_made": ["Enhanced childhood perspective", "Added Telugu cultural elements", "Improved emotional storytelling"],
                "confidence_score": 0.93,
                "cultural_notes": "Captures the essence of community Ganesh celebrations in Telugu regions"
            }
        }
    ]
    
    # Save each story
    for story_data in sample_stories:
        user_email = story_data["user_email"]
        success, story_id = save_story(user_email, story_data)
        if success:
            print(f"Sample story '{story_data['title']}' created with ID: {story_id}")
    
    return sample_stories

def initialize_sample_data():
    """Initialize the platform with sample users and stories"""
    try:
        # Create sample users
        users = create_sample_users()
        print(f"Created {len(users)} sample users")
        
        # Create sample stories
        stories = create_sample_stories()
        print(f"Created {len(stories)} sample stories")
        
        return True, f"Successfully created {len(users)} users and {len(stories)} stories"
    
    except Exception as e:
        return False, f"Failed to create sample data: {str(e)}"

# Sample festival data for quick story creation
FESTIVAL_TEMPLATES = {
    "Diwali": {
        "description": "Festival of lights celebrating the victory of good over evil",
        "typical_elements": ["diyas", "rangoli", "fireworks", "sweets", "family gatherings"],
        "emotions": ["joy", "hope", "togetherness", "prosperity"],
        "traditions": ["lighting lamps", "exchanging gifts", "sharing sweets", "family prayers"]
    },
    "Holi": {
        "description": "Festival of colors celebrating spring and love",
        "typical_elements": ["colors", "water balloons", "music", "dance", "bhang"],
        "emotions": ["joy", "playfulness", "love", "unity"],
        "traditions": ["playing with colors", "community celebrations", "special foods", "folk songs"]
    },
    "Eid": {
        "description": "Festival of breaking the fast, celebrating compassion and community",
        "typical_elements": ["moon sighting", "special prayers", "new clothes", "feasts"],
        "emotions": ["gratitude", "compassion", "community", "joy"],
        "traditions": ["morning prayers", "charity", "family feasts", "gift giving"]
    },
    "Christmas": {
        "description": "Celebration of love, giving, and family togetherness",
        "typical_elements": ["Christmas tree", "carols", "gifts", "family dinner"],
        "emotions": ["love", "generosity", "peace", "family bonding"],
        "traditions": ["midnight mass", "gift exchange", "carol singing", "special meals"]
    },
    "Onam": {
        "description": "Harvest festival of Kerala celebrating King Mahabali's return",
        "typical_elements": ["pookalam", "sadhya", "boat races", "traditional dances"],
        "emotions": ["prosperity", "cultural pride", "community harmony"],
        "traditions": ["flower carpets", "traditional feast", "cultural programs", "boat races"]
    }
}