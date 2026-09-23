"""
SignBridge AI — Shell Component
Renders the top navigation bar, sidebar navigation structure, and profile card.
"""

import streamlit as st
from ui_components.styles import render_html

NAV_ITEMS = [
    ("HOME", ["🏠 Home"]),
    ("WORKSPACE", [
        "⚡ Translate",
        "💬 Live Conversation",
        "📷 SignVision",
        "🎓 Learn ISL",
        "🚨 Emergency",
    ]),
    ("LIBRARY", [
        "🕘 History",
        "⭐ Saved Phrases",
        "📖 Sign Library",
    ]),
    ("SYSTEM", [
        "♿ Accessibility",
        "⚙️ Settings",
    ]),
]

ALL_PAGES = [
    "🏠 Home",
    "⚡ Translate",
    "💬 Live Conversation",
    "📷 SignVision",
    "🎓 Learn ISL",
    "🚨 Emergency",
    "🕘 History",
    "⭐ Saved Phrases",
    "📖 Sign Library",
    "♿ Accessibility",
    "⚙️ Settings",
]


def render_sidebar():
    """Renders the 2026 SaaS-styled clean sidebar with structured navigation."""
    with st.sidebar:
        # Header & Brand
        st.markdown(
            """
            <div style="padding: 6px 4px 16px 4px; margin-bottom: 12px; border-bottom: 1px solid #E5E7EB;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 38px; height: 38px; background: #5B5CEB; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; color: #FFFFFF; box-shadow: 0 4px 12px rgba(91,92,235,0.25);">
                        🤟
                    </div>
                    <div>
                        <div style="font-weight: 800; font-size: 1.12rem; color: #0F172A; letter-spacing: -0.02em; line-height: 1.2;">
                            SIGNBRIDGE <span style="color: #5B5CEB;">AI TEST</span>
                        </div>
                        <div style="font-size: 0.74rem; color: #64748B; font-weight: 500;">
                            Speak. Sign. Understand.
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        current_page = st.session_state.get("nav_page", "🏠 Home")
        if current_page not in ALL_PAGES:
            current_page = "🏠 Home"

        # Modern Nav Groups
        for section_title, pages in NAV_ITEMS:
            st.markdown(
                f"""
                <div style="font-size: 0.70rem; font-weight: 700; color: #94A3B8; letter-spacing: 0.08em; text-transform: uppercase; margin: 14px 4px 6px 4px;">
                    {section_title}
                </div>
                """,
                unsafe_allow_html=True,
            )
            for page in pages:
                is_active = (current_page == page)
                btn_type = "primary" if is_active else "secondary"
                if st.button(page, key=f"nav_btn_{page}", type=btn_type, use_container_width=True):
                    st.session_state["nav_page"] = page
                    st.rerun()

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.divider()

        # Bottom Profile Card
        st.markdown(
            """
            <div style="
                background: #F8FAFC;
                border: 1px solid #E5E7EB;
                border-radius: 14px;
                padding: 12px 14px;
                display: flex;
                align-items: center;
                gap: 10px;
                margin-top: 8px;
            ">
                <div style="width: 36px; height: 36px; background: #EEF2FF; border: 1px solid #C7D2FE; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1rem;">
                    👤
                </div>
                <div style="flex: 1; min-width: 0;">
                    <div style="font-size: 0.84rem; font-weight: 700; color: #0F172A; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        Hackathon Team
                    </div>
                    <div style="display: flex; align-items: center; gap: 5px; margin-top: 1px;">
                        <span style="width: 6px; height: 6px; border-radius: 50%; background: #10B981; display: inline-block;"></span>
                        <span style="font-size: 0.72rem; color: #64748B; font-weight: 500;">System online</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_top_bar(page_title: str, page_subtitle: str = ""):
    """Renders the modern sticky-feel top product bar with controls."""
    col_left, col_right = st.columns([1.6, 1.2], gap="medium")

    with col_left:
        st.markdown(
            f"""
            <div style="margin-bottom: 14px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 2px;">
                    <span style="font-size: 0.76rem; font-weight: 700; color: #5B5CEB; letter-spacing: 0.06em; text-transform: uppercase;">
                        SIGNBRIDGE AI TEST
                    </span>
                    <span style="color: #CBD5E1;">•</span>
                    <span style="font-size: 0.76rem; color: #64748B;">Accessibility Platform</span>
                </div>
                <h1 style="margin: 0; font-size: 1.65rem; font-weight: 800; color: #0F172A; letter-spacing: -0.025em; line-height: 1.2;">
                    {page_title}
                </h1>
                {f'<p style="margin: 3px 0 0 0; color: #64748B; font-size: 0.88rem;">{page_subtitle}</p>' if page_subtitle else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        # Top right utilities
        c1, c2, c3 = st.columns([1.1, 1.0, 1.0], gap="small")
        with c1:
            lang_choice = st.selectbox(
                "Language",
                ["Auto Detect", "English", "Hindi", "Gujarati", "Kannada", "Tamil", "Telugu"],
                key="topbar_language",
                label_visibility="collapsed",
            )
            st.session_state["selected_language"] = lang_choice

        with c2:
            is_demo = st.session_state.get("demo_mode_active", False)
            demo_label = "● Demo Active" if is_demo else "✨ Demo Mode"
            demo_type = "primary" if is_demo else "secondary"
            if st.button(demo_label, key="btn_toggle_demo", type=demo_type, use_container_width=True):
                st.session_state["demo_mode_active"] = not is_demo
                st.rerun()

        with c3:
            if st.button("♿ Access", key="btn_quick_access", type="secondary", use_container_width=True):
                st.session_state["nav_page"] = "♿ Accessibility"
                st.rerun()

    st.markdown("<hr style='border: none; border-top: 1px solid #E5E7EB; margin: 4px 0 20px 0;' />", unsafe_allow_html=True)
