"""
SignBridge AI — Modern 2026 SaaS Design Tokens & Streamlit Stylesheet
Light-first, calm, accessible, intelligent, human, trustworthy, and professional.
"""

def get_modern_css(high_contrast: bool = False, large_text: bool = False, reduced_motion: bool = False) -> str:
    """Returns the injected CSS string styled for the 2026 SaaS light theme."""
    
    font_size_base = "17px" if large_text else "15px"
    font_scale_h1 = "2.1rem" if large_text else "1.85rem"
    font_scale_h2 = "1.5rem" if large_text else "1.35rem"
    border_color = "#94A3B8" if high_contrast else "#E5E7EB"
    card_bg = "#FFFFFF"
    canvas_bg = "#FFFFFF" if high_contrast else "#F6F8FC"
    transition_dur = "0s" if reduced_motion else "0.2s"

    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        /* Root variables */
        :root {{
            --bg-canvas: {canvas_bg};
            --bg-surface: {card_bg};
            --primary: #5B5CEB;
            --primary-hover: #4F46E5;
            --primary-light: rgba(91, 92, 235, 0.08);
            --secondary: #14B8A6;
            --secondary-light: rgba(20, 184, 166, 0.10);
            --text-main: #0F172A;
            --text-muted: #64748B;
            --border: {border_color};
            --success: #10B981;
            --warning: #F59E0B;
            --danger: #EF4444;
            --radius-card: 20px;
            --radius-btn: 12px;
            --radius-pill: 999px;
            --shadow-subtle: 0 1px 3px rgba(15, 23, 42, 0.04), 0 6px 16px rgba(15, 23, 42, 0.03);
            --shadow-card: 0 4px 20px rgba(15, 23, 42, 0.05);
            --transition-speed: {transition_dur};
        }}

        /* App Canvas Override */
        .stApp {{
            background-color: var(--bg-canvas) !important;
            color: var(--text-main) !important;
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            font-size: {font_size_base} !important;
        }}

        /* Streamlit Main Container */
        .main .block-container {{
            max-width: 1380px !important;
            padding-top: 1.2rem !important;
            padding-bottom: 3rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }}

        /* Hide unnecessary Streamlit chrome safely */
        #MainMenu, footer, header[data-testid="stHeader"] {{
            background: transparent !important;
        }}

        /* Modern Clean Sidebar */
        [data-testid="stSidebar"] {{
            background-color: #FFFFFF !important;
            border-right: 1px solid var(--border) !important;
            box-shadow: 2px 0 12px rgba(15, 23, 42, 0.02) !important;
        }}

        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 1.2rem;
            padding-bottom: 1.5rem;
        }}

        [data-testid="stSidebar"] hr {{
            border-color: var(--border) !important;
            margin: 14px 0 !important;
        }}

        /* Navigation Radio in Sidebar */
        [data-testid="stSidebar"] [data-testid="stRadio"] > div {{
            gap: 4px;
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] label {{
            background: transparent;
            border: 1px solid transparent;
            border-radius: var(--radius-btn);
            padding: 9px 14px;
            color: var(--text-muted);
            font-weight: 500;
            font-size: 0.92rem;
            transition: all var(--transition-speed) ease;
            cursor: pointer;
            display: flex;
            align-items: center;
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {{
            background: var(--bg-canvas);
            color: var(--text-main);
        }}

        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] {{
            background: var(--primary-light) !important;
            color: var(--primary) !important;
            font-weight: 600 !important;
            border-left: 3px solid var(--primary) !important;
        }}

        /* Buttons */
        .stButton > button {{
            border-radius: var(--radius-btn) !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            padding: 0.65rem 1.25rem !important;
            transition: all var(--transition-speed) cubic-bezier(0.16, 1, 0.3, 1) !important;
            border: 1px solid var(--border) !important;
        }}

        .stButton > button[kind="primary"] {{
            background-color: var(--primary) !important;
            border: 1px solid var(--primary) !important;
            color: #FFFFFF !important;
            box-shadow: 0 2px 8px rgba(91, 92, 235, 0.25) !important;
        }}

        .stButton > button[kind="primary"]:hover {{
            background-color: var(--primary-hover) !important;
            border-color: var(--primary-hover) !important;
            box-shadow: 0 4px 14px rgba(91, 92, 235, 0.35) !important;
            transform: translateY(-1px);
        }}

        .stButton > button[kind="secondary"] {{
            background-color: #FFFFFF !important;
            border: 1px solid var(--border) !important;
            color: var(--text-main) !important;
        }}

        .stButton > button[kind="secondary"]:hover {{
            background-color: var(--bg-canvas) !important;
            border-color: #CBD5E1 !important;
            color: var(--primary) !important;
        }}

        /* Inputs & Select Boxes */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {{
            background-color: #FFFFFF !important;
            border-color: var(--border) !important;
            color: var(--text-main) !important;
            border-radius: 10px !important;
            box-shadow: none !important;
        }}

        div[data-baseweb="select"] > div:hover,
        div[data-baseweb="input"] > div:hover,
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: var(--primary) !important;
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: #F1F5F9;
            padding: 4px;
            border-radius: 12px;
            border: 1px solid var(--border);
        }}

        .stTabs [data-baseweb="tab"] {{
            background-color: transparent !important;
            border-radius: 8px !important;
            color: var(--text-muted) !important;
            font-weight: 600 !important;
            font-size: 0.90rem !important;
            padding: 8px 18px !important;
            border: none !important;
        }}

        .stTabs [aria-selected="true"] {{
            background-color: #FFFFFF !important;
            color: var(--primary) !important;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08) !important;
        }}

        /* Cards & Expanders */
        [data-testid="stExpander"] {{
            background-color: #FFFFFF !important;
            border: 1px solid var(--border) !important;
            border-radius: 14px !important;
            box-shadow: var(--shadow-subtle) !important;
        }}

        [data-testid="stExpander"] summary {{
            color: var(--text-main) !important;
            font-weight: 600 !important;
        }}

        /* Headings */
        h1 {{
            color: var(--text-main) !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 800 !important;
            font-size: {font_scale_h1} !important;
            letter-spacing: -0.025em !important;
        }}

        h2, h3, h4 {{
            color: var(--text-main) !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            font-size: {font_scale_h2} !important;
            letter-spacing: -0.015em !important;
        }}

        /* Audio component wrapper */
        .stAudio {{
            border-radius: 12px;
            background: #FFFFFF;
            padding: 6px;
            border: 1px solid var(--border);
        }}

        /* -------------------------------------------------------------------------- */
        /* Modern Accessible Light File Uploader Card Styling                         */
        /* -------------------------------------------------------------------------- */
        [data-testid="stFileUploader"] {{
            background-color: transparent !important;
            padding: 0 !important;
            margin-bottom: 10px !important;
        }}

        [data-testid="stFileUploader"] > label {{
            display: none !important;
        }}

        /* Uploader Dropzone Card */
        [data-testid="stFileUploaderDropzone"],
        section[data-testid="stFileUploaderDropzone"] {{
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            border: 1.5px dashed #D8DEE9 !important;
            border-radius: 14px !important;
            padding: 24px 20px 20px 20px !important;
            text-align: center !important;
            transition: all var(--transition-speed) ease !important;
            color: #334155 !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 6px !important;
        }}

        [data-testid="stFileUploaderDropzone"]::before {{
            content: "☁\\A Upload audio or video" !important;
            white-space: pre-line !important;
            font-size: 1.8rem !important;
            line-height: 1.3 !important;
            font-weight: 700 !important;
            color: #5B5CEB !important;
            display: block !important;
            margin-bottom: 2px !important;
        }}

        [data-testid="stFileUploaderDropzone"]:hover,
        [data-testid="stFileUploaderDropzone"]:focus-within {{
            border-color: #5B5CEB !important;
            background-color: #F5F3FF !important;
            background: #F5F3FF !important;
            box-shadow: 0 4px 14px rgba(91, 92, 235, 0.08) !important;
        }}

        /* Instructions inside dropzone */
        [data-testid="stFileUploaderDropzoneInstructions"] {{
            color: #64748B !important;
            margin-bottom: 4px !important;
            order: 2 !important;
        }}

        [data-testid="stFileUploaderDropzoneInstructions"] > div {{
            color: #64748B !important;
            font-size: 0.78rem !important;
            font-weight: 600 !important;
        }}

        [data-testid="stFileUploaderDropzoneInstructions"] small,
        [data-testid="stFileUploaderDropzoneInstructions"] span {{
            color: #94A3B8 !important;
            font-size: 0.72rem !important;
            display: block !important;
            margin-top: 2px !important;
        }}

        /* Choose file button */
        [data-testid="stFileUploaderDropzone"] button,
        [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] {{
            background-color: #5B5CEB !important;
            background: #5B5CEB !important;
            color: #FFFFFF !important;
            border: 1px solid #5B5CEB !important;
            border-radius: 10px !important;
            padding: 10px 22px !important;
            font-weight: 600 !important;
            font-size: 0 !important; /* Hide original 'Browse files' text */
            margin: 6px auto !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-shadow: 0 2px 6px rgba(91, 92, 235, 0.25) !important;
            transition: all var(--transition-speed) ease !important;
            cursor: pointer !important;
            order: 1 !important;
        }}

        [data-testid="stFileUploaderDropzone"] button::after,
        [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"]::after {{
            content: "Choose file" !important;
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            color: #FFFFFF !important;
            visibility: visible !important;
        }}

        [data-testid="stFileUploaderDropzone"] button:hover,
        [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"]:hover {{
            background-color: #4F46E5 !important;
            background: #4F46E5 !important;
            border-color: #4F46E5 !important;
            box-shadow: 0 4px 12px rgba(91, 92, 235, 0.35) !important;
            transform: translateY(-1px) !important;
            color: #FFFFFF !important;
        }}

        [data-testid="stFileUploaderDropzone"] button:focus {{
            outline: 2px solid #5B5CEB !important;
            outline-offset: 2px !important;
        }}

        /* Uploaded file row / container */
        [data-testid="stFileUploaderFileData"],
        [data-testid="stFileUploader"] ul,
        div[data-testid="stFileUploaderFile"] {{
            background: #FFFFFF !important;
            background-color: #FFFFFF !important;
            border: 1px solid #D8DEE9 !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
            margin-top: 12px !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
        }}

        /* Filename text */
        [data-testid="stFileUploaderFileName"],
        [data-testid="stFileUploader"] span[title] {{
            color: #0F172A !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
        }}

        [data-testid="stFileUploaderFileName"]::before {{
            content: "✓ " !important;
            color: #10B981 !important;
            font-weight: 700 !important;
            margin-right: 4px !important;
        }}

        /* File size text */
        [data-testid="stFileUploaderFileData"] small,
        [data-testid="stFileUploader"] small {{
            color: #64748B !important;
            font-size: 0.78rem !important;
            font-weight: 500 !important;
            display: block !important;
        }}

        /* Delete / Remove button */
        [data-testid="stFileUploaderDeleteBtn"] button,
        button[data-testid="stFileUploaderDeleteBtn"] {{
            background: #FFFFFF !important;
            border: 1px solid #FECACA !important;
            border-radius: 8px !important;
            color: #EF4444 !important;
            padding: 6px 12px !important;
            font-size: 0.78rem !important;
            font-weight: 600 !important;
            transition: all var(--transition-speed) ease !important;
            cursor: pointer !important;
        }}

        [data-testid="stFileUploaderDeleteBtn"] button:hover,
        button[data-testid="stFileUploaderDeleteBtn"]:hover {{
            background: #FEE2E2 !important;
            border-color: #EF4444 !important;
            color: #DC2626 !important;
        }}

        [data-testid="stFileUploaderDeleteBtn"] svg {{
            color: #EF4444 !important;
            fill: currentColor !important;
        }}

        /* Audio Recorder Component */
        [data-testid="stAudioInput"] {{
            background: #FFFFFF !important;
            background-color: #FFFFFF !important;
            border: 1px solid #D8DEE9 !important;
            border-radius: 14px !important;
            padding: 12px !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
        }}

        [data-testid="stAudioInput"] button {{
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all var(--transition-speed) ease !important;
        }}

        /* Status Pills */
        .status-pill {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: var(--radius-pill);
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }}

        .status-pill-online {{
            background: rgba(16, 185, 129, 0.10);
            color: #059669;
            border: 1px solid rgba(16, 185, 129, 0.25);
        }}

        .status-pill-primary {{
            background: var(--primary-light);
            color: var(--primary);
            border: 1px solid rgba(91, 92, 235, 0.20);
        }}

        .status-pill-demo {{
            background: rgba(245, 158, 11, 0.12);
            color: #D97706;
            border: 1px solid rgba(245, 158, 11, 0.30);
        }}

        /* Progress bars */
        .stProgress > div > div > div > div {{
            background-color: var(--primary) !important;
            border-radius: 8px !important;
        }}

        /* Modern Card utility */
        .modern-card {{
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: var(--radius-card);
            padding: 24px;
            box-shadow: var(--shadow-subtle);
            transition: transform var(--transition-speed) ease, box-shadow var(--transition-speed) ease;
        }}

        .modern-card:hover {{
            box-shadow: var(--shadow-card);
        }}

        /* Feature cards */
        .feature-card {{
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 22px;
            box-shadow: var(--shadow-subtle);
            transition: all var(--transition-speed) ease;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .feature-card:hover {{
            transform: translateY(-3px);
            border-color: #CBD5E1;
            box-shadow: 0 10px 25px rgba(91, 92, 235, 0.08);
        }}
    </style>
    """


def safe_render_iframe(url: str, width: int = 640, height: int = 480):
    """Safely renders an iframe using st.iframe or components.iframe without deprecation warnings."""
    import streamlit as st
    import streamlit.components.v1 as components
    if hasattr(st, "iframe"):
        st.iframe(url, width=width, height=height)
    else:
        components.iframe(url, width=width, height=height)


def render_html(html_str: str):
    """Safely renders HTML without triggering markdown indented code blocks."""
    import textwrap
    import streamlit as st
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

