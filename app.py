import streamlit as st
from groq import Groq
import json

st.title("Audistill")

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.warning("GROQ_API_KEY not found in secrets. Please set it up to proceed.")
    st.stop()

client = Groq(api_key=api_key)

# Session states
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

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
                st.session_state.summary = completion.choices[0].message.content
            except Exception as e:
                st.error(f"Error generating summary: {e}")

# Display summary if available
if st.session_state.summary:
    st.markdown("### Study Notes")
    st.markdown(st.session_state.summary)

    # Quiz Generation
    if st.button("Generate Quiz"):
        with st.spinner("Generating Quiz Questions..."):
            try:
                quiz_prompt = """
                Based on the summary, generate 3 multiple-choice questions.
                Return strictly valid JSON with this exact structure:
                {"questions": [{"question": "Your question?", "options": ["Option A text", "Option B text", "Option C text", "Option D text"], "answer": "Option A text"}]}
                
                IMPORTANT: The "answer" field must contain the FULL TEXT of the correct option, not just a letter.
                """
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a teacher. Output strictly JSON. The answer field must be the complete text of the correct option."},
                        {"role": "user", "content": f"Summary: {st.session_state.summary}\n\n{quiz_prompt}"}
                    ],
                    response_format={"type": "json_object"}
                )
                st.session_state.quiz_data = json.loads(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Error generating quiz: {e}")

# Quiz Display
if st.session_state.quiz_data:
    st.markdown("### Knowledge Check")
    
    data = st.session_state.quiz_data
    questions = data.get("questions", []) if isinstance(data, dict) else data if isinstance(data, list) else []
    
    if not questions:
        st.error("Invalid quiz format. Please try generating again.")
    else:
        with st.form("quiz_form"):
            user_answers = {}
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i+1}: {q['question']}**")
                user_answers[i] = st.radio(
                    label=f"Select answer for Q{i+1}",
                    options=q['options'],
                    key=f"q_{i}",
                    label_visibility="collapsed"
                )
            
            submitted = st.form_submit_button("Check All Answers")
            
            if submitted:
                score = 0
                for i, q in enumerate(questions):
                    correct_answer = q['answer']
                    
                    # Handle case where answer is a letter instead of full text
                    if correct_answer in ['A', 'B', 'C', 'D']:
                        correct_index = ord(correct_answer) - ord('A')
                        correct_answer = q['options'][correct_index]
                    
                    if user_answers[i] == correct_answer:
                        st.success(f"Q{i+1}: Correct! ✓")
                        score += 1
                    else:
                        st.error(f"Q{i+1}: Incorrect. The answer was: {correct_answer}")
                
                st.markdown(f"### Score: {score}/{len(questions)}")