import io
import os
import re
import string
import tempfile
import urllib.parse

from deep_translator import GoogleTranslator
import numpy as np
import pandas as pd
import soundfile as sf
import speech_recognition as sr
import streamlit as st
import streamlit.components.v1 as components
import whisper

from sign_to_speech import render_sign_to_speech_page

try:
    from moviepy import VideoFileClip  # type: ignore
    MOVIEPY_AVAILABLE = True
except Exception:
    MOVIEPY_AVAILABLE = False

WHISPER_SR = 16000  # sample rate Whisper expects

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(__file__), "sign_database.csv")
FINGERSPELL_BASE = 0x1F1E6  # 🇦 regional indicator symbol letter A

LANGUAGE_MAP = {
    "Auto Detect": None,
    "English": "en",
    "Hindi": "hi",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
}

INDIC_LANGUAGE_TAGS = {
    "hi": "hi-IN",
    "gu": "gu-IN",
    "kn": "kn-IN",
    "ta": "ta-IN",
    "te": "te-IN",
}

CODE_TO_LANGUAGE = {
    "en": "English",
    "hi": "Hindi",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ta": "Tamil",
    "te": "Telugu",
}

SUPPORTED_LANGUAGES = {
    "auto": "Auto Detect",
    "en": "English",
    "hi": "Hindi",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ta": "Tamil",
    "te": "Telugu",
}


st.set_page_config(page_title="SIGNBRIDGE AI - AI Communication For Everyone", page_icon="🤟", layout="wide")

# --------------------------------------------------------------------------
# SIGNBRIDGE — GestureFlow Interface System
# Futuristic Sign Language Communication Studio Design Language
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700;800&display=swap');

        :root {
            --bg-canvas: #F7FAFF;
            --bg-card: #FFFFFF;
            --bg-card-subtle: #F8FAFD;
            --bg-soft-blue: #EAF3FF;
            --bg-soft-purple: #F3EEFF;
            --bg-soft-mint: #ECFDF5;
            --primary-blue: #2878F0;
            --primary-blue-hover: #1D63D8;
            --lavender: #8B5CF6;
            --lavender-soft: #A78BFA;
            --mint: #0D9488;
            --emerald-badge: #059669;
            --border-light: #DCE7F5;
            --border-subtle: #E2EAF4;
            --border-active: #BFDBFE;
            --text-heading: #14213D;
            --text-body: #1E293B;
            --text-secondary: #64748B;
            --text-muted: #94A3B8;
            --font-main: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-heading: 'Poppins', 'Plus Jakarta Sans', sans-serif;
            --card-shadow: 0 10px 30px rgba(40, 120, 240, 0.06), 0 2px 8px rgba(0, 0, 0, 0.03);
            --card-shadow-hover: 0 14px 38px rgba(40, 120, 240, 0.10), 0 4px 12px rgba(0, 0, 0, 0.04);
        }

        /* ---------------------------------------------------------------------- */
        /* Light Theme Canvas & Background Waves                                  */
        /* ---------------------------------------------------------------------- */
        .stApp {
            background-color: var(--bg-canvas) !important;
            background-image:
                radial-gradient(circle at 10% 12%, rgba(234, 243, 255, 0.85) 0%, transparent 45%),
                radial-gradient(circle at 90% 18%, rgba(243, 238, 255, 0.75) 0%, transparent 48%),
                radial-gradient(circle at 50% 88%, rgba(230, 248, 245, 0.65) 0%, transparent 55%),
                url("data:image/svg+xml,%3Csvg width='140' height='140' viewBox='0 0 140 140' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 70 Q35 45 70 70 T140 70' fill='none' stroke='rgba(40,120,240,0.035)' stroke-width='1.2'/%3E%3Cpath d='M0 35 Q70 10 140 35' fill='none' stroke='rgba(139,92,246,0.025)' stroke-width='1' stroke-dasharray='4,8'/%3E%3Ccircle cx='70' cy='70' r='1.5' fill='rgba(40,120,240,0.08)'/%3E%3C/svg%3E") !important;
            background-attachment: fixed !important;
            color: var(--text-body);
            font-family: var(--font-main);
            overflow-x: hidden !important;
        }

        /* ---------------------------------------------------------------------- */
        /* Left Sidebar — Clean Light Design Rail                                 */
        /* ---------------------------------------------------------------------- */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid var(--border-light) !important;
            box-shadow: 4px 0 24px rgba(40, 120, 240, 0.04) !important;
        }

        [data-testid="stSidebar"] hr {
            border-color: var(--border-light) !important;
            margin: 18px 0 !important;
        }

        /* Sidebar Navigation Capsules */
        [data-testid="stSidebar"] [data-testid="stRadio"] > div {
            gap: 10px !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] label {
            background: #F8FAFD !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 14px !important;
            padding: 13px 16px !important;
            color: var(--text-secondary) !important;
            font-weight: 600 !important;
            font-size: 0.90rem !important;
            letter-spacing: 0.01em !important;
            transition: all 0.22s ease !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
            position: relative !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
            border-color: #BFDBFE !important;
            color: var(--primary-blue) !important;
            background: #F0F6FF !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(40, 120, 240, 0.08) !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] {
            background: linear-gradient(135deg, #EAF3FF 0%, #F3EEFF 100%) !important;
            border: 1px solid #C8DEFC !important;
            border-left: 4px solid var(--primary-blue) !important;
            color: var(--primary-blue) !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 14px rgba(40, 120, 240, 0.12) !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"]::after {
            content: "" !important;
            position: absolute !important;
            right: 14px !important;
            width: 8px !important;
            height: 8px !important;
            border-radius: 50% !important;
            background: var(--primary-blue) !important;
            box-shadow: 0 0 10px rgba(40, 120, 240, 0.5) !important;
            animation: radarPulseLight 2s infinite ease-in-out !important;
        }

        @keyframes radarPulseLight {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.35); opacity: 0.6; }
        }

        /* ---------------------------------------------------------------------- */
        /* Brand Technology Identity Panel (Light)                                */
        /* ---------------------------------------------------------------------- */
        .identity-panel {
            padding: 10px 4px 16px 4px;
            border-bottom: 1px solid var(--border-light);
            margin-bottom: 16px;
        }

        .identity-card {
            display: flex;
            align-items: center;
            gap: 12px;
            background: linear-gradient(135deg, #FFFFFF 0%, #F5F9FF 100%);
            border: 1px solid var(--border-light);
            border-radius: 16px;
            padding: 12px 14px;
            box-shadow: 0 4px 16px rgba(40, 120, 240, 0.05);
        }

        .identity-icon-box {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: linear-gradient(135deg, #2878F0 0%, #8B5CF6 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.45rem;
            box-shadow: 0 4px 14px rgba(40, 120, 240, 0.25);
            flex-shrink: 0;
            color: #FFFFFF;
        }

        .identity-title {
            font-family: var(--font-heading);
            font-weight: 800;
            font-size: 1.12rem;
            color: var(--text-heading);
            letter-spacing: -0.01em;
            line-height: 1.15;
        }

        .identity-subtitle {
            font-size: 0.74rem;
            color: var(--text-secondary);
            font-weight: 500;
            margin-top: 2px;
        }

        /* ---------------------------------------------------------------------- */
        /* Center Communication Flow Bridge (Light)                               */
        /* ---------------------------------------------------------------------- */
        .comm-flow-bridge {
            margin: 0 0 22px 0;
            padding: 14px 22px;
            background: #FFFFFF;
            border: 1px solid var(--border-light);
            border-radius: 20px;
            box-shadow: var(--card-shadow);
            position: relative;
        }

        .flow-track {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
        }

        .flow-node {
            display: flex;
            align-items: center;
            gap: 8px;
            background: #F8FAFD;
            border: 1px solid var(--border-light);
            border-radius: 999px;
            padding: 6px 16px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            color: var(--text-heading);
        }

        .flow-node.voice-node {
            background: #EAF3FF;
            border-color: #BFDBFE;
            color: #1E40AF;
        }

        .flow-node.ai-node {
            background: #F3EEFF;
            border-color: #DDD6FE;
            color: #6D28D9;
        }

        .flow-node.sign-node {
            background: #ECFDF5;
            border-color: #A7F3D0;
            color: #047857;
        }

        .flow-node-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            display: inline-block;
        }

        .flow-connector-line {
            flex: 1;
            min-width: 40px;
            height: 2px;
            background: linear-gradient(90deg, #93C5FD 0%, #C4B5FD 50%, #6EE7B7 100%);
            position: relative;
        }

        .flow-connector-line::after {
            content: "";
            position: absolute;
            top: -3px;
            left: 0;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--primary-blue);
            box-shadow: 0 0 8px rgba(40, 120, 240, 0.6);
            animation: packetTravelLight 3.5s infinite ease-in-out;
        }

        @keyframes packetTravelLight {
            0% { left: 0%; opacity: 0; }
            15% { opacity: 1; }
            85% { opacity: 1; }
            100% { left: 100%; opacity: 0; }
        }

        /* ---------------------------------------------------------------------- */
        /* AI Sign Avatar — Light Panel & Stage                                   */
        /* ---------------------------------------------------------------------- */
        .sign-stage-wrapper {
            position: relative;
            background: linear-gradient(180deg, #FFFFFF 0%, #F4F8FF 100%);
            border: 1px solid var(--border-light);
            border-radius: 24px;
            padding: 16px;
            margin-bottom: 18px;
            box-shadow: var(--card-shadow);
            overflow: hidden;
        }

        /* Soft circular background glow behind avatar */
        .sign-stage-wrapper::before {
            content: "";
            position: absolute;
            bottom: 0;
            left: 12%;
            right: 12%;
            height: 140px;
            background: radial-gradient(ellipse at bottom, rgba(40, 120, 240, 0.12) 0%, rgba(139, 92, 246, 0.06) 50%, transparent 75%);
            pointer-events: none;
            z-index: 0;
        }

        /* Gentle decorative rings */
        .stage-orbital-ring {
            position: absolute;
            top: 20px;
            right: 20px;
            width: 130px;
            height: 130px;
            border: 1px dashed rgba(40, 120, 240, 0.18);
            border-radius: 50%;
            pointer-events: none;
            animation: orbitalSpinLight 35s linear infinite;
            z-index: 0;
        }

        @keyframes orbitalSpinLight {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .stage-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
            position: relative;
            z-index: 2;
        }

        .stage-title {
            margin: 0;
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-heading);
            display: flex;
            align-items: center;
            gap: 8px;
            letter-spacing: -0.01em;
            font-family: var(--font-heading);
        }

        .avatar-status-pill {
            font-size: 0.74rem;
            color: var(--primary-blue);
            background: var(--bg-soft-blue);
            padding: 4px 12px;
            border-radius: 999px;
            border: 1px solid #BFDBFE;
            font-weight: 700;
            letter-spacing: 0.02em;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .avatar-status-dot {
            width: 6.5px;
            height: 6.5px;
            border-radius: 50%;
            background: var(--primary-blue);
            box-shadow: 0 0 6px rgba(40, 120, 240, 0.5);
            display: inline-block;
            animation: radarPulseLight 2s infinite ease-in-out;
        }

        iframe {
            border-radius: 18px !important;
            border: 1px solid var(--border-light) !important;
            box-shadow: 0 8px 24px rgba(40, 120, 240, 0.08) !important;
            background: #FFFFFF !important;
        }

        /* ---------------------------------------------------------------------- */
        /* Main Hero Card (Light Theme)                                           */
        /* ---------------------------------------------------------------------- */
        .hero-command-panel {
            background: linear-gradient(135deg, #FFFFFF 0%, #F5F9FF 100%);
            border: 1px solid var(--border-light);
            border-radius: 24px;
            padding: 24px 28px;
            margin-bottom: 22px;
            box-shadow: var(--card-shadow);
            position: relative;
            overflow: hidden;
        }

        .hero-command-panel::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, var(--primary-blue) 0%, var(--lavender) 60%, #38BDF8 100%);
        }

        .capability-chip {
            background: #F0F6FF;
            color: var(--primary-blue);
            padding: 6px 14px;
            border-radius: 999px;
            font-weight: 600;
            font-size: 0.82rem;
            border: 1px solid var(--border-light);
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.22s ease;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        }

        .capability-chip:hover {
            border-color: #BFDBFE;
            background: #E4EFFF;
            transform: translateY(-1.5px);
            box-shadow: 0 4px 12px rgba(40, 120, 240, 0.12);
        }

        /* ---------------------------------------------------------------------- */
        /* Voice Capture Console Framing (Light Theme)                            */
        /* ---------------------------------------------------------------------- */
        .voice-capture-console {
            background: #FFFFFF;
            border: 1px solid var(--border-light);
            border-radius: 24px;
            padding: 20px;
            box-shadow: var(--card-shadow);
            margin-bottom: 18px;
        }

        /* Audio input component styling */
        [data-testid="stAudioInput"] {
            background: #FFFFFF !important;
            border: 1px solid var(--border-light) !important;
            border-radius: 18px !important;
            padding: 14px !important;
            box-shadow: 0 2px 10px rgba(40, 120, 240, 0.04) !important;
            transition: all 0.22s ease !important;
        }

        [data-testid="stAudioInput"]:hover {
            border-color: #BFDBFE !important;
            box-shadow: 0 6px 18px rgba(40, 120, 240, 0.08) !important;
        }

        /* File Uploader compact input panel */
        [data-testid="stFileUploader"] {
            background: #F8FAFD !important;
            border: 2px dashed #C8DEFC !important;
            border-radius: 18px !important;
            padding: 12px !important;
            transition: all 0.22s ease !important;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: var(--primary-blue) !important;
            background: #F0F6FF !important;
        }

        /* Buttons — Light Modern Styling */
        .stButton > button {
            border-radius: 12px !important;
            font-family: var(--font-main) !important;
            font-weight: 700 !important;
            font-size: 0.90rem !important;
            letter-spacing: 0.01em !important;
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
            border: 1px solid var(--border-light) !important;
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #2878F0 0%, #4F46E5 100%) !important;
            border: 1px solid var(--primary-blue) !important;
            color: #FFFFFF !important;
            box-shadow: 0 6px 18px rgba(40, 120, 240, 0.22) !important;
        }

        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #1D63D8 0%, #4338CA 100%) !important;
            box-shadow: 0 8px 24px rgba(40, 120, 240, 0.32) !important;
            transform: translateY(-1.5px) !important;
        }

        .stButton > button[kind="secondary"] {
            background: #FFFFFF !important;
            border: 1px solid var(--border-light) !important;
            color: var(--text-heading) !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
        }

        .stButton > button[kind="secondary"]:hover {
            background: #F0F6FF !important;
            border-color: #BFDBFE !important;
            color: var(--primary-blue) !important;
            box-shadow: 0 4px 14px rgba(40, 120, 240, 0.10) !important;
        }

        /* Selectboxes & Text Inputs */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        .stTextInput > div > div > input {
            background-color: #FFFFFF !important;
            border: 1px solid var(--border-light) !important;
            color: var(--text-heading) !important;
            border-radius: 12px !important;
            font-family: var(--font-main) !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        }

        div[data-baseweb="select"] > div:hover,
        div[data-baseweb="input"] > div:hover,
        .stTextInput > div > div > input:focus {
            border-color: #BFDBFE !important;
            box-shadow: 0 0 0 3px rgba(40, 120, 240, 0.12) !important;
        }

        /* Dropdown popover list items */
        ul[data-baseweb="menu"] {
            background-color: #FFFFFF !important;
            border: 1px solid var(--border-light) !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08) !important;
        }

        li[data-baseweb="menu-item"] {
            color: var(--text-heading) !important;
        }

        /* Expanders */
        [data-testid="stExpander"] {
            background-color: #FFFFFF !important;
            border: 1px solid var(--border-light) !important;
            border-radius: 16px !important;
            box-shadow: var(--card-shadow) !important;
        }

        /* Dataframe styling */
        [data-testid="stDataFrame"] {
            background-color: #FFFFFF !important;
            border: 1px solid var(--border-light) !important;
            border-radius: 14px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
        }

        /* Audio Player Styling */
        audio {
            border-radius: 12px;
            width: 100%;
            filter: drop-shadow(0 2px 8px rgba(40, 120, 240, 0.08));
        }

        /* Alert boxes */
        .stAlert {
            background-color: #EAF3FF !important;
            border: 1px solid #BFDBFE !important;
            color: #1E40AF !important;
            border-radius: 14px !important;
        }

        /* Headings */
        h1, h2, h3, h4 {
            color: var(--text-heading) !important;
            font-family: var(--font-heading) !important;
            letter-spacing: -0.015em !important;
        }

        /* Responsive refinements */
        @media (max-width: 768px) {
            .hero-command-panel {
                padding: 18px 20px;
            }
            .comm-flow-bridge {
                padding: 12px 16px;
            }
            .flow-track {
                gap: 8px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Cached resources
# --------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_whisper_model(model_size: str):
    return whisper.load_model(model_size)


@st.cache_data(show_spinner=False)
def load_sign_database(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        default_data = [
            {"word": "hello", "sign": "👋", "category": "greetings"},
            {"word": "hi", "sign": "👋", "category": "greetings"},
            {"word": "bye", "sign": "👋", "category": "greetings"},
            {"word": "goodbye", "sign": "👋", "category": "greetings"},
            {"word": "welcome", "sign": "👐", "category": "greetings"},
            {"word": "yes", "sign": "👍", "category": "responses"},
            {"word": "no", "sign": "👎", "category": "responses"},
            {"word": "please", "sign": "🙏", "category": "courtesy"},
            {"word": "thank", "sign": "🤝", "category": "courtesy"},
            {"word": "thanks", "sign": "🤝", "category": "courtesy"},
            {"word": "sorry", "sign": "🙇", "category": "courtesy"},
            {"word": "help", "sign": "🆘", "category": "common"},
            {"word": "stop", "sign": "🛑", "category": "common"},
            {"word": "go", "sign": "🟢", "category": "common"},
            {"word": "good", "sign": "👍", "category": "common"},
            {"word": "bad", "sign": "👎", "category": "common"},
            {"word": "love", "sign": "❤️", "category": "emotions"},
            {"word": "happy", "sign": "😊", "category": "emotions"},
            {"word": "sad", "sign": "😢", "category": "emotions"},
            {"word": "angry", "sign": "😠", "category": "emotions"},
            {"word": "water", "sign": "💧", "category": "food"},
            {"word": "food", "sign": "🍲", "category": "food"},
            {"word": "eat", "sign": "🍽️", "category": "food"},
            {"word": "drink", "sign": "🥤", "category": "food"},
            {"word": "coffee", "sign": "☕", "category": "food"},
            {"word": "tea", "sign": "🍵", "category": "food"},
            {"word": "friend", "sign": "🧑‍🤝‍🧑", "category": "people"},
            {"word": "family", "sign": "👨‍👩‍👧‍👦", "category": "people"},
            {"word": "mother", "sign": "👩", "category": "people"},
            {"word": "father", "sign": "👨", "category": "people"},
            {"word": "brother", "sign": "👦", "category": "people"},
            {"word": "sister", "sign": "👧", "category": "people"},
            {"word": "peace", "sign": "✌️", "category": "gestures"},
            {"word": "okay", "sign": "👌", "category": "gestures"},
            {"word": "victory", "sign": "✌️", "category": "gestures"},
            {"word": "clap", "sign": "👏", "category": "gestures"},
            {"word": "call", "sign": "🤙", "category": "gestures"},
            {"word": "pray", "sign": "🙏", "category": "gestures"},
            {"word": "look", "sign": "👀", "category": "senses"},
            {"word": "listen", "sign": "👂", "category": "senses"},
            {"word": "speak", "sign": "🗣️", "category": "senses"},
            {"word": "home", "sign": "🏠", "category": "places"},
            {"word": "school", "sign": "🏫", "category": "places"},
            {"word": "work", "sign": "💼", "category": "places"},
            {"word": "car", "sign": "🚗", "category": "transport"},
            {"word": "bus", "sign": "🚌", "category": "transport"},
            {"word": "time", "sign": "⏰", "category": "common"},
            {"word": "day", "sign": "☀️", "category": "time"},
            {"word": "night", "sign": "🌙", "category": "time"},
            {"word": "money", "sign": "💰", "category": "common"},
            {"word": "question", "sign": "❓", "category": "common"},
        ]
        df = pd.DataFrame(default_data)
        df.to_csv(path, index=False)
        return df
    df = pd.read_csv(path)
    df["word"] = df["word"].str.lower().str.strip()
    df = df.drop_duplicates(subset="word", keep="first").reset_index(drop=True)
    return df


def fingerspell(word: str) -> str:
    """Fallback for words not in the database: spell it out with
    regional-indicator emoji letters, standing in for ASL fingerspelling."""
    letters = []
    for ch in word.lower():
        if "a" <= ch <= "z":
            letters.append(chr(FINGERSPELL_BASE + (ord(ch) - ord("a"))))
    return "".join(letters) if letters else "❓"


def clean_tokens(text: str) -> list[str]:
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation.replace("'", "")))
    tokens = re.findall(r"[a-z']+", text)
    return tokens


def words_to_signs(tokens: list[str], df: pd.DataFrame) -> pd.DataFrame:
    columns = ["word", "sign", "category", "matched"]
    if not tokens:
        return pd.DataFrame(columns=columns), 0.0

    lookup = df.set_index("word")["sign"].to_dict()
    cats = df.set_index("word")["category"].to_dict()

    rows = []
    hits = np.zeros(len(tokens), dtype=bool)
    for i, tok in enumerate(tokens):
        if tok in lookup:
            rows.append({"word": tok, "sign": lookup[tok], "category": cats[tok], "matched": True})
            hits[i] = True
        else:
            rows.append({"word": tok, "sign": fingerspell(tok), "category": "fingerspelled", "matched": False})
    coverage = float(hits.mean()) * 100 if len(hits) else 0.0
    return pd.DataFrame(rows, columns=columns), coverage


def resample(audio: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
    if orig_sr == target_sr or len(audio) == 0:
        return audio
    duration = len(audio) / orig_sr
    target_len = max(1, int(round(duration * target_sr)))
    x_old = np.linspace(0, duration, num=len(audio), endpoint=False)
    x_new = np.linspace(0, duration, num=target_len, endpoint=False)
    return np.interp(x_new, x_old, audio).astype(np.float32)


def trim_silence(audio: np.ndarray, threshold: float = 0.015, pad_samples: int = 1600) -> np.ndarray:
    """Carefully remove leading/trailing silence from 16kHz audio with safety padding."""
    if len(audio) == 0:
        return audio

    abs_audio = np.abs(audio)
    max_amp = float(np.max(abs_audio))
    if max_amp == 0:
        return audio

    thresh = max(threshold, 0.05 * max_amp)
    above_thresh = np.where(abs_audio > thresh)[0]

    if len(above_thresh) == 0:
        return audio

    start_idx = max(0, above_thresh[0] - pad_samples)
    end_idx = min(len(audio), above_thresh[-1] + pad_samples)
    return audio[start_idx:end_idx]


def preprocess_audio(audio: np.ndarray) -> np.ndarray:
    """Preprocess audio: float32 mono 16kHz, silence trimmed, and non-destructive normalization."""
    if len(audio) == 0:
        return audio

    audio = audio.astype(np.float32)
    audio = trim_silence(audio)

    max_abs = float(np.max(np.abs(audio))) if len(audio) > 0 else 0.0
    if max_abs > 0.05:
        audio = (audio / max_abs) * 0.95

    return audio.astype(np.float32)


def extract_audio_from_uploaded_file(file_bytes: bytes, file_name: str) -> bytes:
    """Extracts raw audio WAV bytes from audio or video uploads."""
    lower_name = file_name.lower()
    video_exts = [".mp4", ".mov", ".avi", ".webm", ".mkv"]
    is_video = any(lower_name.endswith(ext) for ext in video_exts)

    if is_video and MOVIEPY_AVAILABLE:
        ext = os.path.splitext(file_name)[1] or ".mp4"
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp_in:
            temp_in.write(file_bytes)
            temp_in_path = temp_in.name

        temp_out_path = temp_in_path + "_audio.wav"
        try:
            clip = VideoFileClip(temp_in_path)
            if clip.audio is not None:
                clip.audio.write_audiofile(
                    temp_out_path, fps=16000, nbytes=2, codec="pcm_s16le", logger=None
                )
                clip.close()
                with open(temp_out_path, "rb") as f:
                    audio_bytes = f.read()
                return audio_bytes
            else:
                raise ValueError("The uploaded video does not contain an audio track.")
        finally:
            for p in [temp_in_path, temp_out_path]:
                if os.path.exists(p):
                    try:
                        os.remove(p)
                    except Exception:
                        pass
    return file_bytes


def bytes_to_audio_array(audio_bytes: bytes) -> tuple[np.ndarray, dict]:
    """Decode audio entirely in-memory with soundfile (libsndfile).
    Calculates diagnostic metrics, resamples to mono float32 16kHz,
    and preprocesses for Whisper ASR."""
    data, sr = sf.read(io.BytesIO(audio_bytes), dtype="float32", always_2d=False)
    if data.ndim > 1:
        data = data.mean(axis=1)  # downmix to mono

    num_samples = len(data)
    duration_s = float(num_samples / sr) if sr > 0 else 0.0
    min_amp = float(np.min(data)) if num_samples > 0 else 0.0
    max_amp = float(np.max(data)) if num_samples > 0 else 0.0
    rms = float(np.sqrt(np.mean(data**2))) if num_samples > 0 else 0.0

    diag = {
        "sample_rate": sr,
        "num_samples": num_samples,
        "duration_s": round(duration_s, 3),
        "min_amplitude": round(min_amp, 5),
        "max_amplitude": round(max_amp, 5),
        "rms_amplitude": round(rms, 5),
    }

    # Resample to 16000 Hz float32
    resampled = resample(data, sr, WHISPER_SR).astype(np.float32)
    preprocessed = preprocess_audio(resampled)

    return preprocessed, diag


# --------------------------------------------------------------------------
# ASR Router & Backends
# --------------------------------------------------------------------------
class BaseASRBackend:
    name: str = "Base ASR"

    def transcribe(self, audio_bytes: bytes, preprocessed_audio: np.ndarray, language_code: str = None) -> tuple[str, str]:
        raise NotImplementedError


class WhisperASRBackend(BaseASRBackend):
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.name = f"Whisper ({model_size})"

    def transcribe(self, audio_bytes: bytes, preprocessed_audio: np.ndarray, language_code: str = None) -> tuple[str, str]:
        try:
            model = load_whisper_model(self.model_size)
        except Exception as exc:
            raise RuntimeError(
                f"Whisper model '{self.model_size}' could not be loaded. "
                "Try the base or tiny model."
            ) from exc
        transcribe_kwargs = {
            "task": "transcribe",
            "fp16": False,
            "temperature": 0.0,
            "condition_on_previous_text": False,
        }
        if language_code:
            transcribe_kwargs["language"] = language_code

        result = model.transcribe(preprocessed_audio, **transcribe_kwargs)
        text = result.get("text", "").strip()
        detected_lang = result.get("language", language_code or "en")
        return text, detected_lang


class IndicASRBackend(BaseASRBackend):
    name: str = "Indic ASR Engine (AI4Bharat / Google Indic)"

    def __init__(self):
        self._recognizer = sr.Recognizer()

    def transcribe(self, audio_bytes: bytes, preprocessed_audio: np.ndarray, language_code: str = None) -> tuple[str, str]:
        lang_tag = INDIC_LANGUAGE_TAGS.get(language_code, "hi-IN" if language_code == "hi" else f"{language_code}-IN")
        wav_buf = io.BytesIO()
        sf.write(wav_buf, preprocessed_audio, WHISPER_SR, format="WAV")
        wav_buf.seek(0)

        with sr.AudioFile(wav_buf) as source:
            audio_data = self._recognizer.record(source)

        text = self._recognizer.recognize_google(audio_data, language=lang_tag)
        return text.strip(), language_code or "hi"


class ASRRouter:
    def __init__(self, whisper_model_size: str = "base"):
        self.whisper_model_size = whisper_model_size
        self.whisper_backend = WhisperASRBackend(whisper_model_size)
        self.indic_backend = IndicASRBackend()

    def route_and_transcribe(
        self, audio_bytes: bytes, preprocessed_audio: np.ndarray, language: str = None
    ) -> tuple[str, str, dict]:
        lang_code = LANGUAGE_MAP.get(language, language) if language else None
        if lang_code == "Auto Detect":
            lang_code = None

        backend_used = None
        transcript = ""
        detected_lang = lang_code or "en"
        fallback_used = False

        if lang_code in INDIC_LANGUAGE_TAGS:
            try:
                transcript, detected_lang = self.indic_backend.transcribe(
                    audio_bytes, preprocessed_audio, lang_code
                )
                backend_used = f"{self.indic_backend.name} [{INDIC_LANGUAGE_TAGS[lang_code]}]"
            except Exception as indic_err:
                transcript, detected_lang = self.whisper_backend.transcribe(
                    audio_bytes, preprocessed_audio, lang_code
                )
                backend_used = f"Whisper ({self.whisper_model_size}) [Fallback from Indic ASR: {indic_err}]"
                fallback_used = True
        else:
            transcript, detected_lang = self.whisper_backend.transcribe(
                audio_bytes, preprocessed_audio, lang_code
            )
            backend_used = self.whisper_backend.name

        debug_info = {
            "selected_language": language or "Auto Detect",
            "passed_language_code": lang_code,
            "asr_backend": backend_used,
            "model_size": self.whisper_model_size,
            "returned_language": detected_lang,
            "fallback_used": fallback_used,
        }
        return transcript, detected_lang, debug_info


def transcribe_multilingual(
    audio_bytes: bytes, language: str = None, model_size: str = "base"
) -> tuple[str, str, dict, dict]:
    """Modular ASR Speech Recognition Entrypoint."""
    try:
        preprocessed_audio, audio_diag = bytes_to_audio_array(audio_bytes)
    except Exception as exc:
        raise RuntimeError(
            "Couldn't decode audio/video. Please ensure file is a valid audio or video recording."
        ) from exc

    if audio_diag["rms_amplitude"] < 0.005:
        raise ValueError("Audio volume is too low. Please record again closer to the microphone.")

    # Run Speech Transcription via Router
    router = ASRRouter(whisper_model_size=model_size)
    transcript, detected_lang, debug_info = router.route_and_transcribe(
        audio_bytes, preprocessed_audio, language=language
    )

    return transcript, detected_lang, debug_info, audio_diag


def translate_to_english(text: str, source_language: str = "auto") -> tuple[str, str]:
    if not text or not text.strip():
        return text, "None"

    if source_language in ("English", "en"):
        return text, "None (Source is English)"

    src = LANGUAGE_MAP.get(source_language, source_language) or "auto"
    if src == "en":
        return text, "None (Source is English)"

    backend_name = f"IndicTrans / Google Translator ({src} → en)"
    try:
        translated = GoogleTranslator(source=src, target="en").translate(text)
        if translated:
            return translated.strip(), backend_name
    except Exception:
        pass

    try:
        translated = GoogleTranslator(source="auto", target="en").translate(text)
        return (translated.strip() if translated else text), backend_name
    except Exception as exc:
        raise RuntimeError(f"Translation failed: {exc}") from exc




# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# Mode Navigation & Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="identity-panel">
            <div class="identity-card">
                <span class="corner-tick tick-tl"></span>
                <span class="corner-tick tick-tr"></span>
                <span class="corner-tick tick-bl"></span>
                <span class="corner-tick tick-br"></span>
                <div class="identity-icon-box">
                    🤟
                </div>
                <div>
                    <div class="identity-title">
                        SIGNBRIDGE AI
                    </div>
                    <div class="identity-subtitle">
                        AI Communication For Everyone
                    </div>
                </div>
            </div>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 0 4px; margin-bottom: 8px;">
            <span style="font-size:0.72rem; font-weight:700; color:#2878F0; letter-spacing:0.08em; text-transform:uppercase;">
                NAVIGATION
            </span>
            <span style="font-size:0.68rem; color:#64748B; font-weight:600; letter-spacing:0.04em;">
                STUDIO V2
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    app_mode = st.radio(
        "Select Feature Mode",
        ["🎙️ Speech → Sign", "🤟 Sign → Speech"],
        index=0,
        label_visibility="collapsed",
    )
    st.divider()

if app_mode == "🤟 Sign → Speech":
    with st.sidebar:
        st.markdown("### ℹ️ Sign → Speech Guide")
        st.info(
            "**Quick Instructions:**\n\n"
            "1. Allow webcam access when prompted.\n"
            "2. Keep your hand visible in camera frame.\n"
            "3. Perform any of the 24 Everyday Signs.\n"
            "4. Hear the instant spoken voice and see text!"
        )
        st.caption("⚡ Powered by MediaPipe Hands + Web Speech API")

    render_sign_to_speech_page()

else:
    with st.sidebar:
        st.header("⚙️ Settings")
        model_size = st.selectbox(
            "Whisper model size",
            ["tiny", "base", "small"],
            index=1,
            help="Bigger = more accurate speech recognition. 'base' recommended.",
        )

        language = st.selectbox(
            "Speech Language",
            [
                "Auto Detect",
                "English",
                "Hindi",
                "Gujarati",
                "Kannada",
                "Tamil",
                "Telugu",
            ],
            index=0,
        )
        st.caption("Select your spoken language or leave on Auto Detect.")

        st.divider()

        st.divider()
        st.header("📖 Sign database")
        db_df = load_sign_database(DB_PATH)
        st.caption(f"{len(db_df)} words currently mapped to a sign.")
        search = st.text_input("Search a word")
        if search:
            matches = db_df[db_df["word"].str.contains(search.lower(), na=False)]
            st.dataframe(matches, hide_index=True, use_container_width=True)

        with st.expander("➕ Add a custom word / sign"):
            new_word = st.text_input("Word", key="new_word")
            new_sign = st.text_input("Sign (emoji)", key="new_sign")
            new_cat = st.text_input("Category", value="custom", key="new_cat")
            if st.button("Add to database"):
                if new_word and new_sign:
                    updated = pd.concat(
                        [db_df, pd.DataFrame([{"word": new_word.lower().strip(), "sign": new_sign, "category": new_cat}])],
                        ignore_index=True,
                    ).drop_duplicates(subset="word", keep="last")
                    updated.to_csv(DB_PATH, index=False)
                    load_sign_database.clear()
                    st.success(f"Added '{new_word}' -> {new_sign}")
                    st.rerun()
                else:
                    st.warning("Enter both a word and a sign first.")

        if st.button("🗑️ Clear history"):
            st.session_state.history = []
            st.rerun()

    # Top Product Bar
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px 22px; background: #FFFFFF; border: 1px solid var(--border-light); border-radius: 16px; margin-bottom: 18px; box-shadow: var(--card-shadow);">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 0.88rem; font-weight: 800; color: #14213D; letter-spacing: 0.02em; display: flex; align-items: center; gap: 8px; font-family: var(--font-heading);">
                    <span style="display: flex; align-items: center; justify-content: center; width: 26px; height: 26px; border-radius: 7px; background: linear-gradient(135deg, #2878F0 0%, #8B5CF6 100%); color: #FFFFFF; font-size: 0.95rem;">🤟</span> SIGNBRIDGE AI
                </span>
                <span style="color: #DCE7F5; font-size: 1.0rem;">|</span>
                <span style="font-size: 0.78rem; color: #64748B; font-weight: 500; letter-spacing: 0.01em;">
                    Two-Way AI Accessibility Platform
                </span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; background: #ECFDF5; border: 1px solid #A7F3D0; padding: 5px 14px; border-radius: 999px; box-shadow: 0 2px 6px rgba(16, 185, 129, 0.08);">
                <span style="width: 7px; height: 7px; border-radius: 50%; background: #10B981; display: inline-block;"></span>
                <span style="font-size: 0.72rem; font-weight: 800; color: #047857; letter-spacing: 0.06em;">AI SYSTEM ONLINE</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Speech to Sign Hero Card — "Communication Command Panel"
    st.markdown(
        """
        <div class="hero-command-panel">
            <span class="corner-tick tick-tl"></span>
            <span class="corner-tick tick-tr"></span>
            <span class="corner-tick tick-bl"></span>
            <span class="corner-tick tick-br"></span>
            <div style="display: flex; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; gap: 16px; position: relative; z-index: 1;">
                <div style="max-width: 680px;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        <span style="font-size: 1.25rem;">🤟</span>
                        <span style="font-size: 0.76rem; font-weight: 800; color: #2878F0; letter-spacing: 0.08em; text-transform: uppercase;">SPEECH TO SIGN</span>
                        <span style="background: #EAF3FF; color: #2878F0; font-size: 0.68rem; padding: 3px 10px; border-radius: 6px; font-weight: 700; border: 1px solid #BFDBFE;">GESTUREFLOW STUDIO</span>
                    </div>
                    <h1 style="margin: 0; font-size: 1.95rem; color: #14213D; font-weight: 800; letter-spacing: -0.02em; line-height: 1.25; font-family: var(--font-heading);">
                        Breaking communication <span style="background: linear-gradient(135deg, #2878F0 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">barriers with AI</span>
                    </h1>
                    <p style="margin: 10px 0 0 0; color: #64748B; font-size: 0.94rem; line-height: 1.6;">
                        Convert speech into expressive sign language using AI-powered speech recognition, translation, and a human-like 3D avatar.
                    </p>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: center;">
                    <span class="capability-chip">⚡ Whisper ASR</span>
                    <span class="capability-chip">🌐 Multilingual</span>
                    <span class="capability-chip">🤟 Sign Translation</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Center Communication Flow Decorative Bridge
    st.markdown(
        """
        <div class="comm-flow-bridge">
            <div class="flow-track">
                <div class="flow-node voice-node">
                    <span style="display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 50%; background: #2878F0; color: #FFFFFF; font-size: 0.72rem; box-shadow: 0 2px 8px rgba(40,120,240,0.35);">🎙️</span>
                    <span>VOICE INPUT</span>
                </div>
                <div class="flow-connector-line"></div>
                <div class="flow-node ai-node">
                    <span style="display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 50%; background: #8B5CF6; color: #FFFFFF; font-size: 0.72rem; box-shadow: 0 2px 8px rgba(139,92,246,0.35);">🧠</span>
                    <span>AI UNDERSTANDING</span>
                </div>
                <div class="flow-connector-line"></div>
                <div class="flow-node sign-node">
                    <span style="display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 50%; background: #10B981; color: #FFFFFF; font-size: 0.72rem; box-shadow: 0 2px 8px rgba(16,185,129,0.35);">🤟</span>
                    <span>SIGN LANGUAGE</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_input, col_output = st.columns([1, 1.4], gap="large")

    with col_input:
        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                <h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #14213D; display: flex; align-items: center; gap: 8px; font-family: var(--font-heading);">
                    <span>🎙️</span> Voice Input
                </h3>
                <span style="font-size: 0.74rem; color: #047857; background: #ECFDF5; padding: 4px 12px; border-radius: 999px; border: 1px solid #A7F3D0; font-weight: 700; display: inline-flex; align-items: center; gap: 6px;">
                    <span style="width: 6px; height: 6px; border-radius: 50%; background: #10B981; display: inline-block;"></span>● Ready to listen
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        audio_value = st.audio_input("Record your speech")
        uploaded_file = st.file_uploader(
            "OR UPLOAD AUDIO / VIDEO (WAV, FLAC, OGG, MP3, MP4, MOV, AVI, WEBM)",
            type=["wav", "flac", "ogg", "mp3", "mp4", "mov", "avi", "webm", "mkv"],
        )

        raw_uploaded_bytes = None
        file_name = ""
        if audio_value is not None:
            raw_uploaded_bytes = audio_value.getvalue()
            file_name = "mic_recording.wav"
        elif uploaded_file is not None:
            raw_uploaded_bytes = uploaded_file.getvalue()
            file_name = uploaded_file.name

        audio_bytes = None
        if raw_uploaded_bytes is not None:
            try:
                audio_bytes = extract_audio_from_uploaded_file(raw_uploaded_bytes, file_name)
            except Exception as vid_err:
                st.error(f"Error extracting audio: {vid_err}")
                audio_bytes = None

        if audio_bytes is not None:
            st.markdown("**Audio Playback:**")
            st.audio(audio_bytes)

        run = st.button("✨ Convert to Signs ➡️", type="primary", disabled=audio_bytes is None, use_container_width=True)

    with col_output:
        st.markdown(
            """
            <div class="stage-header">
                <h3 class="stage-title">
                    <span>👤</span> AI Sign Avatar
                </h3>
                <span class="avatar-status-pill">
                    <span class="avatar-status-dot"></span>● Avatar Ready
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Determine 3D Avatar State & URL
        if st.session_state.history:
            item = st.session_state.history[0]
            if isinstance(item, dict):
                transcript = item["transcript"]
                english_text = item["english_text"]
                display_lang = item.get("display_lang", "English")
                signs_df = item["signs_df"]
                coverage = item["coverage"]
                is_translated = item.get("is_translated", False)
                trans_backend = item.get("trans_backend", "IndicTrans / Google Translator")
            else:
                transcript, signs_df, coverage = item
                english_text = transcript
                display_lang = "English"
                is_translated = False
                trans_backend = "None"

            encoded_text = urllib.parse.quote(english_text)
            react_url = (
                f"https://ai-avatar-jade-zeta.vercel.app/?text={encoded_text}"
                f"&speed=0.10&pause=800&emotion=neutral&intensity=40"
            )
        else:
            react_url = (
                "https://ai-avatar-jade-zeta.vercel.app/?text=Hello"
                "&speed=0.10&pause=800&emotion=neutral&intensity=40"
            )

        # Sign Stage Holographic Frame
        st.markdown(
            """
            <div class="sign-stage-wrapper">
                <span class="corner-tick tick-tl"></span>
                <span class="corner-tick tick-tr"></span>
                <span class="corner-tick tick-bl"></span>
                <span class="corner-tick tick-br"></span>
                <div class="stage-orbital-ring"></div>
                <div class="stage-grid-floor"></div>
            """,
            unsafe_allow_html=True,
        )
        if hasattr(st, "iframe"):
            st.iframe(react_url, width=800, height=560)
        else:
            components.iframe(react_url, width=800, height=560)
        st.markdown("</div>", unsafe_allow_html=True)

        if run and audio_bytes is not None:
            with st.spinner("Transcribing speech with Whisper..."):
                try:
                    transcript, detected_lang, debug_info, audio_diag = transcribe_multilingual(
                        audio_bytes, language=language, model_size=model_size
                    )
                except ValueError as exc:
                    st.warning(str(exc))
                    transcript, detected_lang, debug_info, audio_diag = None, None, {}, {}
                except RuntimeError as exc:
                    st.error(str(exc))
                    transcript, detected_lang, debug_info, audio_diag = None, None, {}, {}
                except Exception as exc:
                    st.error(f"Speech Recognition Error: {exc}")
                    transcript, detected_lang, debug_info, audio_diag = None, None, {}, {}

            if transcript == "":
                st.warning("Didn't catch any speech in that clip — try again.")
            elif transcript:
                lang_code = detected_lang or (LANGUAGE_MAP.get(language) if language != "Auto Detect" else None)
                display_lang = CODE_TO_LANGUAGE.get(
                    lang_code, language if language != "Auto Detect" else (lang_code.title() if lang_code else "English")
                )

                is_english = (lang_code == "en") or (language == "English")
                english_text = transcript
                trans_backend = "None (English Speech)"
                is_translated = False

                if not is_english:
                    with st.spinner("Translating speech to English..."):
                        try:
                            english_text, trans_backend = translate_to_english(transcript, source_language=lang_code or language)
                            is_translated = english_text.strip().lower() != transcript.strip().lower()
                        except Exception as exc:
                            st.warning(f"Translation warning: {exc}. Using original transcript.")
                            english_text = transcript
                            trans_backend = f"Error ({exc})"
                            is_translated = False

                tokens = clean_tokens(english_text)
                signs_df, coverage = words_to_signs(tokens, db_df)
                st.session_state.history.insert(
                    0,
                    {
                        "transcript": transcript,
                        "english_text": english_text,
                        "display_lang": display_lang,
                        "debug_info": debug_info,
                        "audio_diag": audio_diag,
                        "trans_backend": trans_backend,
                        "model_size": model_size,
                        "signs_df": signs_df,
                        "coverage": coverage,
                        "is_translated": is_translated,
                    },
                )
                st.rerun()

        if st.session_state.history:
            item = st.session_state.history[0]
            if isinstance(item, dict):
                transcript = item["transcript"]
                english_text = item["english_text"]
                display_lang = item.get("display_lang", "English")
                signs_df = item["signs_df"]
                coverage = item["coverage"]
                is_translated = item.get("is_translated", False)
                trans_backend = item.get("trans_backend", "IndicTrans / Google Translator")
            else:
                transcript, signs_df, coverage = item
                english_text = transcript
                display_lang = "English"
                is_translated = False
                trans_backend = "None"

            # Recognized Speech Card (Light Theme)
            st.markdown(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #DCE7F5; border-radius: 20px; padding: 18px 22px; margin-bottom: 14px; box-shadow: 0 10px 30px rgba(40, 120, 240, 0.08);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 0.76rem; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em;">Recognized Speech</span>
                        <span style="font-size: 0.72rem; color: #2878F0; background: #EAF3FF; padding: 3px 10px; border-radius: 6px; border: 1px solid #BFDBFE; font-weight: 700;">{display_lang}</span>
                    </div>
                    <div style="font-size: 1.18rem; font-weight: 600; color: #14213D; line-height: 1.45;">"{transcript}"</div>
                    {f'<div style="font-size: 0.90rem; color: #2878F0; margin-top: 6px; font-weight: 500;"><b>English:</b> "{english_text}"</div>' if is_translated else ''}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.progress(coverage / 100, text=f"{coverage:.0f}% of words mapped directly to sign animations")

            n_cols = 6
            rows_needed = int(np.ceil(len(signs_df) / n_cols)) if len(signs_df) else 0
            idx = 0
            for _ in range(rows_needed):
                cols = st.columns(n_cols)
                for c in cols:
                    if idx >= len(signs_df):
                        break
                    row = signs_df.iloc[idx]
                    with c:
                        st.markdown(
                            f"""
                            <div style="background: #FFFFFF; border: 1px solid #DCE7F5; border-radius: 14px; padding: 12px 6px; text-align: center; margin-bottom: 8px; transition: all 0.2s ease; box-shadow: 0 4px 14px rgba(40, 120, 240, 0.05);">
                                <div style="font-size: 1.85rem; margin-bottom: 4px;">{row['sign']}</div>
                                <div style="font-size: 0.76rem; font-weight: 700; color: #2878F0; text-transform: uppercase; letter-spacing: 0.04em;">{row['word']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    idx += 1

            with st.expander("Show as table"):
                st.dataframe(signs_df, hide_index=True, use_container_width=True)
        else:
            st.info("Record audio or upload an audio/video file, then press 'Convert to signs'.")

    if len(st.session_state.history) > 1:
        st.divider()
        st.subheader("🕘 History")
        for item in st.session_state.history[1:]:
            if isinstance(item, dict):
                hist_orig = item["transcript"]
                hist_eng = item["english_text"]
                hist_signs = item["signs_df"]
                hist_cov = item["coverage"]
                label = hist_eng if hist_eng != hist_orig else hist_orig
            else:
                hist_orig, hist_signs, hist_cov = item
                label = hist_orig
            with st.expander(f"{label[:50]}{'...' if len(label) > 50 else ''}"):
                st.write("".join(hist_signs["sign"].tolist()))
                st.caption(f"{hist_cov:.0f}% direct match")