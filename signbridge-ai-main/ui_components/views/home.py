"""
SignBridge AI — Modern Dashboard Home View
Hero presentation, system status, and 4 clean SaaS feature cards.
"""

import streamlit as st
from ui_components.styles import render_html


def render_home_view():
    """Renders the modern 2026 SaaS home hero and feature cards."""
    # Status Pill & Greeting
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
            <div style="font-size: 0.95rem; font-weight: 600; color: #64748B;">
                Good morning 👋
            </div>
            <div class="status-pill status-pill-online">
                <span style="width: 7px; height: 7px; border-radius: 50%; background: #10B981; display: inline-block;"></span>
                <span>AI system online</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hero Card
    st.markdown(
        """
        <div style="
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 20px;
            padding: 32px 36px;
            margin-bottom: 28px;
            box-shadow: 0 4px 20px rgba(15, 23, 42, 0.04);
            position: relative;
            overflow: hidden;
        ">
            <div style="position: absolute; right: -20px; top: -20px; width: 220px; height: 220px; background: radial-gradient(circle, rgba(91,92,235,0.06) 0%, transparent 70%); border-radius: 50%; pointer-events: none;"></div>
            <div style="max-width: 720px; position: relative; z-index: 1;">
                <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(91,92,235,0.08); padding: 4px 12px; border-radius: 999px; margin-bottom: 14px;">
                    <span style="font-size: 0.85rem;">🤟</span>
                    <span style="font-size: 0.76rem; font-weight: 700; color: #5B5CEB; letter-spacing: 0.05em; text-transform: uppercase;">Next-Gen Indian Sign Language AI</span>
                </div>
                <h1 style="margin: 0 0 10px 0; font-size: 2.2rem; font-weight: 800; color: #0F172A; letter-spacing: -0.03em; line-height: 1.18;">
                    Make communication accessible.
                </h1>
                <p style="margin: 0 0 24px 0; color: #64748B; font-size: 1.02rem; line-height: 1.55;">
                    Translate speech, text, and Indian Sign Language with an intelligent 3D human avatar. Two-way communication designed for clarity and empathy.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # CTA Buttons in hero
    btn_col1, btn_col2, _ = st.columns([1.2, 1.0, 2.8], gap="small")
    with btn_col1:
        if st.button("🚀 Start Conversation", type="primary", use_container_width=True):
            st.session_state["nav_page"] = "💬 Live Conversation"
            st.rerun()
    with btn_col2:
        if st.button("✨ Try Demo", type="secondary", use_container_width=True):
            st.session_state["demo_mode_active"] = True
            st.session_state["nav_page"] = "⚡ Translate"
            st.session_state["demo_preset_phrase"] = "Hello! Where is the hospital?"
            st.rerun()

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Section Title
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
            <h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #0F172A;">
                Core Capabilities
            </h3>
            <span style="font-size: 0.80rem; color: #64748B;">4 Intelligent Engines</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 4 Clean Feature Cards
    f1, f2, f3, f4 = st.columns(4, gap="medium")

    with f1:
        st.markdown(
            """
            <div class="feature-card">
                <div>
                    <div style="width: 44px; height: 44px; border-radius: 12px; background: rgba(91,92,235,0.08); display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-bottom: 14px;">
                        ⚡
                    </div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #0F172A; margin-bottom: 6px;">
                        Translate
                    </div>
                    <div style="font-size: 0.85rem; color: #64748B; line-height: 1.45;">
                        Speech / text → ISL with emotion analysis and 3D avatar animation.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Translator →", key="home_card_trans", use_container_width=True):
            st.session_state["nav_page"] = "⚡ Translate"
            st.rerun()

    with f2:
        st.markdown(
            """
            <div class="feature-card">
                <div>
                    <div style="width: 44px; height: 44px; border-radius: 12px; background: rgba(20,184,166,0.10); display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-bottom: 14px;">
                        💬
                    </div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #0F172A; margin-bottom: 6px;">
                        Live Conversation
                    </div>
                    <div style="font-size: 0.85rem; color: #64748B; line-height: 1.45;">
                        Two-way seamless communication stream between signing and speaking.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Start Live Chat →", key="home_card_live", use_container_width=True):
            st.session_state["nav_page"] = "💬 Live Conversation"
            st.rerun()

    with f3:
        st.markdown(
            """
            <div class="feature-card">
                <div>
                    <div style="width: 44px; height: 44px; border-radius: 12px; background: rgba(16,185,129,0.10); display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-bottom: 14px;">
                        📷
                    </div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #0F172A; margin-bottom: 6px;">
                        SignVision
                    </div>
                    <div style="font-size: 0.85rem; color: #64748B; line-height: 1.45;">
                        Real-time camera sign recognition with MediaPipe landmark tracking.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Launch Camera →", key="home_card_vision", use_container_width=True):
            st.session_state["nav_page"] = "📷 SignVision"
            st.rerun()

    with f4:
        st.markdown(
            """
            <div class="feature-card">
                <div>
                    <div style="width: 44px; height: 44px; border-radius: 12px; background: rgba(245,158,11,0.10); display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-bottom: 14px;">
                        🎓
                    </div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #0F172A; margin-bottom: 6px;">
                        Learn ISL
                    </div>
                    <div style="font-size: 0.85rem; color: #64748B; line-height: 1.45;">
                        Interactive lessons, daily practice streaks, and vocabulary expansion.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Practice Signs →", key="home_card_learn", use_container_width=True):
            st.session_state["nav_page"] = "🎓 Learn ISL"
            st.rerun()

    # Quick Emergency banner
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="
            background: #FEF2F2;
            border: 1px solid #FECACA;
            border-radius: 16px;
            padding: 16px 22px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
        ">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.4rem;">🚨</span>
                <div>
                    <div style="font-weight: 700; font-size: 0.95rem; color: #991B1B;">Emergency Assist Mode</div>
                    <div style="font-size: 0.82rem; color: #B91C1C;">One-touch high-contrast alerts and immediate spoken voice for medical and urgent scenarios.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Emergency Assist 🚨", key="home_emergency_cta", use_container_width=True):
        st.session_state["nav_page"] = "🚨 Emergency"
        st.rerun()
