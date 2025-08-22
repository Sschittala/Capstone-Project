import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from gtts import gTTS
import io
import os
import tempfile
import google.generativeai as genai
st.set_page_config(page_title="Text Translator & Speech Generator", layout="centered")
st.title("🌍 Text Translator & Speech Generator")

st.markdown("Translate text into different languages and generate speech using **Gemini API + gTTS**.")