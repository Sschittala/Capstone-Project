import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from gtts import gTTS
import io
import os
import tempfile
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

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
    prompt = f"Translate the following text into {target_language}:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

def text_to_speech(text, lang_code="en"):
    tts = gTTS(text=text, lang=lang_code)
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save(fp.name + ".mp3")
        with open(fp.name + ".mp3", "rb") as f:
            return f.read()
st.set_page_config(page_title="Text Translator & Speech Generator", layout="centered")
st.title("🌍 Text Translator & Speech Generator")

st.markdown("Translate text into different languages and generate speech using **Gemini API + gTTS**.")