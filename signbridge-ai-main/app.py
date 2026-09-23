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
from emotion_engine import (
    load_all_emotion_models,
    analyze_audio_emotion_multimodal,
    ALL_SUPPORTED_EMOTIONS,
)
from ui_components.styles import get_modern_css
from ui_components.shell import render_sidebar, render_top_bar
from ui_components.views.home import render_home_view
from ui_components.views.translator import render_translator_view
from ui_components.views.live_conversation import render_live_conversation_view
from ui_components.views.learn_isl import render_learn_isl_view
from ui_components.views.emergency import render_emergency_view
from ui_components.views.library import (
    render_sign_library_view,
    render_saved_phrases_view,
    render_history_view,
)
from ui_components.views.accessibility import (
    render_accessibility_view,
    render_settings_view,
)

try:
    from moviepy import VideoFileClip
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

EMOTION_META = {
    "HAPPY": {"emoji": "😊", "color": "#10b981", "desc": "Happy / Joyful", "bg": "linear-gradient(135deg, #064e3b, #047857)"},
    "SAD": {"emoji": "😢", "color": "#3b82f6", "desc": "Sad / Subdued", "bg": "linear-gradient(135deg, #1e3a8a, #1d4ed8)"},
    "ANGRY": {"emoji": "😠", "color": "#ef4444", "desc": "Angry / Frustrated", "bg": "linear-gradient(135deg, #7f1d1d, #b91c1c)"},
    "FEAR": {"emoji": "😨", "color": "#8b5cf6", "desc": "Fearful / Anxious", "bg": "linear-gradient(135deg, #4c1d95, #6d28d9)"},
    "SURPRISE": {"emoji": "😲", "color": "#06b6d4", "desc": "Surprised / Excited", "bg": "linear-gradient(135deg, #164e63, #0891b2)"},
    "DISGUST": {"emoji": "🤢", "color": "#84cc16", "desc": "Disgusted / Aversive", "bg": "linear-gradient(135deg, #365314, #4d7c0f)"},
    "NEUTRAL": {"emoji": "😐", "color": "#64748b", "desc": "Neutral / Calm", "bg": "linear-gradient(135deg, #0f172a, #1e293b)"},
    "UNCERTAIN": {"emoji": "❓", "color": "#f59e0b", "desc": "Uncertain / Mixed", "bg": "linear-gradient(135deg, #451a03, #78350f)"},
}


@st.cache_resource(show_spinner=False)
def get_cached_emotion_model():
    """Caches the multimodal emotion recognition models (Speech wav2vec2 + NLP DistilRoBERTa) across Streamlit runs."""
    return load_all_emotion_models()

st.set_page_config(page_title="SIGNBRIDGE AI TEST - AI Communication For Everyone", page_icon="🤟", layout="wide")

# --------------------------------------------------------------------------
# SIGNBRIDGE AI — Modern 2026 SaaS Light-First Theme
# --------------------------------------------------------------------------
st.markdown(
    get_modern_css(
        high_contrast=st.session_state.get("high_contrast", False),
        large_text=st.session_state.get("large_text", False),
        reduced_motion=st.session_state.get("reduced_motion", False),
    ),
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
    and preprocesses for Whisper and Emotion DSP."""
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
    def __init__(self, model_size: str = "small"):
        self.model_size = model_size
        self.name = f"Whisper ({model_size})"

    def transcribe(self, audio_bytes: bytes, preprocessed_audio: np.ndarray, language_code: str = None) -> tuple[str, str]:
        model = load_whisper_model(self.model_size)
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
    def __init__(self, whisper_model_size: str = "small"):
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
    audio_bytes: bytes, language: str = None, model_size: str = "small"
) -> tuple[str, str, dict, dict, dict]:
    """Modular ASR + Multimodal Emotion Entrypoint."""
    try:
        preprocessed_audio, audio_diag = bytes_to_audio_array(audio_bytes)
    except Exception as exc:
        raise RuntimeError(
            "Couldn't decode audio/video. Please ensure file is a valid audio or video recording."
        ) from exc

    if audio_diag["rms_amplitude"] < 0.005:
        raise ValueError("Audio volume is too low. Please record again closer to the microphone.")

    # 1. Run Speech Transcription via Router
    router = ASRRouter(whisper_model_size=model_size)
    transcript, detected_lang, debug_info = router.route_and_transcribe(
        audio_bytes, preprocessed_audio, language=language
    )

    # 2. Run Tri-Modal Emotion Analysis (Audio 50% + Text 30% + Prosody 20%)
    emotion_model_tuple = get_cached_emotion_model()
    emotion_data = analyze_audio_emotion_multimodal(
        preprocessed_audio, sr=WHISPER_SR, transcript=transcript, models_tuple=emotion_model_tuple
    )

    return transcript, detected_lang, debug_info, audio_diag, emotion_data


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
# Dynamic Emotion-Aware Avatar Renderer
# --------------------------------------------------------------------------
def render_avatar(text: str, emotion: str = "NEUTRAL", intensity: float = 40.0, confidence: float = 70.0) -> str:
    """HTML / CSS procedural animated facial rig as fallback avatar."""
    em_meta = EMOTION_META.get(emotion, EMOTION_META["NEUTRAL"])
    emoji = em_meta["emoji"]
    accent_color = em_meta["color"]
    bg_gradient = em_meta["bg"]
    safe_text = html.escape(text) if text else "Ready to communicate."

    # Visual expression attributes
    mouth_height = 10
    mouth_radius = "0 0 16px 16px"
    mouth_bg = "#d9485f"
    eyebrow_left_rotate = "0deg"
    eyebrow_right_rotate = "0deg"
    eyebrow_top = "40px"
    eye_scale_y = "1.0"
    eye_scale_x = "1.0"
    anim_speed = max(0.08, 0.20 - (intensity / 100.0) * 0.12)

    if emotion == "HAPPY":
        mouth_radius = "0 0 26px 26px / 0 0 20px 20px"
        mouth_height = 16
        eyebrow_left_rotate = "-10deg"
        eyebrow_right_rotate = "10deg"
        eyebrow_top = "38px"
        eye_scale_y = "0.8"
    elif emotion == "ANGRY":
        mouth_radius = "4px"
        mouth_height = 12
        mouth_bg = "#b91c1c"
        eyebrow_left_rotate = "25deg"
        eyebrow_right_rotate = "-25deg"
        eyebrow_top = "44px"
    elif emotion == "SAD":
        mouth_radius = "18px 18px 0 0 / 14px 14px 0 0"
        mouth_height = 10
        eyebrow_left_rotate = "-18deg"
        eyebrow_right_rotate = "18deg"
        eyebrow_top = "38px"
        eye_scale_y = "0.7"
    elif emotion == "FEAR":
        mouth_radius = "8px"
        mouth_height = 14
        eyebrow_left_rotate = "-22deg"
        eyebrow_right_rotate = "22deg"
        eyebrow_top = "36px"
        eye_scale_y = "1.3"
        eye_scale_x = "1.2"
    elif emotion == "SURPRISE":
        mouth_radius = "50%"
        mouth_height = 24
        eyebrow_left_rotate = "-12deg"
        eyebrow_right_rotate = "12deg"
        eyebrow_top = "32px"
        eye_scale_y = "1.4"
        eye_scale_x = "1.3"
    elif emotion == "DISGUST":
        mouth_radius = "0 14px 0 14px"
        mouth_height = 12
        eyebrow_left_rotate = "15deg"
        eyebrow_right_rotate = "-8deg"
        eyebrow_top = "42px"

    return f"""
    <style>
        .avatar-shell {{
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            background: {bg_gradient};
            border-radius: 22px;
            padding: 20px 14px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.35);
            border: 2px solid {accent_color}55;
            position: relative;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}

        .emotion-badge {{
            position: absolute;
            top: 12px;
            right: 14px;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid {accent_color};
            color: white;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
            backdrop-filter: blur(8px);
        }}

        .avatar-wrap {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .avatar {{
            position: relative;
            width: 180px;
            height: 220px;
        }}

        .head {{
            position: absolute;
            left: 50%;
            top: 18px;
            transform: translateX(-50%);
            width: 120px;
            height: 120px;
            background: #f7d7b5;
            border-radius: 50%;
            border: 4px solid #2d3748;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}

        .hair {{
            position: absolute;
            top: -8px;
            left: 50%;
            transform: translateX(-50%);
            width: 122px;
            height: 36px;
            background: #2b1d17;
            border-radius: 60px 60px 18px 18px;
        }}

        .eyebrow {{
            position: absolute;
            width: 22px;
            height: 5px;
            background: #2b1d17;
            border-radius: 3px;
            top: {eyebrow_top};
            transition: all 0.2s ease;
        }}

        .eyebrow.left {{ left: 24px; transform: rotate({eyebrow_left_rotate}); }}
        .eyebrow.right {{ right: 24px; transform: rotate({eyebrow_right_rotate}); }}

        .eye {{
            position: absolute;
            width: 10px;
            height: 10px;
            background: #111827;
            border-radius: 50%;
            top: 52px;
            transform: scale({eye_scale_x}, {eye_scale_y});
            transition: all 0.2s ease;
        }}

        .eye.left {{ left: 30px; }}
        .eye.right {{ right: 30px; }}

        .mouth {{
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            bottom: 16px;
            width: 58px;
            height: {mouth_height}px;
            background: {mouth_bg};
            border-radius: {mouth_radius};
            transition: all 0.15s ease;
        }}

        .body {{
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 96px;
            height: 86px;
            background: {accent_color};
            border-radius: 18px 18px 10px 10px;
            border: 4px solid #2d3748;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }}

        .caption {{
            margin-top: 14px;
            color: #f8fafc;
            font-size: 13px;
            text-align: center;
            opacity: 0.95;
            max-width: 280px;
            word-wrap: break-word;
            font-weight: 500;
        }}
    </style>

    <div class="avatar-shell">
        <div class="emotion-badge">
            <span>{emoji} {emotion}</span>
            <span style="opacity:0.75; font-size:10px;">| {int(intensity)}% int.</span>
        </div>
        <div class="avatar-wrap">
            <div class="avatar">
                <div class="head">
                    <div class="hair"></div>
                    <div class="eyebrow left"></div>
                    <div class="eyebrow right"></div>
                    <div class="eye left"></div>
                    <div class="eye right"></div>
                    <div class="mouth" id="avatar-mouth"></div>
                </div>
                <div class="body"></div>
            </div>
            <div class="caption">{safe_text[:120]}</div>
        </div>
    </div>

    <script>
        const mouth = document.getElementById('avatar-mouth');
        let step = 0;
        const baseH = {mouth_height};
        setInterval(() => {{
            const mod = ((Math.sin(step) + 1) * {4 + (intensity / 20.0)});
            mouth.style.height = (baseH + mod) + 'px';
            step += 0.45;
        }}, {int(anim_speed * 1000)});
    </script>
    """


# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------------------------------------------------------
# Modern Navigation Router & Views
# --------------------------------------------------------------------------
if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "🏠 Home"

db_df = load_sign_database(DB_PATH)

# Render Global Clean Sidebar
render_sidebar()

# Page routing map
current_page = st.session_state.get("nav_page", "🏠 Home")

PAGE_METADATA = {
    "🏠 Home": ("Welcome to SignBridge AI", "Make communication accessible with an intelligent 3D human avatar."),
    "⚡ Translate": ("Intelligent Translator", "Multilingual speech and text to Indian Sign Language with 3D human avatar."),
    "💬 Live Conversation": ("Live Conversation", "Communicate naturally in both directions with speech and signing."),
    "📷 SignVision": ("SignVision", "Real-time visual sign recognition powered by MediaPipe."),
    "🎓 Learn ISL": ("Learn Indian Sign Language", "Master everyday signs through guided practice and milestones."),
    "🚨 Emergency": ("Emergency Assist", "Essential communication when every second matters."),
    "🕘 History": ("Activity Timeline", "Chronological history of recent translations and interactions."),
    "⭐ Saved Phrases": ("Phrasebook", "Instant access and replay for essential saved phrases."),
    "📖 Sign Library": ("Sign Library", "Search and explore 500+ Indian Sign Language vocabulary concepts."),
    "♿ Accessibility": ("Accessibility Suite", "Customizable presentation and assistive controls."),
    "⚙️ Settings": ("System & Model Settings", "Configure speech recognition and diagnostics."),
}

title, subtitle = PAGE_METADATA.get(current_page, ("SignBridge AI", ""))
render_top_bar(title, subtitle)

if current_page == "🏠 Home":
    render_home_view()

elif current_page == "⚡ Translate":
    render_translator_view(
        transcribe_fn=transcribe_multilingual,
        translate_fn=translate_to_english,
        clean_tokens_fn=clean_tokens,
        words_to_signs_fn=words_to_signs,
        extract_audio_fn=extract_audio_from_uploaded_file,
        db_df=db_df,
        emotion_cache_fn=get_cached_emotion_model,
    )

elif current_page == "💬 Live Conversation":
    render_live_conversation_view()

elif current_page == "📷 SignVision":
    render_sign_to_speech_page()

elif current_page == "🎓 Learn ISL":
    render_learn_isl_view()

elif current_page == "🚨 Emergency":
    render_emergency_view()

elif current_page == "📖 Sign Library":
    render_sign_library_view(db_df)

elif current_page == "⭐ Saved Phrases":
    render_saved_phrases_view()

elif current_page == "🕘 History":
    render_history_view()

elif current_page == "♿ Accessibility":
    render_accessibility_view()

elif current_page == "⚙️ Settings":
    render_settings_view()
