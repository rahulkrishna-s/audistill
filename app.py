import streamlit as st
from groq import Groq

st.title("Audistill")

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.warning("GROQ_API_KEY not found in secrets. Please set it up to proceed.")
    st.stop()

client = Groq(api_key=api_key)

audio_file = st.file_uploader("Upload Audio (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    st.audio(audio_file)

    if st.button("Transcribe Audio"):
        with st.spinner("Transcribing with Groq Whisper..."):
            try:
                transcription = client.audio.transcriptions.create(
                    file=(audio_file.name, audio_file),
                    model="whisper-large-v3", 
                    response_format="json"
                )
                
                st.success("Transcription Successful!")
                st.markdown("### Raw Transcript")
                st.text_area("Transcript", transcription.text, height=300)
                
            except Exception as e:
                st.error(f"Error: {e}")