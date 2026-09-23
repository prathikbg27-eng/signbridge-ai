"""
SignBridge AI — Learn ISL View
Gamified Indian Sign Language Learning: Goals, Streaks, XP, and Interactive Lesson Cards.
"""

import urllib.parse
import streamlit as st
from ui_components.styles import render_html
import streamlit.components.v1 as components

LESSONS = [
    {
        "id": "HELLO",
        "word": "HELLO",
        "emoji": "👋",
        "difficulty": "Beginner",
        "desc": "Open palm facing camera with fingers upright and spread, waving gently.",
        "xp": 50,
        "completed": True,
    },
    {
        "id": "THANK_YOU",
        "word": "THANK YOU",
        "emoji": "🤝",
        "difficulty": "Beginner",
        "desc": "Flat open hand touching chin, then moving forward towards the other person.",
        "xp": 50,
        "completed": True,
    },
    {
        "id": "PLEASE",
        "word": "PLEASE",
        "emoji": "🙏",
        "difficulty": "Beginner",
        "desc": "Open hand pressed against chest in a gentle circular clockwise motion.",
        "xp": 50,
        "completed": True,
    },
    {
        "id": "HELP",
        "word": "HELP",
        "emoji": "🆘",
        "difficulty": "Essential",
        "desc": "Closed fist with thumb up placed on top of flat palm, lifting upward.",
        "xp": 75,
        "completed": True,
    },
    {
        "id": "WATER",
        "word": "WATER",
        "emoji": "💧",
        "difficulty": "Beginner",
        "desc": "Index, middle, and ring fingers forming 'W' tapped gently against the chin.",
        "xp": 50,
        "completed": False,
    },
    {
        "id": "FAMILY",
        "word": "FAMILY",
        "emoji": "👨‍👩‍👧‍👦",
        "difficulty": "Intermediate",
        "desc": "Both hands forming 'F' shape starting together and circling outward.",
        "xp": 100,
        "completed": False,
    },
]


def render_learn_isl_view():
    """Renders the modern gamified ISL learning dashboard."""
    # Top Gamification Bar: Goal + Streak + XP
    g1, g2, g3 = st.columns([1.6, 1.0, 1.0], gap="medium")

    with g1:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 16px; padding: 18px 20px; box-shadow: 0 2px 8px rgba(15,23,42,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 0.88rem; font-weight: 700; color: #0F172A;">Today's Learning Goal</span>
                    <span style="font-size: 0.85rem; font-weight: 800; color: #5B5CEB;">4 / 5 signs completed</span>
                </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(0.80)
        st.markdown(
            """
                <div style="font-size: 0.74rem; color: #64748B; margin-top: 6px;">
                    Just 1 more sign today to maintain your streak!
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with g2:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 16px; padding: 18px 20px; box-shadow: 0 2px 8px rgba(15,23,42,0.03); text-align: center; height: 100%;">
                <div style="font-size: 1.6rem; margin-bottom: 2px;">🔥</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #D97706;">5 Days</div>
                <div style="font-size: 0.76rem; color: #64748B; font-weight: 600; text-transform: uppercase;">Active Streak</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with g3:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 16px; padding: 18px 20px; box-shadow: 0 2px 8px rgba(15,23,42,0.03); text-align: center; height: 100%;">
                <div style="font-size: 1.6rem; margin-bottom: 2px;">⭐</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #5B5CEB;">375 XP</div>
                <div style="font-size: 0.76rem; color: #64748B; font-weight: 600; text-transform: uppercase;">Total Experience</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Active Lesson Preview & Practice
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
            <h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #0F172A;">
                Recommended Lessons
            </h3>
            <span style="font-size: 0.80rem; color: #64748B;">Curated Curriculum</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Lesson Cards Grid (2 rows of 3 columns)
    row1 = st.columns(3, gap="medium")
    for i in range(3):
        lesson = LESSONS[i]
        with row1[i]:
            status_badge = '<span style="background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; font-size: 0.72rem; padding: 2px 8px; border-radius: 999px; font-weight: 700;">✓ Mastered</span>' if lesson["completed"] else '<span style="background: #F1F5F9; color: #475569; font-size: 0.72rem; padding: 2px 8px; border-radius: 999px; font-weight: 600;">In Progress</span>'
            st.markdown(
                f"""
                <div class="feature-card" style="margin-bottom: 14px;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <span style="font-size: 0.74rem; font-weight: 700; color: #5B5CEB; background: rgba(91,92,235,0.08); padding: 3px 8px; border-radius: 6px;">{lesson['difficulty']}</span>
                            {status_badge}
                        </div>
                        <div style="font-size: 1.4rem; margin-bottom: 6px;">{lesson['emoji']} <b style="font-size: 1.15rem; color: #0F172A;">{lesson['word']}</b></div>
                        <div style="font-size: 0.84rem; color: #64748B; line-height: 1.45; margin-bottom: 14px;">{lesson['desc']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button(f"Watch 3D", key=f"btn_watch_{lesson['id']}", use_container_width=True):
                    st.session_state["preview_lesson_sign"] = lesson["word"]
            with col_b2:
                if st.button(f"Practice 📷", key=f"btn_prac_{lesson['id']}", type="primary", use_container_width=True):
                    st.session_state["nav_page"] = "📷 SignVision"
                    st.rerun()

    row2 = st.columns(3, gap="medium")
    for i in range(3, 6):
        lesson = LESSONS[i]
        with row2[i - 3]:
            status_badge = '<span style="background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; font-size: 0.72rem; padding: 2px 8px; border-radius: 999px; font-weight: 700;">✓ Mastered</span>' if lesson["completed"] else '<span style="background: #F1F5F9; color: #475569; font-size: 0.72rem; padding: 2px 8px; border-radius: 999px; font-weight: 600;">In Progress</span>'
            st.markdown(
                f"""
                <div class="feature-card" style="margin-bottom: 14px;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <span style="font-size: 0.74rem; font-weight: 700; color: #5B5CEB; background: rgba(91,92,235,0.08); padding: 3px 8px; border-radius: 6px;">{lesson['difficulty']}</span>
                            {status_badge}
                        </div>
                        <div style="font-size: 1.4rem; margin-bottom: 6px;">{lesson['emoji']} <b style="font-size: 1.15rem; color: #0F172A;">{lesson['word']}</b></div>
                        <div style="font-size: 0.84rem; color: #64748B; line-height: 1.45; margin-bottom: 14px;">{lesson['desc']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button(f"Watch 3D", key=f"btn_watch_{lesson['id']}", use_container_width=True):
                    st.session_state["preview_lesson_sign"] = lesson["word"]
            with col_b2:
                if st.button(f"Practice 📷", key=f"btn_prac_{lesson['id']}", type="primary", use_container_width=True):
                    st.session_state["nav_page"] = "📷 SignVision"
                    st.rerun()

    # If Watch 3D clicked, render dynamic avatar preview
    preview_sign = st.session_state.get("preview_lesson_sign")
    if preview_sign:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 20px; padding: 20px; box-shadow: 0 4px 18px rgba(15,23,42,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="font-weight: 800; font-size: 1.15rem; color: #0F172A;">Interactive 3D Demo: {preview_sign}</div>
                    <span class="status-pill status-pill-primary">● 3D Avatar Ready</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        enc = urllib.parse.quote(preview_sign)
        components.iframe(f"https://ai-avatar-jade-zeta.vercel.app/?text={enc}&speed=0.10&pause=800", width=640, height=450)
