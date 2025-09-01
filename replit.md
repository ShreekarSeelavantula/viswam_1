# Utsav Kathalu AI - Multilingual Festival Story Collector

## Overview

Utsav Kathalu AI is a Streamlit-based web application designed to collect, curate, and display culturally rich festival stories from across India. The platform supports multilingual input through voice and text, uses AI for content enhancement, and presents stories in an interactive virtual book format. This open-source project aims to preserve Indian cultural heritage while building a clean Indic language corpus for research purposes.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular Streamlit architecture with a multi-page design pattern. The system is built around user authentication, story collection, AI-powered content processing, and an interactive story viewing experience.

### Frontend Architecture
- **Framework**: Streamlit with custom CSS styling
- **Design Pattern**: Multi-page application using Streamlit's native page routing
- **Theme**: Indian cultural design with warm colors (gold, brown, orange gradients)
- **Pages**: Home, Authentication, Upload, and Virtual Book viewer
- **UI Components**: Custom styled containers, forms, and interactive elements

### Backend Architecture
- **Language**: Python
- **Web Framework**: Streamlit
- **File Structure**: Modular utilities in separate files
- **Session Management**: Streamlit's built-in session state
- **Data Processing**: Synchronous processing with OpenAI API integration

## Key Components

### Authentication System (`utils/auth.py`)
- **Purpose**: User registration, login, and session management
- **Features**: Email validation, password hashing (SHA-256), user data persistence
- **Data**: Supports Indian states and languages selection during registration
- **Security**: Basic password requirements (minimum 6 characters)

### Database Layer (`utils/db.py`)
- **Type**: File-based JSON storage
- **Structure**: Flat file system with separate directories for users and stories
- **Files**: `users.json` for user data, individual JSON files for stories
- **Operations**: CRUD operations for users and stories with error handling

### Speech Processing (`utils/speech_to_text.py`)
- **Service**: OpenAI Whisper API integration
- **Functionality**: Audio file transcription with language support
- **File Handling**: Temporary file management for audio processing
- **Output**: Text transcription with error handling

### Text Enhancement (`utils/text_cleaner.py`)
- **Service**: OpenAI GPT-4o integration
- **Purpose**: Grammar correction, cultural sensitivity, and text improvement
- **Features**: Context-aware processing for festival stories
- **Output**: Structured JSON response with improvements and cultural notes

### Story Management
- **Upload**: Multi-section story creation with image support
- **Organization**: Section-based story structure with metadata
- **Storage**: JSON format with base64 encoded images
- **Retrieval**: User-specific story listing and loading

## Data Flow

1. **User Registration/Login**: User creates account → Data stored in `users.json` → Session initialized
2. **Story Upload**: User selects input method → Audio transcribed or text processed → AI cleaning applied → Story sections organized → Saved to individual JSON files
3. **Story Viewing**: User accesses virtual book → Stories loaded from JSON files → Interactive book interface displayed
4. **AI Processing**: Raw content → OpenAI API → Enhanced content → Structured output

## External Dependencies

### AI Services
- **OpenAI API**: Primary dependency for Whisper (speech-to-text) and GPT-4o (text enhancement)
- **API Key Management**: Environment variable based configuration
- **Models**: whisper-1 for transcription, gpt-4o for text processing

### Python Libraries
- **Streamlit**: Web application framework and UI components
- **OpenAI**: Official API client for AI services
- **PIL (Pillow)**: Image processing and manipulation
- **Standard Libraries**: json, os, hashlib, datetime, uuid, tempfile, base64

### File System Dependencies
- **Local Storage**: JSON files for data persistence
- **Directory Structure**: Organized data and stories folders
- **File Formats**: JSON for structured data, base64 for image encoding

## Deployment Strategy

### Target Platforms
- **Primary**: Replit (development and hosting)
- **Secondary**: Hugging Face Spaces (alternative deployment)
- **Compatibility**: Designed for cloud-based Python environments

### Configuration Requirements
- **Environment Variables**: OpenAI API key configuration
- **File Permissions**: Read/write access to data directories
- **Dependencies**: Requirements for Streamlit, OpenAI, and image processing libraries

### Scalability Considerations
- **Current Limitation**: File-based storage suitable for small to medium user bases
- **Future Enhancement**: Ready for database migration (Postgres compatible)
- **Performance**: Synchronous processing may require optimization for high traffic

### Security Considerations
- **Authentication**: Basic email/password system with hashed storage
- **API Keys**: Environment variable protection
- **Data Storage**: Local file system with JSON encoding
- **Input Validation**: Basic email and password validation implemented

## Recent Changes

### Analytics Dashboard (2025-01-28)
- Added comprehensive analytics page (`pages/5_Analytics.py`) showing:
  - Platform overview metrics (users, stories, languages, festivals)
  - Language and festival distribution charts
  - Detailed user information with story counts
  - Recent activity feed
- Enhanced main dashboard with admin management features
- Added sample data initialization system

### Sample Data System (2025-01-28)
- Created `utils/sample_data.py` with pre-populated festival stories
- Added 4 sample users from different Indian states
- Created 4 detailed festival stories (Diwali, Durga Puja, Navratri, Ganesh Chaturthi)
- Stories include authentic cultural details, multiple sections, and AI enhancement data
- One-click sample data population for demonstration

### User Analytics Enhancement (2025-01-28)
- Enhanced database statistics tracking
- Added user registration date tracking
- Improved story metadata collection
- User activity monitoring and reporting

### Replit Migration (2025-07-28)
- Successfully migrated project from Replit Agent to standard Replit environment
- Installed all required dependencies (streamlit, openai, pandas, pillow)
- Created proper Streamlit configuration file (.streamlit/config.toml) for deployment
- Fixed function naming conflict in VirtualBook page (renamed show_virtual_book to show_story_reader)
- Enhanced security with proper client/server separation and environment variable protection
- Application runs cleanly on port 5000

### Upload System Redesign (2025-07-28)
- Completely redesigned upload process to eliminate unnecessary API calls
- Created streamlined 5-step workflow: Story Setup → Input Method Selection → Content Creation → Image Upload → Review & Save
- Added voice input functionality with OpenAI Whisper transcription
- Made AI enhancement completely optional to minimize API costs
- Implemented dynamic section creation based on user selection (2-6 sections)
- Added proper image upload system requiring 2+ images per section
- Fixed virtual book display issues with proper image key matching
- Fixed function naming conflict in VirtualBook page (renamed show_virtual_book to show_story_reader)
- Enhanced security with proper client/server separation and environment variable protection
- Application now runs cleanly on port 5000 with no LSP errors

### Virtual Book Enhancement (2025-07-28)
- **Core Feature Update**: Virtual Book Library now displays ALL stories from ALL users (not just user's own stories)
- Implemented realistic book page-turning animation instead of PowerPoint-style transitions
- Added enhanced image layout with top-left and bottom-right positioning in virtual books
- Created voice playback functionality for stories created with voice input
- Added comprehensive filtering by festival, language, state, and author
- Enhanced story cards with author information and creation dates
- Updated database functions to include user information in all stories
- Improved navigation with animated page controls and progress tracking

### Access Control Update (2025-07-28)
- **Authentication Required**: All story exploration features now require user authentication
- Created dedicated "Explore Stories" page accessible only to logged-in users
- Updated main dashboard to include story exploration as primary feature for authenticated users
- Fixed HTML content display issues - stories now show clean text instead of markup
- Removed public access to virtual books - users must login to explore festival stories
- Enhanced user flow: Welcome → Login → Dashboard with Explore/Upload/My Stories options