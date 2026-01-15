import streamlit as st
from groq import Groq

st.title("Audistill")

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.warning("GROQ_API_KEY not found in secrets. Please set it up to proceed.")
    st.stop()

client = Groq(api_key=api_key)

if "transcript" not in st.session_state:
    st.session_state.transcript = None

audio_file = st.file_uploader("Upload Audio (MP3, WAV, M4A)", type=["mp3", "wav", "m4a", "ogg"])

if audio_file is not None:
    st.audio(audio_file)

    # Transcription
    if st.button("Transcribe Audio"):
        with st.spinner("Transcribing with Groq Whisper..."):
            try:
                transcription = client.audio.transcriptions.create(
                    file=(audio_file.name, audio_file),
                    model="whisper-large-v3", 
                    response_format="json"
                )

                st.session_state.transcript = transcription.text
                st.success("Transcription Successful!")
                
            except Exception as e:
                st.error(f"Error: {e}")

if st.session_state.transcript:
    st.markdown("### Raw Transcript")
    st.text_area("Transcript", st.session_state.transcript, height=300)

    # Summary Generation
    if st.button("Generate Summary & Notes"):
        with st.spinner("Generating study notes..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant", 
                    messages=[
                        {"role": "system", "content": "You are an expert student assistant. Summarize the following lecture into key study points."},
                        {"role": "user", "content": st.session_state.transcript}
                    ]
                )
                summary = completion.choices[0].message.content
                st.markdown("### Study Notes")
                st.write(summary)
            except Exception as e:
                st.error(f"Error generating summary: {e}")