import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from gtts import gTTS
import io
import os
import tempfile
import google.generativeai as genai
import re

genai.configure(api_key=os.getenv("Google_Api_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")
# for model in genai.list_models():
#     print(f"Name: {model.name}, Supports: {model.supported_generation_methods}")
def extract_text_from_file(uploaded_file):
    text = ""
    if uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    elif uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        text = df.to_string()
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
        text = df.to_string()
    
    return text.strip()

def translate_text(text, target_language):
    if not text.strip():
        return "No text provided for translation."
    prompt = f"Translate the following text into {target_language}:\n\n{text}"
    response = model.generate_content(prompt)
    if not response.candidates:
        return "No response generated"
    candidate = response.candidates[0]
    if not candidate.content.parts:
        return "No content returned"
    translated = "".join(part.text for part in candidate.content.parts if hasattr(part, "text"))
    translated = re.sub(r"[*_'#>-]", "", translated)
    translated = re.sub(r"\s+", " ", translated)
    return translated.strip()

def text_to_speech(text, lang_code="en"):
    tts = gTTS(text=text, lang=lang_code)
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(fp.name + ".mp3")
        with open(fp.name + ".mp3", "rb") as f:
            return f.read()

st.set_page_config(page_title="Text Translator & Speech Generator", layout="centered")
dark_css = """
<style>
/* Main background */
[data-testid="stAppViewContainer"]{
    background: linear-gradient(135deg, #0b0b0b, #141414);
    color: #e0e0e0;
    font-family:'Segoe UI', sans-serif;
}
/* Sidebar */
[data-testid="stSidebar"]{
    background: #111111;
    color: #e0e0e0;
}
/* Titles */
h1, h2, h3, h4 {
    color: #66ffe7;
    text-shadow: 0 0 10px #008b8b, 0 0 20px #005f5f;
}
/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#004f4f, #006666);
    color: #f0f0f0;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
    padding: 0.6em 2em;
    border: none;
    box-shadow: 0 0 15px #00cccc, 0 0 30px #009999;
    transition: all 0.3s ease-in-out;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #006666, #009999);
    color: #ffffff;
    box-shadow: 0 0 20px #00cccc, 0 0 40px #009999;
    transform: scale(1.05);
}
/* Inputs */
.stTextArea textarea {
    background: #1c1c1c !important;
    color: #e0e0e0 !important;
    border-radius: 8px;
    border: 1px solid #004f4f;
    box-shadow: inset 0 0 10px #006666;
    
}

/* Audio Player */
.stAudio {
    background: #101010;
    border: 1px solid #222222;
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0 0 10px #444444;
}
/* Download Button */
.stDownloadButton>button {
    background: linear-gradient(90deg, #3a003a, #520052;
    color: #f0f0f0;
    border-radius: 12px;
    font-size: 16px;
    padding: 0.6em 2em;
    box-shadow: 0 0 15px #800080, 00 30px #550055;
    transition: all 0.3s ease-in-out;
}
.stDownloadButton>button:hover {
    background: linear-gradient(90deg, #520052, #800080);
    box-shadow: 0 0 20px #aa00aa, 0 0 40px #770077;
    transform: scale(1.05);
}
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)
st.title("🌍 Text Translator & Speech Generator")

st.markdown("Translate text into different languages and generate speech using **Gemini API + gTTS**.")
option = st.radio("Choose input method:", ["Enter text", "Upload File"])
input_text = ""
if option == "Enter text":
    input_text = st.text_area("Enter your text here:")
elif option == "Upload File":
    uploaded_file = st.file_uploader("Upload a file (txt, pdf, csv, xlsx)", type=["txt", "pdf", "csv", "xlsx"])
    if uploaded_file is not None:
        input_text = extract_text_from_file(uploaded_file)

t_language = st.selectbox("Select Preferred Language:",
                          ["French", "Spanish", "German", "Hindi", "Chinese", "Arabic", "English"])

l_codes = {
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Hindi": "hi",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "English": "en"
}

if st.button("Translate"):
    if input_text.strip() == "":
        st.error("Please enter or upload some text.")
    else:
        with st.spinner("Translating..."):
            translated_text = translate_text(input_text, t_language)
        st.subheader("Translated Text:")
        st.write(translated_text)
        with st.spinner("Converting to speech..."):
            audio_bytes = text_to_speech(translated_text, l_codes[t_language])
        st.audio(audio_bytes, format="audio/mp3")
        
        st.download_button(
            label="Download Audio",
            data = audio_bytes, 
            file_name="translated_audio.mp3",
            mime="audio/mp3"
        )
