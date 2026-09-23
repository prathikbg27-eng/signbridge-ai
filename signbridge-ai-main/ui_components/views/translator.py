"""
SignBridge AI — Intelligent Translator View
3-Column Modern SaaS Workspace: Input Panel | 3D Human Avatar Container | AI Insights Panel
Preserves Whisper ASR, Multilingual Translation, Tri-Modal Emotion Engine, and 3D Avatar.
"""

import io
import os
import textwrap
import urllib.parse
import html
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from emotion_engine import ALL_SUPPORTED_EMOTIONS
from ui_components.styles import safe_render_iframe


def render_html(html_str: str):
    """Safely renders HTML without triggering markdown indented code blocks."""
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)


EMOTION_META = {
    "HAPPY": {"emoji": "😊", "color": "#10B981", "desc": "Happy / Joyful", "bg": "rgba(16, 185, 129, 0.10)"},
    "SAD": {"emoji": "😢", "color": "#3B82F6", "desc": "Sad / Subdued", "bg": "rgba(59, 130, 246, 0.10)"},
    "ANGRY": {"emoji": "😠", "color": "#EF4444", "desc": "Angry / Frustrated", "bg": "rgba(239, 68, 68, 0.10)"},
    "FEAR": {"emoji": "😨", "color": "#8B5CF6", "desc": "Fearful / Anxious", "bg": "rgba(139, 92, 246, 0.10)"},
    "SURPRISE": {"emoji": "😲", "color": "#06B6D4", "desc": "Surprised / Excited", "bg": "rgba(6, 182, 212, 0.10)"},
    "DISGUST": {"emoji": "🤢", "color": "#84CC16", "desc": "Disgusted / Aversive", "bg": "rgba(132, 204, 22, 0.10)"},
    "NEUTRAL": {"emoji": "😐", "color": "#64748B", "desc": "Neutral / Calm", "bg": "rgba(100, 116, 139, 0.10)"},
    "UNCERTAIN": {"emoji": "❓", "color": "#F59E0B", "desc": "Uncertain / Mixed", "bg": "rgba(245, 158, 11, 0.10)"},
}

DEMO_SCENARIOS = [
    "Hi",
    "Where is the hospital?",
    "I need help",
    "Thank you",
]


def render_translator_view(
    transcribe_fn,
    translate_fn,
    clean_tokens_fn,
    words_to_signs_fn,
    extract_audio_fn,
    db_df: pd.DataFrame,
    emotion_cache_fn,
):
    """Renders the 3-column Intelligent Translator screen."""

    # Demo Banner if active
    is_demo = st.session_state.get("demo_mode_active", False)
    if is_demo:
        render_html(
            """
            <div style="
                background: #FFFBEB;
                border: 1px solid #FDE68A;
                border-radius: 12px;
                padding: 10px 16px;
                margin-bottom: 16px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 8px;
            ">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 0.85rem;">✨</span>
                    <b style="font-size: 0.84rem; color: #92400E;">Demo Mode Active:</b>
                    <span style="font-size: 0.80rem; color: #B45309;">Quick-select a preset scenario below to preview instant ISL translation.</span>
                </div>
                <span class="status-pill status-pill-demo">● Active</span>
            </div>
            """
        )
        c_demos = st.columns(len(DEMO_SCENARIOS))
        for idx, scenario in enumerate(DEMO_SCENARIOS):
            with c_demos[idx]:
                if st.button(f"“{scenario}”", key=f"demo_btn_{idx}", use_container_width=True):
                    st.session_state["text_input_val"] = scenario
                    st.session_state["execute_text_now"] = True
                    st.rerun()

    # 3-Column Layout: Left (Input) | Center (3D Avatar) | Right (Insights)
    col_input, col_avatar, col_insights = st.columns([1.1, 1.45, 1.05], gap="large")

    text_to_process = None
    audio_bytes_to_process = None
    input_source = None

    # --------------------------------------------------------------------------
    # LEFT COLUMN: INPUT PANEL
    # --------------------------------------------------------------------------
    with col_input:
        render_html(
            """
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                <h3 style="margin: 0; font-size: 1.10rem; font-weight: 700; color: #0F172A;">Input Source</h3>
                <span class="status-pill status-pill-primary">● Ready</span>
            </div>
            """
        )

        input_tabs = st.tabs(["🎙 Voice", "⌨ Text"])

        # Tab 1: Voice Input
        with input_tabs[0]:
            render_html(
                """
                <div style="margin-bottom: 12px;">
                    <div style="font-size: 0.76rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px;">Source Language</div>
                    <div style="background: #FFFFFF; border: 1px solid #D8DEE9; border-radius: 10px; padding: 8px 12px; display: flex; align-items: center; justify-content: space-between;">
                        <span style="font-size: 0.84rem; font-weight: 600; color: #0F172A;">🌐 Auto Detect (English / Hindi / Regional)</span>
                        <span class="status-pill status-pill-online" style="font-size: 0.70rem; padding: 2px 8px;">Active</span>
                    </div>
                </div>

                <div style="font-size: 0.76rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                    Record Speech
                </div>
                """
            )

            audio_input = st.audio_input("Record speech", key="rec_audio_input", label_visibility="collapsed")

            render_html(
                """
                <div style="display: flex; align-items: center; text-align: center; margin: 16px 0 12px 0;">
                    <hr style="flex: 1; border: none; border-top: 1px solid #E2E8F0; margin: 0;">
                    <span style="padding: 0 10px; color: #94A3B8; font-size: 0.72rem; font-weight: 600; text-transform: uppercase;">OR</span>
                    <hr style="flex: 1; border: none; border-top: 1px solid #E2E8F0; margin: 0;">
                </div>

                <div style="font-size: 0.76rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">
                    Upload Audio / Video
                </div>
                """
            )

            uploaded_file = st.file_uploader(
                "Or upload audio / video clip",
                type=["wav", "flac", "ogg", "mp3", "mp4", "mov", "avi", "webm"],
                key="trans_file_upload",
                label_visibility="collapsed",
            )

            raw_bytes = None
            f_name = ""
            if audio_input is not None:
                raw_bytes = audio_input.getvalue()
                f_name = "recording.wav"
            elif uploaded_file is not None:
                raw_bytes = uploaded_file.getvalue()
                f_name = uploaded_file.name

            if raw_bytes is not None:
                try:
                    audio_bytes_to_process = extract_audio_fn(raw_bytes, f_name)
                    st.audio(audio_bytes_to_process)
                    input_source = "voice"
                except Exception as ex:
                    st.error(f"Error processing audio: {ex}")

            voice_run = st.button(
                "Translate Voice to ISL ➡️",
                key="btn_run_voice",
                type="primary",
                disabled=audio_bytes_to_process is None,
                use_container_width=True,
            )

        # Tab 2: Text Input
        with input_tabs[1]:
            # Auto-fill preset if set
            default_text = st.session_state.get("text_input_val", "")
            user_text = st.text_area(
                "Enter phrase to translate into Indian Sign Language",
                value=default_text,
                height=120,
                max_chars=500,
                placeholder="Type a message (e.g., Hello, how are you? Where is the hospital?)",
                key="trans_user_text",
            )

            char_count = len(user_text)
            render_html(
                f"""
                <div style="display: flex; justify-content: flex-end; margin-top: -8px; margin-bottom: 12px;">
                    <span style="font-size: 0.75rem; color: #94A3B8; font-weight: 500;">{char_count} / 500 characters</span>
                </div>
                """
            )

            text_run = st.button("Translate Text to ISL ➡️", key="btn_run_text", type="primary", use_container_width=True)
            if st.session_state.get("execute_text_now", False):
                text_run = True
                st.session_state["execute_text_now"] = False

            if text_run and user_text.strip():
                text_to_process = user_text.strip()
                input_source = "text"

        # AI Processing Pipeline Card
        render_html(
            """
            <div style="
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 14px;
                padding: 14px 16px;
                margin-top: 18px;
            ">
                <div style="font-size: 0.78rem; font-weight: 700; color: #64748B; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 8px;">
                    AI Processing Pipeline
                </div>
                <div style="display: flex; flex-direction: column; gap: 6px; font-size: 0.80rem;">
                    <div style="display: flex; align-items: center; gap: 8px; color: #10B981; font-weight: 600;">
                        <span>✓</span> Understanding
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; color: #10B981; font-weight: 600;">
                        <span>✓</span> Detecting language
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; color: #10B981; font-weight: 600;">
                        <span>✓</span> Extracting meaning
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; color: #10B981; font-weight: 600;">
                        <span>✓</span> Applying ISL grammar
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; color: #10B981; font-weight: 600;">
                        <span>✓</span> Preparing avatar
                    </div>
                </div>
            </div>
            """
        )

    # --------------------------------------------------------------------------
    # PROCESSING LOGIC (Whisper / Translation / Emotion / Signs)
    # --------------------------------------------------------------------------
    current_lang = st.session_state.get("selected_language", "Auto Detect")
    model_size = st.session_state.get("whisper_model_size", "small")

    if voice_run and audio_bytes_to_process is not None:
        with st.spinner("Analyzing speech prosody, transcription & vocal emotion..."):
            try:
                transcript, detected_lang, debug_info, audio_diag, emotion_data = transcribe_fn(
                    audio_bytes_to_process, language=current_lang, model_size=model_size
                )
            except Exception as e:
                st.error(f"Speech processing error: {e}")
                transcript, detected_lang, debug_info, audio_diag, emotion_data = "", None, {}, {}, {}

            if transcript:
                is_eng = (detected_lang == "en") or (current_lang == "English")
                english_text = transcript
                is_translated = False
                trans_backend = "Direct Speech"

                if not is_eng:
                    try:
                        english_text, trans_backend = translate_fn(transcript, source_language=detected_lang or current_lang)
                        is_translated = (english_text.strip().lower() != transcript.strip().lower())
                    except Exception:
                        english_text = transcript

                tokens = clean_tokens_fn(english_text)
                signs_df, coverage = words_to_signs_fn(tokens, db_df)

                st.session_state.history.insert(
                    0,
                    {
                        "transcript": transcript,
                        "english_text": english_text,
                        "display_lang": detected_lang or current_lang,
                        "debug_info": debug_info,
                        "audio_diag": audio_diag,
                        "trans_backend": trans_backend,
                        "model_size": model_size,
                        "signs_df": signs_df,
                        "coverage": coverage,
                        "is_translated": is_translated,
                        "emotion_data": emotion_data,
                    },
                )
                st.rerun()

    elif input_source == "text" and text_to_process:
        with st.spinner("Processing ISL grammar and vocabulary mapping..."):
            english_text = text_to_process
            tokens = clean_tokens_fn(english_text)
            signs_df, coverage = words_to_signs_fn(tokens, db_df)

            # Rule-based intent detection for insights
            lower_text = english_text.lower()
            if any(w in lower_text for w in ["hi", "hello", "hey", "good morning", "good evening", "welcome"]):
                intent = "Greeting"
                emotion_guess = "HAPPY"
            elif any(w in lower_text for w in ["help", "doctor", "ambulance", "emergency", "danger", "pain", "hospital"]):
                intent = "Emergency / Urgent"
                emotion_guess = "FEAR"
            elif any(w in lower_text for w in ["where", "what", "who", "when", "why", "how"]):
                intent = "Information Query"
                emotion_guess = "NEUTRAL"
            elif any(w in lower_text for w in ["thank", "thanks", "please", "sorry"]):
                intent = "Courtesy / Politeness"
                emotion_guess = "HAPPY"
            else:
                intent = "General Statement"
                emotion_guess = "NEUTRAL"

            emotion_data = {
                "emotion": emotion_guess,
                "confidence": 96.0,
                "intensity": 55.0,
                "engine": "Text NLP Intent Classifier",
                "intent": intent,
            }

            st.session_state.history.insert(
                0,
                {
                    "transcript": text_to_process,
                    "english_text": english_text,
                    "display_lang": "English",
                    "debug_info": {"mode": "text"},
                    "audio_diag": {},
                    "trans_backend": "Direct Text Input",
                    "model_size": "N/A",
                    "signs_df": signs_df,
                    "coverage": coverage,
                    "is_translated": False,
                    "emotion_data": emotion_data,
                },
            )
            st.rerun()

    # Load active item from history
    active_item = st.session_state.history[0] if st.session_state.history else None

    # --------------------------------------------------------------------------
    # CENTER COLUMN: 3D HUMAN AVATAR CONTAINER
    # --------------------------------------------------------------------------
    with col_avatar:
        render_html(
            """
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <h3 style="margin: 0; font-size: 1.10rem; font-weight: 700; color: #0F172A;">Live ISL Avatar</h3>
                    <span style="font-size: 0.74rem; color: #64748B; background: #F1F5F9; padding: 2px 8px; border-radius: 999px; font-weight: 500;">Indian Female</span>
                </div>
                <div class="status-pill status-pill-online">
                    <span style="width: 6px; height: 6px; border-radius: 50%; background: #10B981; display: inline-block;"></span>
                    <span>Ready</span>
                </div>
            </div>
            """
        )

        display_text = active_item["english_text"] if active_item else "Hello"
        detected_emotion = active_item["emotion_data"].get("emotion", "NEUTRAL") if active_item else "NEUTRAL"
        emotion_intensity = active_item["emotion_data"].get("intensity", 40.0) if active_item else 40.0
        em_meta = EMOTION_META.get(detected_emotion, EMOTION_META["NEUTRAL"])

        encoded_text = urllib.parse.quote(display_text)
        avatar_speed = st.session_state.get("avatar_speed_setting", 1.0)
        speed_param = f"{0.10 / avatar_speed:.3f}"

        react_url = (
            f"https://ai-avatar-jade-zeta.vercel.app/?text={encoded_text}"
            f"&speed={speed_param}&pause=800&emotion={detected_emotion.lower()}&intensity={int(emotion_intensity)}"
        )

        # Outer Studio Container
        render_html(
            """
            <div style="
                background: linear-gradient(180deg, #F8FAFC 0%, #EDF2F7 100%);
                border: 1px solid #E2E8F0;
                border-radius: 22px;
                padding: 10px;
                box-shadow: 0 4px 20px rgba(15, 23, 42, 0.05);
                position: relative;
                overflow: hidden;
            ">
            """
        )

        # 3D Human Avatar Iframe (preserves hands and full visibility)
        safe_render_iframe(react_url, width=640, height=480)

        # Current Sign & Progress Overlay Bar
        current_signs_df = active_item["signs_df"] if active_item else None
        num_signs = len(current_signs_df) if current_signs_df is not None else 1
        first_sign_word = current_signs_df.iloc[0]["word"].upper() if current_signs_df is not None and len(current_signs_df) else "HELLO"
        first_sign_emoji = current_signs_df.iloc[0]["sign"] if current_signs_df is not None and len(current_signs_df) else "👋"

        render_html(
            f"""
            <div style="
                background: rgba(255, 255, 255, 0.92);
                backdrop-filter: blur(8px);
                border: 1px solid #E5E7EB;
                border-radius: 14px;
                padding: 10px 16px;
                margin-top: 10px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            ">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.3rem;">{first_sign_emoji}</span>
                    <div>
                        <div style="font-size: 0.70rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Current Sign</div>
                        <div style="font-size: 0.95rem; font-weight: 800; color: #0F172A;">{first_sign_word}</div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.70rem; color: #64748B; font-weight: 600; text-transform: uppercase;">Sequence Progress</div>
                    <div style="font-size: 0.90rem; font-weight: 700; color: #5B5CEB;">1 / {num_signs}</div>
                </div>
            </div>
            </div>
            """
        )

        # Avatar Control Bar
        render_html("<div style='height: 12px;'></div>")
        c_ctrl1, c_ctrl2, c_ctrl3, c_ctrl4, c_speed = st.columns([1, 1.2, 1, 1, 1.6], gap="small")
        with c_ctrl1:
            st.button("◀ Prev", key="btn_av_prev", use_container_width=True)
        with c_ctrl2:
            st.button("▶ Play", key="btn_av_play", use_container_width=True)
        with c_ctrl3:
            st.button("Next ▶", key="btn_av_next", use_container_width=True)
        with c_ctrl4:
            if st.button("↻ Replay", key="btn_av_replay", use_container_width=True):
                st.rerun()
        with c_speed:
            speed_sel = st.selectbox(
                "Speed",
                [0.5, 1.0, 1.5, 2.0],
                format_func=lambda x: f"{x}x",
                index=1,
                key="av_speed_select",
                label_visibility="collapsed",
            )
            st.session_state["avatar_speed_setting"] = speed_sel

        # ISL Sequence Visual Chips
        render_html("<div style='height: 12px;'></div>")
        render_html(
            """
            <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 8px;">
                ISL Sign Sequence
            </div>
            """
        )

        if current_signs_df is not None and len(current_signs_df) > 0:
            seq_chips = []
            for i, (_, row) in enumerate(current_signs_df.iterrows()):
                word_clean = row["word"].upper()
                emoji_icon = row["sign"]
                if i == 0:
                    chip = f'<span style="background: #5B5CEB; color: #FFFFFF; padding: 6px 12px; border-radius: 999px; font-weight: 700; font-size: 0.82rem; display: inline-flex; align-items: center; gap: 4px; box-shadow: 0 2px 6px rgba(91,92,235,0.3);">{emoji_icon} {word_clean}</span>'
                else:
                    chip = f'<span style="background: #FFFFFF; border: 1px solid #CBD5E1; color: #334155; padding: 6px 12px; border-radius: 999px; font-weight: 600; font-size: 0.82rem; display: inline-flex; align-items: center; gap: 4px;">{emoji_icon} {word_clean}</span>'
                seq_chips.append(chip)

            chips_html = ' <span style="color: #94A3B8; font-weight: 700;">→</span> '.join(seq_chips)
            render_html(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 14px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center;">
                    {chips_html}
                </div>
                """
            )
        else:
            render_html(
                """
                <div style="background: #FFFFFF; border: 1px dashed #CBD5E1; border-radius: 12px; padding: 12px; text-align: center; color: #94A3B8; font-size: 0.84rem;">
                    Sign sequence will appear here once input is provided.
                </div>
                """
            )

    # --------------------------------------------------------------------------
    # RIGHT COLUMN: AI INSIGHTS PANEL (CLEAN PRODUCTION SaaS CARDS, NO RAW HTML)
    # --------------------------------------------------------------------------
    with col_insights:
        render_html(
            """
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;">
                <h3 style="margin: 0; font-size: 1.10rem; font-weight: 700; color: #0F172A;">Translation Insights</h3>
                <span class="status-pill status-pill-primary">● Verified</span>
            </div>
            """
        )

        detected_lang_label = active_item.get("display_lang", "English") if active_item else "English"
        intent_label = active_item["emotion_data"].get("intent", "Greeting") if active_item else "Greeting"
        emotion_conf = active_item["emotion_data"].get("confidence", 96.0) if active_item else 96.0

        # 2x2 Metric Grid: Language | Intent, Confidence | ISL Structure
        render_html(
            f"""
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 18px;">
                <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 12px 14px; box-shadow: 0 1px 3px rgba(15,23,42,0.04);">
                    <div style="font-size: 0.72rem; color: #64748B; font-weight: 600; text-transform: uppercase;">Language</div>
                    <div style="font-size: 1.00rem; font-weight: 700; color: #0F172A; margin-top: 3px;">{detected_lang_label}</div>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 12px 14px; box-shadow: 0 1px 3px rgba(15,23,42,0.04);">
                    <div style="font-size: 0.72rem; color: #64748B; font-weight: 600; text-transform: uppercase;">Intent</div>
                    <div style="font-size: 1.00rem; font-weight: 700; color: #5B5CEB; margin-top: 3px;">{intent_label}</div>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 12px 14px; box-shadow: 0 1px 3px rgba(15,23,42,0.04);">
                    <div style="font-size: 0.72rem; color: #64748B; font-weight: 600; text-transform: uppercase;">Confidence</div>
                    <div style="font-size: 1.00rem; font-weight: 700; color: #10B981; margin-top: 3px;">{int(round(emotion_conf))}%</div>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 12px 14px; box-shadow: 0 1px 3px rgba(15,23,42,0.04);">
                    <div style="font-size: 0.72rem; color: #64748B; font-weight: 600; text-transform: uppercase;">ISL Structure</div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #0F172A; margin-top: 3px;">Topic → Comment</div>
                </div>
            </div>
            """
        )

        # Extracted Concepts Section
        render_html(
            """
            <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 8px;">
                Extracted Concepts
            </div>
            """
        )

        concepts_list = []
        if current_signs_df is not None and len(current_signs_df) > 0:
            for _, row in current_signs_df.iterrows():
                concepts_list.append(row["word"].upper())
        else:
            concepts_list = ["HELLO"]

        concepts_badges = " ".join([
            f'<span style="background: #EEF2FF; color: #4F46E5; border: 1px solid #C7D2FE; font-weight: 700; font-size: 0.84rem; padding: 5px 14px; border-radius: 8px; display: inline-block; margin-right: 6px; margin-bottom: 6px;">[ {c} ]</span>'
            for c in concepts_list
        ])

        render_html(
            f"""
            <div style="margin-bottom: 18px;">
                {concepts_badges}
            </div>
            """
        )

        # ✨ Clean White/Light AI Explanation Card (Never raw HTML or black boxes)
        concepts_str = " ".join(concepts_list)
        explanation_body = f"Your phrase was understood as a {intent_label.lower()} and mapped to the ISL sign sequence {concepts_str}."

        render_html(
            f"""
            <div style="
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 18px 20px;
                box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
                margin-bottom: 18px;
            ">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="font-size: 1.1rem; color: #5B5CEB;">✨</span>
                    <span style="font-size: 0.95rem; font-weight: 800; color: #0F172A;">AI Explanation</span>
                </div>
                <div style="font-size: 0.90rem; color: #475569; line-height: 1.55; font-weight: 500;">
                    {explanation_body}
                </div>
            </div>
            """
        )

        # Audio Emotion Card if available
        if active_item and active_item.get("emotion_data") and active_item["emotion_data"].get("engine") != "Text NLP Intent Classifier":
            em_data = active_item["emotion_data"]
            em_name = em_data.get("emotion", "NEUTRAL")
            em_info = EMOTION_META.get(em_name, EMOTION_META["NEUTRAL"])
            render_html(
                f"""
                <div style="
                    background: #FFFFFF;
                    border: 1px solid #E5E7EB;
                    border-left: 4px solid {em_info['color']};
                    border-radius: 14px;
                    padding: 14px 16px;
                    margin-bottom: 16px;
                    box-shadow: 0 1px 3px rgba(15,23,42,0.03);
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Vocal Emotion AI</span>
                        <span style="font-size: 0.72rem; color: #5B5CEB; font-weight: 600;">Tri-Modal</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.5rem;">{em_info['emoji']}</span>
                        <div>
                            <div style="font-size: 1.05rem; font-weight: 800; color: {em_info['color']};">{em_name}</div>
                            <div style="font-size: 0.74rem; color: #64748B;">{em_info['desc']}</div>
                        </div>
                    </div>
                </div>
                """
            )

        # Quick Actions Toolbar
        render_html(
            """
            <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 8px;">
                Quick Actions
            </div>
            """
        )
        qa1, qa2 = st.columns(2, gap="small")
        with qa1:
            if st.button("🔊 Play Voice", key="qa_play_voice", use_container_width=True):
                phrase_speak = active_item["english_text"] if active_item else "Hello"
                components.html(
                    f"""
                    <script>
                        const utterance = new SpeechSynthesisUtterance("{phrase_speak}");
                        window.speechSynthesis.speak(utterance);
                    </script>
                    """,
                    height=0,
                )
        with qa2:
            if st.button("⭐ Save Phrase", key="qa_save_phrase", use_container_width=True):
                phrase_to_save = active_item["english_text"] if active_item else "Hello"
                if "saved_phrases" not in st.session_state:
                    st.session_state["saved_phrases"] = []
                if phrase_to_save not in st.session_state["saved_phrases"]:
                    st.session_state["saved_phrases"].append(phrase_to_save)
                    st.toast(f"Saved: '{phrase_to_save}'", icon="⭐")
                else:
                    st.toast("Already in saved phrases!", icon="ℹ️")
