import streamlit as st
import os
from google import genai
from google.genai import types

# Set page configuration
st.set_page_config(
    page_title="Lecture Voice-to-Notes Generator",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .upload-section {
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. CONCEPT & UI SETUP ---
st.markdown('<div class="main-header"><h1>🎙️ Lecture Voice-to-Notes Generator</h1></div>', unsafe_allow_html=True)
st.write("Transform your lecture audio files into comprehensive study materials with AI-powered transcription and note generation!")

# Sidebar for API key and settings
with st.sidebar:
    st.header("⚙️ Configuration")
    gemini_api_key = st.text_input("Enter your Gemini API Key:", type="password", help="Get your API key from Google AI Studio")
    st.markdown("📚 [Get API key from Google AI Studio](https://aistudio.google.com/app/apikey)")

    # Additional settings
    st.subheader("📝 Generation Settings")
    include_timestamps = st.checkbox("Include timestamps (if available)", value=False)
    quiz_difficulty = st.selectbox("Quiz difficulty level", ["Easy", "Medium", "Hard"], index=1)
    num_questions = st.slider("Number of quiz questions", 3, 10, 5)

# File upload section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.subheader("📁 Upload Audio File")
uploaded_file = st.file_uploader
