# Audistill - AI Lecture Assistant

> **Work in Progress:** This project is currently in active development. The core transcription and summarization pipelines are functional. Next update will include the Quiz Generation module.

## Overview
Audistill is a GenAI powered study aid designed to help students convert raw lecture audio into structured study materials. By leveraging the **Groq Cloud API**, it offers near real time transcription and intelligent summarization.

## Features
* **Audio Transcription:** Upload audio files (MP3, WAV, M4A) and get high accuracy transcripts using the `whisper-large-v3` model.
* **Smart Summarization:** Automatically converts transcripts into concise bullet point study notes using `llama-3.1-8b-instant`.
* **Interactive UI:** Built with Streamlit for a responsive and easy to use experience.

## Roadmap & Development Status
I am actively building out the full feature set. Here is the current progress:

- [x] **Core Pipeline:** Audio upload & processing logic.
- [x] **Transcription Engine:** Integration with Groq Whisper API.
- [x] **Summarizer:** Llama 3.1 integration for note generation.
- [ ] **Quiz Mode:** Generating JSON structured quizzes from lecture content *(Currently implementing locally)*.
- [ ] **Export Options:** Download notes as PDF/Markdown.

## Tech Stack
* **Language:** Python
* **Frontend:** Streamlit
* **AI/Models:** Groq Cloud API (Whisper-large-v3, Llama-3.1-8b)

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
