"""
SignBridge AI — Emergency Assist View
High-clarity, high-contrast accessible emergency interface with instant spoken audio & 3D avatar gestures.
"""

import urllib.parse
import streamlit as st
from ui_components.styles import render_html
import streamlit.components.v1 as components

EMERGENCY_ACTIONS = [
    {
        "id": "HELP",
        "title": "I NEED HELP",
        "subtitle": "Urgent personal assistance required",
        "icon": "🆘",
        "sign_text": "HELP",
        "audio_text": "I need help urgently, please assist me!",
        "bg": "#FEF2F2",
        "border": "#F87171",
        "text_color": "#991B1B",
    },
    {
        "id": "DOCTOR",
        "title": "I NEED A DOCTOR",
        "subtitle": "Medical emergency or physical illness",
        "icon": "🩺",
        "sign_text": "DOCTOR",
        "audio_text": "I need a doctor immediately.",
        "bg": "#EFF6FF",
        "border": "#60A5FA",
        "text_color": "#1E40AF",
    },
    {
        "id": "AMBULANCE",
        "title": "CALL AN AMBULANCE",
        "subtitle": "Severe trauma, critical emergency",
        "icon": "🚑",
        "sign_text": "AMBULANCE",
        "audio_text": "Please call an ambulance right now!",
        "bg": "#FFF1F2",
        "border": "#FB7185",
        "text_color": "#9F1239",
    },
    {
        "id": "MEDICINE",
        "title": "I NEED MEDICINE",
        "subtitle": "Prescription, insulin, or first-aid supplies",
        "icon": "💊",
        "sign_text": "MEDICINE",
        "audio_text": "I need urgent medicine or first aid.",
        "bg": "#F0FDF4",
        "border": "#4ADE80",
        "text_color": "#166534",
    },
    {
        "id": "DIRECTIONS",
        "title": "I NEED DIRECTIONS",
        "subtitle": "Lost or seeking nearest safe location",
        "icon": "📍",
        "sign_text": "WHERE HOSPITAL",
        "audio_text": "I am lost. Please give me directions to safety or the nearest hospital.",
        "bg": "#F8FAFC",
        "border": "#94A3B8",
        "text_color": "#1E293B",
    },
    {
        "id": "DANGER",
        "title": "I AM IN DANGER",
        "subtitle": "Threat to safety, security assistance needed",
        "icon": "⚠️",
        "sign_text": "DANGER HELP",
        "audio_text": "I am in danger! Please call the police immediately!",
        "bg": "#FEF2F2",
        "border": "#EF4444",
        "text_color": "#7F1D1D",
    },
]


def render_emergency_view():
    """Renders the high-accessibility emergency assist interface."""
    st.markdown(
        """
        <div style="background: #FFF1F2; border: 1px solid #FECDD3; border-radius: 16px; padding: 16px 20px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.5rem;">🚨</span>
                <div>
                    <div style="font-size: 1.05rem; font-weight: 800; color: #9F1239;">Emergency Assist Mode</div>
                    <div style="font-size: 0.84rem; color: #BE123C;">Click any emergency card below to broadcast loud spoken audio and project instant ISL sign gestures.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Active Emergency Display if triggered
    active_alert = st.session_state.get("active_emergency_alert")
    if active_alert:
        st.markdown(
            f"""
            <div style="
                background: #991B1B;
                color: #FFFFFF;
                border-radius: 18px;
                padding: 22px;
                margin-bottom: 24px;
                box-shadow: 0 6px 24px rgba(153, 27, 27, 0.35);
                text-align: center;
            ">
                <div style="font-size: 2rem; margin-bottom: 4px;">{active_alert['icon']}</div>
                <div style="font-size: 1.8rem; font-weight: 900; letter-spacing: -0.01em; margin-bottom: 6px;">
                    {active_alert['title']}
                </div>
                <div style="font-size: 1.10rem; opacity: 0.92; margin-bottom: 14px;">
                    "{active_alert['audio_text']}"
                </div>
                <div style="display: inline-block; background: rgba(255,255,255,0.20); padding: 4px 14px; border-radius: 999px; font-weight: 700; font-size: 0.85rem;">
                    Broadcasting Spoken Audio & 3D ISL Sign Sequence
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Trigger Speech Synthesis
        components.html(
            f"""
            <script>
                const utterance = new SpeechSynthesisUtterance("{active_alert['audio_text']}");
                utterance.rate = 0.95;
                utterance.volume = 1.0;
                window.speechSynthesis.speak(utterance);
            </script>
            """,
            height=0,
        )

        # 3D Avatar Signing
        enc_sign = urllib.parse.quote(active_alert["sign_text"])
        components.iframe(f"https://ai-avatar-jade-zeta.vercel.app/?text={enc_sign}&speed=0.10&pause=600&emotion=fear&intensity=90", width=640, height=450)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # 6 High-Contrast Accessible Cards (2 rows of 3)
    col1, col2, col3 = st.columns(3, gap="medium")
    cols = [col1, col2, col3]

    for idx, act in enumerate(EMERGENCY_ACTIONS):
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div style="
                    background: {act['bg']};
                    border: 2px solid {act['border']};
                    border-radius: 18px;
                    padding: 20px;
                    margin-bottom: 12px;
                    box-shadow: 0 2px 10px rgba(15,23,42,0.03);
                    min-height: 130px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                ">
                    <div>
                        <div style="font-size: 1.8rem; margin-bottom: 6px;">{act['icon']}</div>
                        <div style="font-size: 1.12rem; font-weight: 800; color: {act['text_color']}; margin-bottom: 4px;">
                            {act['title']}
                        </div>
                        <div style="font-size: 0.82rem; color: #64748B;">
                            {act['subtitle']}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"BROADCAST: {act['title']} 🚨", key=f"btn_em_{act['id']}", type="primary", use_container_width=True):
                st.session_state["active_emergency_alert"] = act
                st.rerun()
