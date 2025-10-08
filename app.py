import streamlit as st
import os
from google.cloud import speech
from google import genai
from google.genai import types

# --- 1. CONCEPT & UI SETUP ---
# The app is designed to be simple. A title, a file uploader, and a place to show the results.
# We use Streamlit's functions like st.title() and st.file_uploader() to create these elements.

st.title("🎙️ Lecture Voice-to-Notes Generator")
st.write("Upload a lecture audio file, and get a transcript, summary, key points, and a quiz!")

# We get the API key from the user via a sidebar input.
with st.sidebar:
    gemini_api_key = st.text_input("Enter your Gemini API Key:", type="password")
    st.markdown("Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).")

# The user uploads an audio file. We specify the types of audio files we accept.
uploaded_file = st.file_uploader(
    "Upload your audio file (e.g., .mp3, .wav, .m4a)",
    type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]
)

# --- 2. PSEUDO CODE EXPLANATION (and Implementation) ---

# IF the user has provided an API key AND has uploaded a file:
if gemini_api_key and uploaded_file is not None:
    st.success("API Key and file uploaded successfully!")
    
    # Initialize Gemini client
    # IMPORTANT: Using google-genai SDK as per python_gemini integration
    gemini_client = genai.Client(api_key=gemini_api_key)
    
    # STEP 1: Transcribe the audio file using Google Speech-to-Text.
    # We show a spinner to let the user know something is happening.
    with st.spinner("Transcribing audio... this might take a moment ⏳"):
        try:
            # Google Speech-to-Text can handle audio directly from Streamlit's uploaded file
            # We read the audio file content
            audio_content = uploaded_file.read()
            
            # Initialize Speech-to-Text client
            speech_client = speech.SpeechClient()
            
            # Configure the audio
            audio = speech.RecognitionAudio(content=audio_content)
            
            # Configure recognition settings
            # Using automatic encoding detection and common settings
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
                language_code="en-US",
                enable_automatic_punctuation=True,
                audio_channel_count=1,
            )
            
            # Call the Speech-to-Text API
            response = speech_client.recognize(config=config, audio=audio)
            
            # Extract the transcript text from the response
            transcript_text = ""
            for result in response.results:
                transcript_text += result.alternatives[0].transcript + " "
            
            transcript_text = transcript_text.strip()
            
        except Exception as e:
            st.error(f"Error during transcription: {e}")
            st.info("Note: Google Speech-to-Text requires proper audio format. Try using WAV, FLAC, or properly encoded MP3 files.")
            transcript_text = ""

    # IF the transcription was successful (we got some text back):
    if transcript_text:
        st.header("📜 Full Transcript")
        # We display the transcript in an expandable box to save space.
        with st.expander("Click to view transcript"):
            st.write(transcript_text)

        # STEP 2: Use Gemini to generate notes from the transcript.
        # We show another spinner for this process.
        with st.spinner("Generating summary, key points, and quiz... 🧠"):
            try:
                # This is the prompt we send to the AI. It tells the AI exactly what to do.
                prompt = f"""You are an expert note-taking assistant. Your goal is to convert the provided lecture transcript into clear, concise, and useful study materials.

Based on the following lecture transcript, please generate the following:
1. A short summary (2-3 sentences).
2. A list of key points or takeaways (using bullet points).
3. A short, 3-question multiple-choice quiz to test understanding. Provide the correct answer for each question.

Transcript:
---
{transcript_text}
"""

                # Call the Gemini API for content generation
                # IMPORTANT: Using gemini-2.5-flash as per the integration guidelines
                response = gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                
                # The AI's response is in response.text
                generated_notes = response.text

                st.header("📝 Generated Study Notes")
                st.write(generated_notes)

            except Exception as e:
                st.error(f"Error during note generation: {e}")

# IF the user has NOT provided an API key or uploaded a file:
else:
    st.warning("Please enter your Gemini API key and upload an audio file to begin.")
