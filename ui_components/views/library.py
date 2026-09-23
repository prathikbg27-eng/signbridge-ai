"""
SignBridge AI — Library Views
Contains: Sign Library (Searchable Categorical Directory), Saved Phrases (Phrasebook with Replay), and History Timeline.
"""

import urllib.parse
import pandas as pd
import streamlit as st
from ui_components.styles import render_html
import streamlit.components.v1 as components

DEFAULT_SAVED = [
    "Hi",
    "Where is the hospital?",
    "I need help",
    "Thank you",
    "I need water",
]

LIBRARY_CATEGORIES = [
    "All",
    "Basic",
    "Health",
    "Education",
    "Daily",
    "Travel",
    "Emergency",
    "Actions",
    "People",
]


def render_sign_library_view(db_df: pd.DataFrame):
    """Renders the searchable, category-filtered Sign Library."""
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
            <div>
                <div style="font-size: 0.82rem; font-weight: 700; color: #5B5CEB; text-transform: uppercase; letter-spacing: 0.05em;">VOCABULARY DIRECTORY</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #0F172A;">500+ Indian Sign Language Concept Base</div>
            </div>
            <span class="status-pill status-pill-primary">Indexed & Verified</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Search and Filter
    c_srch, c_cat = st.columns([1.8, 1.2], gap="medium")
    with c_srch:
        search_query = st.text_input("🔍 Search vocabulary...", placeholder="Type word (e.g., hello, water, help, doctor)...", key="lib_search")
    with c_cat:
        selected_cat = st.selectbox("Category Filter", LIBRARY_CATEGORIES, key="lib_cat_filter")

    # Filter dataframe
    filtered_df = db_df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df["word"].str.contains(search_query.lower().strip(), na=False)]
    if selected_cat != "All":
        filtered_df = filtered_df[filtered_df["category"].str.lower() == selected_cat.lower()]

    st.markdown(
        f"""
        <div style="font-size: 0.82rem; color: #64748B; margin-bottom: 16px;">
            Showing <b>{len(filtered_df)}</b> available sign concepts
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Preview dialog / container if user selected one
    active_preview = st.session_state.get("active_library_sign_preview")
    if active_preview:
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 18px; padding: 20px; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(15,23,42,0.06);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="font-size: 1.15rem; font-weight: 800; color: #0F172A;">Sign Animation Preview: {active_preview.upper()}</div>
                    <span class="status-pill status-pill-online">● 3D Human Avatar</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        enc_word = urllib.parse.quote(active_preview)
        components.iframe(f"https://ai-avatar-jade-zeta.vercel.app/?text={enc_word}&speed=0.10&pause=800", width=640, height=440)

    # Render Cards (Paginated / Grid of 12 items for high performance)
    page_size = 12
    total_pages = max(1, (len(filtered_df) + page_size - 1) // page_size)
    page_num = st.number_input(f"Page (1 to {total_pages})", min_value=1, max_value=total_pages, value=1, step=1, key="lib_page_nav")
    start_idx = (page_num - 1) * page_size
    current_page_df = filtered_df.iloc[start_idx : start_idx + page_size]

    if len(current_page_df) == 0:
        st.info("No matching sign concepts found. Try another search term.")
    else:
        grid_cols = st.columns(3, gap="medium")
        for idx, (_, row) in enumerate(current_page_df.iterrows()):
            with grid_cols[idx % 3]:
                word_cap = row["word"].title()
                emoji_icon = row["sign"]
                cat_name = row["category"].title()

                st.markdown(
                    f"""
                    <div class="feature-card" style="margin-bottom: 12px;">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="font-size: 0.72rem; font-weight: 700; color: #5B5CEB; background: rgba(91,92,235,0.08); padding: 2px 8px; border-radius: 6px;">{cat_name}</span>
                                <span style="font-size: 0.72rem; color: #10B981; font-weight: 600;">✓ Animated</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                                <span style="font-size: 1.5rem;">{emoji_icon}</span>
                                <span style="font-size: 1.10rem; font-weight: 700; color: #0F172A;">{word_cap}</span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    if st.button("Preview 3D", key=f"btn_prev_{row['word']}", use_container_width=True):
                        st.session_state["active_library_sign_preview"] = row["word"]
                        st.rerun()
                with c_btn2:
                    if st.button("Practice 📷", key=f"btn_prac_lib_{row['word']}", type="secondary", use_container_width=True):
                        st.session_state["nav_page"] = "📷 SignVision"
                        st.rerun()


def render_saved_phrases_view():
    """Renders the Saved Phrases phrasebook."""
    if "saved_phrases" not in st.session_state:
        st.session_state["saved_phrases"] = list(DEFAULT_SAVED)

    saved_list = st.session_state["saved_phrases"]

    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
            <div>
                <div style="font-size: 0.82rem; font-weight: 700; color: #5B5CEB; text-transform: uppercase;">QUICK ACCESS PHRASEBOOK</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #0F172A;">Starred & Essential Phrases</div>
            </div>
            <span class="status-pill status-pill-primary">Instant Replay</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Active replay player
    replay_phrase = st.session_state.get("active_saved_replay")
    if replay_phrase:
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 18px; padding: 20px; margin-bottom: 24px; box-shadow: 0 4px 18px rgba(15,23,42,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div style="font-size: 1.15rem; font-weight: 800; color: #0F172A;">Replaying: "{replay_phrase}"</div>
                    <span class="status-pill status-pill-online">● 3D Avatar Signing</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        enc_rep = urllib.parse.quote(replay_phrase)
        components.iframe(f"https://ai-avatar-jade-zeta.vercel.app/?text={enc_rep}&speed=0.10&pause=800", width=640, height=440)

    if not saved_list:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px dashed #CBD5E1; border-radius: 16px; padding: 36px; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 8px;">⭐</div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #0F172A; margin-bottom: 4px;">Save useful phrases for quick access.</div>
                <div style="font-size: 0.84rem; color: #64748B;">Star any phrase in the Translator to save it to your phrasebook.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for idx, phrase in enumerate(saved_list):
            st.markdown(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 14px 18px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="color: #F59E0B; font-size: 1.1rem;">⭐</span>
                        <span style="font-size: 0.98rem; font-weight: 600; color: #0F172A;">"{phrase}"</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            c_r1, c_r2, _ = st.columns([1, 1, 3])
            with c_r1:
                if st.button("▶ Replay ISL", key=f"rep_btn_{idx}", type="primary", use_container_width=True):
                    st.session_state["active_saved_replay"] = phrase
                    st.rerun()
            with c_r2:
                if st.button("Delete", key=f"del_saved_{idx}", type="secondary", use_container_width=True):
                    st.session_state["saved_phrases"].remove(phrase)
                    st.rerun()


def render_history_view():
    """Renders the recent activity timeline."""
    history = st.session_state.get("history", [])

    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
            <div>
                <div style="font-size: 0.82rem; font-weight: 700; color: #5B5CEB; text-transform: uppercase;">ACTIVITY LOG</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #0F172A;">Recent Translations Timeline</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not history:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px dashed #CBD5E1; border-radius: 16px; padding: 36px; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 8px;">🕘</div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #0F172A; margin-bottom: 4px;">Your conversations will appear here.</div>
                <div style="font-size: 0.84rem; color: #64748B;">Any spoken speech or translated text will be logged with linguistic metrics.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        if st.button("🗑️ Clear History", key="btn_clear_hist_top", type="secondary"):
            st.session_state["history"] = []
            st.rerun()

        for idx, item in enumerate(history):
            if isinstance(item, dict):
                transcript = item.get("transcript", "")
                english_text = item.get("english_text", transcript)
                lang = item.get("display_lang", "English")
                cov = item.get("coverage", 100.0)
                emotion = item.get("emotion_data", {}).get("emotion", "NEUTRAL")
            else:
                transcript, _, cov = item
                english_text = transcript
                lang = "English"
                emotion = "NEUTRAL"

            st.markdown(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 16px 20px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 0.74rem; font-weight: 700; color: #5B5CEB; background: rgba(91,92,235,0.08); padding: 2px 8px; border-radius: 6px;">{lang}</span>
                        <span style="font-size: 0.74rem; color: #64748B;">Emotion: <b>{emotion}</b> · Match: <b>{cov:.0f}%</b></span>
                    </div>
                    <div style="font-size: 1.02rem; font-weight: 700; color: #0F172A; margin-bottom: 2px;">"{transcript}"</div>
                    {f'<div style="font-size: 0.86rem; color: #64748B;"><b>English:</b> "{english_text}"</div>' if english_text != transcript else ''}
                </div>
                """,
                unsafe_allow_html=True,
            )
