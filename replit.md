# Overview

This is a Streamlit-based web application that converts lecture audio files into structured educational materials. The app leverages Google's Gemini AI to transcribe audio, generate summaries, extract key points, and create quizzes from lecture recordings. Users can upload various audio formats (mp3, wav, m4a, etc.) and receive comprehensive study materials in return.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit web application framework
- **Rationale**: Streamlit provides rapid development of data-focused web applications with minimal boilerplate code. It handles UI rendering, state management, and user interactions out-of-the-box, making it ideal for AI-powered tools where the focus is on functionality rather than complex UI.
- **UI Components**: 
  - File uploader for audio input (supports multiple audio formats)
  - Sidebar for API key input (secured with password masking)
  - Spinner widgets for async operation feedback
  - Result display areas for transcript, summary, key points, and quiz

## Backend Architecture
- **AI Processing**: Google Gemini AI (via google-genai SDK)
- **Architecture Pattern**: Direct API integration with client-side processing
- **Rationale**: The application uses Gemini's native audio processing capabilities rather than a multi-step pipeline, simplifying the architecture and reducing latency. Audio files are processed directly by Gemini without intermediate transcription services.
- **Data Flow**:
  1. User uploads audio file → stored in memory (Streamlit file buffer)
  2. Audio bytes + prompt sent to Gemini API
  3. Gemini processes audio and generates structured output
  4. Results displayed in Streamlit interface

## Authentication & Security
- **API Key Management**: User-provided API keys stored in session state (not persisted)
- **Security Approach**: Client-side API key input with password masking
- **Rationale**: Allows users to use their own Gemini API keys, avoiding server-side key storage and associated security concerns. Each user bears their own API costs.

## Audio Processing Pipeline
- **Supported Formats**: mp3, mp4, mpeg, mpga, m4a, wav, webm, aac
- **MIME Type Mapping**: Dynamic MIME type detection based on file extension
- **Processing Method**: Direct binary upload to Gemini API with inline content
- **Rationale**: Gemini 2.5's native audio capabilities eliminate the need for separate transcription services (like Whisper), reducing complexity and dependencies.

# External Dependencies

## AI Services
- **Google Gemini AI** (google-genai SDK)
  - Purpose: Audio transcription and content generation
  - Integration Method: REST API via official Python SDK
  - Authentication: API key-based
  - Key Features Used: Native audio file processing, multi-modal content generation

## Python Packages
- **Streamlit**: Web application framework for the user interface
- **google-genai**: Official Google Gemini AI SDK for Python

## API Requirements
- Users must provide their own Google Gemini API key
- API key obtained from Google AI Studio (https://aistudio.google.com/app/apikey)

## Potential Future Dependencies
- Database integration (if user history or saved transcripts are needed)
- File storage service (if processed results need persistence)
- User authentication system (if multi-user deployment is required)