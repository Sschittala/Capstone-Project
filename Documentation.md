# Text Translator and Speech Generator Documentation

# Overview
The Text Translator and Speech Generator is a web application built with Streamlit, which allows users to:
- Translate text into multiple languages using the Google Gemini API.
- Convert the translated text into speech using gTTS.
- Support input through manual text entry or file uploads (txt, pdf, csv, xlsx).
- Download the generated audio as an MP3 file.

This app features a modern, dark-themed interface and provides an intuitaive workflow for translation and speech generation. 

# Setup Instructions

# 1. Clone Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

# 2. Create and activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
# 3. Install Dependencies
```bash
pip install -r requirements.txt
```
# 4. Set Gemini API Key
This app uses Google's Gemini API. Set the API key as an environment variable
```bash
export GOOGLE_API_KEY="Your Google Gemini API Key"   # macOS/Linux
set GOOGLE_API_KEY="Your Google Gemini API Key"      # Windows
```
# 5. Run the app
```bash
streamlit run new_app.py
```
# Usage Instructions
1. Choose the input method by selecting "Enter Text" or "Upload File"
2. Input Text or Upload File:
- Enter your text in the text area.
- Or upload a supported file type.
3. Select the preferred language from the dropdown menu.
4. Click Translate:
- The app translated the text using Gemini API.
- The translated text gets displayed.
- Audio is generated automatically, and displayed for playback.
5. Download the audio if needed for offline use. 