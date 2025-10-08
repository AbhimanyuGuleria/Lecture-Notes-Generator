import streamlit as st
import openai
import os

# --- 1. CONCEPT & UI SETUP ---
# The app is designed to be simple. A title, a file uploader, and a place to show the results.
# We use Streamlit's functions like st.title() and st.file_uploader() to create these elements.

st.title("🎙️ Lecture Voice-to-Notes Generator")
st.write("Upload a lecture audio file, and get a transcript, summary, key points, and a quiz!")

# We get the API key from the user via a sidebar input.
# For deployment, it's better to use Streamlit Secrets.
with st.sidebar:
    openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    st.markdown("Get your API key from [OpenAI](https://platform.openai.com/account/api-keys).")

# The user uploads an audio file. We specify the types of audio files we accept.
uploaded_file = st.file_uploader(
    "Upload your audio file (e.g., .mp3, .wav, .m4a)",
    type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]
)

# --- 2. PSEUDO CODE EXPLANATION (and Implementation) ---

# IF the user has provided an API key AND has uploaded a file:
if openai_api_key and uploaded_file is not None:
    st.success("API Key and file uploaded successfully!")
    openai.api_key = openai_api_key

    # STEP 1: Transcribe the audio file using OpenAI's Whisper model.
    # We show a spinner to let the user know something is happening.
    with st.spinner("Transcribing audio... this might take a moment ⏳"):
        try:
            # We call the OpenAI API to create a transcription.
            # 'file=uploaded_file' sends the audio data.
            # 'model="whisper-1"' specifies the AI model to use.
            transcript_response = openai.audio.transcriptions.create(
                file=uploaded_file,
                model="whisper-1"
            )
            # The actual text is stored in the 'text' attribute of the response.
            transcript_text = transcript_response.text
        except Exception as e:
            st.error(f"Error during transcription: {e}")
            transcript_text = ""

    # IF the transcription was successful (we got some text back):
    if transcript_text:
        st.header("📜 Full Transcript")
        # We display the transcript in an expandable box to save space.
        with st.expander("Click to view transcript"):
            st.write(transcript_text)

        # STEP 2: Use a generative AI model (GPT) to generate notes from the transcript.
        # We show another spinner for this process.
        with st.spinner("Generating summary, key points, and quiz... 🧠"):
            try:
                # This is the prompt we send to the AI. It tells the AI exactly what to do.
                # We give it a role ("You are an expert note-taking assistant.") and a task.
                system_prompt = "You are an expert note-taking assistant. Your goal is to convert the provided lecture transcript into clear, concise, and useful study materials."
                user_prompt = f"""
                Based on the following lecture transcript, please generate the following:
                1. A short summary (2-3 sentences).
                2. A list of key points or takeaways (using bullet points).
                3. A short, 3-question multiple-choice quiz to test understanding. Provide the correct answer for each question.

                Transcript:
                ---
                {transcript_text}
                """

                # We call the OpenAI chat completion API.
                # 'model="gpt-3.5-turbo"' specifies the generative model.
                # 'messages' contains the instructions and the transcript.
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                # The AI's response is in 'response.choices[0].message.content'.
                generated_notes = response.choices[0].message.content

                st.header("📝 Generated Study Notes")
                st.write(generated_notes)

            except Exception as e:
                st.error(f"Error during note generation: {e}")

# IF the user has NOT provided an API key or uploaded a file:
else:
    st.warning("Please enter your OpenAI API key and upload an audio file to begin.")

