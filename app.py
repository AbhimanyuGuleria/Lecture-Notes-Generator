import streamlit as st
import os
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
    type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm", "aac"]
)

# --- 2. PSEUDO CODE EXPLANATION (and Implementation) ---

# IF the user has provided an API key AND has uploaded a file:
if gemini_api_key and uploaded_file is not None:
    st.success("API Key and file uploaded successfully!")
    
    # Initialize Gemini client
    # IMPORTANT: Using google-genai SDK as per python_gemini integration
    gemini_client = genai.Client(api_key=gemini_api_key)
    
    # STEP 1: Transcribe the audio file using Gemini's audio capabilities.
    # Gemini 2.5 can directly process audio files for transcription!
    # We show a spinner to let the user know something is happening.
    with st.spinner("Transcribing audio... this might take a moment ⏳"):
        try:
            # Read the audio file content
            audio_bytes = uploaded_file.read()
            
            # Determine MIME type based on file extension
            file_extension = uploaded_file.name.split('.')[-1].lower()
            mime_type_map = {
                'mp3': 'audio/mp3',
                'mpeg': 'audio/mpeg',
                'mpga': 'audio/mpeg',
                'mp4': 'audio/mp4',
                'm4a': 'audio/mp4',
                'wav': 'audio/wav',
                'webm': 'audio/webm',
                'aac': 'audio/aac'
            }
            mime_type = mime_type_map.get(file_extension, 'audio/mpeg')
            
            # Use Gemini to transcribe the audio
            # IMPORTANT: Using gemini-2.5-flash as per the integration guidelines
            transcription_response = gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    "Please transcribe this audio file accurately. Provide the complete transcript with proper punctuation.",
                    types.Part.from_bytes(
                        data=audio_bytes,
                        mime_type=mime_type
                    )
                ]
            )
            
            transcript_text = transcription_response.text.strip()
            
        except Exception as e:
            st.error(f"Error during transcription: {e}")
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
