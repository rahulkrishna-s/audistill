# Audistill - AI Lecture Assistant

>Transform lecture recordings into comprehensive study materials with AI-powered transcription, summarization, quizzes, and flashcards.

## Overview
Audistill is a GenAI powered study aid designed to help students convert raw lecture audio into structured study materials. By leveraging the **Groq Cloud API**, it offers near real time transcription and intelligent summarization.


## Features
* **Audio Transcription:** Upload audio files (MP3, WAV, M4A, OGG) and get high accuracy transcripts using the `whisper-large-v3` model.
* **Smart Summarization:** Automatically converts transcripts into concise bullet point study notes using `llama-3.1-8b-instant`.
* **Interactive Quizzes:** Generate multiple-choice questions from lecture content with instant feedback and scoring.
* **Flashcard Generator:** Create study flashcards with flip-able cards for active recall practice.
* **Interactive UI:** Built with Streamlit for a responsive and easy to use experience.

## Tech Stack
* **Language:** Python
* **Frontend:** Streamlit
* **AI/Models:** Groq Cloud API
  - Whisper-large-v3 (Transcription)
  - Llama-3.1-8b-instant (Summarization)
  - Llama-3.3-70b-versatile (Quiz & Flashcard Generation)

## How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/rahulkrishna-s/audistill.git
   cd audistill
2. Install dependencies
   ```bash
   pip install streamlit groq
3. Set up API Keys Create a .streamlit/secrets.toml file in the root directory and add your Groq API key:
   ```bash
   GROQ_API_KEY = "your_api_key_here"
4. Run the App
   ```bash
   streamlit run app.py

##
Developed as part of the ASAP Kerala AI Internship Capstone.
