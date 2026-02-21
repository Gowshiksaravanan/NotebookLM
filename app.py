import streamlit as st
import uuid
import base64
import os
from datetime import datetime
from auth import require_auth

# ── Logo ─────────────────────────────────────────────────────────────────────
LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 60">
  <defs>
    <linearGradient id="lg1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea"/>
      <stop offset="100%" style="stop-color:#764ba2"/>
    </linearGradient>
    <linearGradient id="lg2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#a78bfa"/>
      <stop offset="100%" style="stop-color:#667eea"/>
    </linearGradient>
    <linearGradient id="sp" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#fbbf24"/>
      <stop offset="100%" style="stop-color:#f59e0b"/>
    </linearGradient>
  </defs>
  <g transform="translate(4,6)">
    <rect x="2" y="4" width="36" height="44" rx="4" fill="url(#lg1)"/>
    <rect x="2" y="4" width="8" height="44" rx="3" fill="url(#lg2)" opacity="0.7"/>
    <line x1="16" y1="16" x2="32" y2="16" stroke="rgba(255,255,255,0.5)" stroke-width="1.8" stroke-linecap="round"/>
    <line x1="16" y1="23" x2="30" y2="23" stroke="rgba(255,255,255,0.4)" stroke-width="1.8" stroke-linecap="round"/>
    <line x1="16" y1="30" x2="32" y2="30" stroke="rgba(255,255,255,0.5)" stroke-width="1.8" stroke-linecap="round"/>
    <line x1="16" y1="37" x2="28" y2="37" stroke="rgba(255,255,255,0.4)" stroke-width="1.8" stroke-linecap="round"/>
    <g transform="translate(32,2)">
      <path d="M6 0 L7.5 4.5 L12 6 L7.5 7.5 L6 12 L4.5 7.5 L0 6 L4.5 4.5 Z" fill="url(#sp)"/>
      <path d="M14 8 L14.8 10.2 L17 11 L14.8 11.8 L14 14 L13.2 11.8 L11 11 L13.2 10.2 Z" fill="#fbbf24" opacity="0.7"/>
    </g>
  </g>
  <text x="56" y="28" font-family="Inter,-apple-system,sans-serif" font-size="22" font-weight="700">
    <tspan fill="url(#lg1)">Notebook</tspan><tspan fill="#a78bfa" font-weight="800">LM</tspan>
  </text>
  <text x="57" y="46" font-family="Inter,-apple-system,sans-serif" font-size="10.5" fill="#8888aa" font-weight="400" letter-spacing="0.8">
    AI-Powered Study Companion
  </text>
</svg>"""

# Small icon-only version for headers
LOGO_ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 60">
  <defs>
    <linearGradient id="ig1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea"/>
      <stop offset="100%" style="stop-color:#764ba2"/>
    </linearGradient>
    <linearGradient id="ig2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#a78bfa"/>
      <stop offset="100%" style="stop-color:#667eea"/>
    </linearGradient>
    <linearGradient id="isp" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#fbbf24"/>
      <stop offset="100%" style="stop-color:#f59e0b"/>
    </linearGradient>
  </defs>
  <g transform="translate(2,4)">
    <rect x="2" y="4" width="36" height="44" rx="5" fill="url(#ig1)"/>
    <rect x="2" y="4" width="9" height="44" rx="4" fill="url(#ig2)" opacity="0.7"/>
    <line x1="16" y1="16" x2="32" y2="16" stroke="rgba(255,255,255,0.55)" stroke-width="2" stroke-linecap="round"/>
    <line x1="16" y1="23" x2="30" y2="23" stroke="rgba(255,255,255,0.4)" stroke-width="2" stroke-linecap="round"/>
    <line x1="16" y1="30" x2="32" y2="30" stroke="rgba(255,255,255,0.55)" stroke-width="2" stroke-linecap="round"/>
    <line x1="16" y1="37" x2="28" y2="37" stroke="rgba(255,255,255,0.4)" stroke-width="2" stroke-linecap="round"/>
    <g transform="translate(30,0)">
      <path d="M7 0 L8.8 5.3 L14 7 L8.8 8.8 L7 14 L5.2 8.8 L0 7 L5.2 5.3 Z" fill="url(#isp)"/>
      <path d="M16 9 L17 11.5 L19.5 12.5 L17 13.5 L16 16 L15 13.5 L12.5 12.5 L15 11.5 Z" fill="#fbbf24" opacity="0.7"/>
    </g>
  </g>
</svg>"""


def get_logo_b64(svg_str: str) -> str:
    return base64.b64encode(svg_str.encode()).decode()


LOGO_B64 = get_logo_b64(LOGO_SVG)
ICON_B64 = get_logo_b64(LOGO_ICON_SVG)


# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NotebookLM",
    page_icon="📓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global Styles ────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] .stMarkdown h1 {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
    font-size: 1.8rem;
    letter-spacing: -0.5px;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #c0c0d0 !important;
}
section[data-testid="stSidebar"] .stDivider {
    border-color: rgba(255,255,255,0.08) !important;
}

/* ── Notebook button in sidebar ── */
section[data-testid="stSidebar"] .stButton > button {
    border-radius: 10px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 8px 14px !important;
    transition: all 0.2s ease !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    color: white !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #d0d0e0 !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.1) !important;
    border-color: rgba(102,126,234,0.4) !important;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0px;
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(255,255,255,0.06);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 10px 24px;
    font-weight: 500;
    font-size: 0.9rem;
    color: #888;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    font-weight: 600;
}
.stTabs [data-baseweb="tab-highlight"] {
    display: none;
}
.stTabs [data-baseweb="tab-border"] {
    display: none;
}

/* ── Main container ── */
.main .block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

/* ── Cards ── */
div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    background: rgba(255,255,255,0.02) !important;
    transition: all 0.2s ease;
}
div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"]:hover {
    border-color: rgba(102,126,234,0.3) !important;
    background: rgba(255,255,255,0.04) !important;
}

/* ── Chat messages ── */
.stChatMessage {
    border-radius: 14px !important;
    padding: 16px 20px !important;
    margin-bottom: 8px !important;
}
div[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}
div[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
}

/* ── Chat input ── */
.stChatInput > div {
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    background: rgba(255,255,255,0.03) !important;
}
.stChatInput > div:focus-within {
    border-color: #667eea !important;
    box-shadow: 0 0 0 2px rgba(102,126,234,0.2) !important;
}

/* ── Expanders ── */
.streamlit-expanderHeader {
    border-radius: 10px !important;
    font-weight: 500 !important;
}

/* ── File uploader ── */
section[data-testid="stFileUploader"] > div {
    border-radius: 14px !important;
    border: 2px dashed rgba(102,126,234,0.3) !important;
    background: rgba(102,126,234,0.03) !important;
}
section[data-testid="stFileUploader"] > div:hover {
    border-color: rgba(102,126,234,0.6) !important;
    background: rgba(102,126,234,0.06) !important;
}

/* ── Main content buttons ── */
.main .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    transition: all 0.2s ease !important;
}
.main .stButton > button[kind="primary"]:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.3) !important;
}
.main .stButton > button[kind="secondary"] {
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    background: rgba(255,255,255,0.04) !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
.main .stButton > button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.2) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    border-radius: 10px !important;
    font-weight: 500 !important;
}

/* ── Text input ── */
.stTextInput > div > div {
    border-radius: 10px !important;
}

/* ── Metrics / status badges ── */
.stSuccess, .stWarning, .stError, .stInfo {
    border-radius: 10px !important;
}

/* ── Welcome hero ── */
.welcome-hero {
    text-align: center;
    padding: 80px 40px;
    background: linear-gradient(135deg, rgba(102,126,234,0.08) 0%, rgba(118,75,162,0.08) 100%);
    border-radius: 20px;
    border: 1px solid rgba(102,126,234,0.15);
    margin: 20px 0;
}
.welcome-hero h1 {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 12px;
}
.welcome-hero p {
    color: #9090a8;
    font-size: 1.1rem;
    line-height: 1.6;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 60px 30px;
    color: #707088;
}
.empty-state h3 {
    color: #a0a0b8;
    margin-bottom: 8px;
    font-weight: 600;
}
.empty-state p {
    font-size: 0.95rem;
    line-height: 1.5;
}

/* ── Source card ── */
.source-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 20px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    margin-bottom: 10px;
    transition: all 0.2s ease;
}
.source-card:hover {
    border-color: rgba(102,126,234,0.3);
    background: rgba(255,255,255,0.04);
}
.source-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
}
.source-icon.pdf { background: rgba(239,68,68,0.15); }
.source-icon.pptx { background: rgba(249,115,22,0.15); }
.source-icon.txt { background: rgba(59,130,246,0.15); }
.source-icon.url { background: rgba(34,197,94,0.15); }
.source-icon.youtube { background: rgba(239,68,68,0.15); }
.source-info { flex: 1; min-width: 0; }
.source-info .name {
    font-weight: 600;
    font-size: 0.95rem;
    color: #e0e0f0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.source-info .meta {
    font-size: 0.8rem;
    color: #707088;
    margin-top: 2px;
}
.source-badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.source-badge.ready {
    background: rgba(34,197,94,0.15);
    color: #22c55e;
}
.source-badge.processing {
    background: rgba(234,179,8,0.15);
    color: #eab308;
}
.source-badge.failed {
    background: rgba(239,68,68,0.15);
    color: #ef4444;
}

/* ── Artifact generation cards ── */
.gen-card {
    text-align: center;
    padding: 30px 20px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    transition: all 0.25s ease;
    cursor: default;
}
.gen-card:hover {
    border-color: rgba(102,126,234,0.3);
    background: rgba(102,126,234,0.04);
    transform: translateY(-2px);
}
.gen-card .icon {
    font-size: 2.5rem;
    margin-bottom: 12px;
}
.gen-card h4 {
    margin: 0 0 6px 0;
    font-weight: 600;
    color: #e0e0f0;
}
.gen-card p {
    font-size: 0.85rem;
    color: #808098;
    line-height: 1.4;
    margin: 0;
}

/* ── Citation chip ── */
.citation-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    background: rgba(102,126,234,0.1);
    border: 1px solid rgba(102,126,234,0.2);
    border-radius: 20px;
    font-size: 0.8rem;
    color: #a0b0f0;
    margin: 3px 4px;
}

/* ── Notebook header ── */
.notebook-header {
    padding: 0 0 16px 0;
    margin-bottom: 16px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.notebook-header h2 {
    font-weight: 700;
    font-size: 1.5rem;
    margin: 0;
    color: #e8e8f8;
}
.notebook-header .meta {
    font-size: 0.85rem;
    color: #707088;
    margin-top: 4px;
}

/* ── Hide ALL Streamlit default chrome ── */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
.stDeployButton,
[data-testid="stToolbar"],
[data-testid="stBottomBlockContainer"],
[data-testid="manage-app-button"] {
    display: none !important;
}
/* Kill all Material Icon text leaks */
[data-testid="stSidebarCollapseButton"] *,
[data-testid="collapsedControl"] *,
[data-testid="stBottomBlockContainer"] * {
    display: none !important;
}

/* ── Force dark theme on main area ── */
.stApp, .stApp > header {
    background-color: #0e1117 !important;
}
.main .block-container {
    background-color: #0e1117 !important;
}
.stApp [data-testid="stHeader"] {
    background-color: #0e1117 !important;
}
/* All text defaults to light */
.stApp, .stApp p, .stApp span, .stApp li, .stApp td, .stApp th {
    color: #c8c8d8 !important;
}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: #e0e0f0 !important;
}
.stApp strong {
    color: #e8e8f8 !important;
}
/* Markdown inside containers */
.stMarkdown, .stMarkdown p {
    color: #c8c8d8 !important;
}

/* ── Expander styling for dark ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 10px !important;
    color: #c0c0d0 !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.01) !important;
    border-color: rgba(255,255,255,0.06) !important;
}

/* ── Table styling ── */
.stApp table {
    border-collapse: collapse;
}
.stApp th {
    background: rgba(102,126,234,0.1) !important;
    border-bottom: 1px solid rgba(255,255,255,0.1) !important;
}
.stApp td {
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
}

/* ── Radio / select styling ── */
.stRadio label, .stSelectbox label, .stSlider label {
    color: #a0a0b8 !important;
}

/* ── Alert boxes ── */
[data-testid="stAlert"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.25); }
</style>
""", unsafe_allow_html=True)


# ── Authentication ───────────────────────────────────────────────────────────
user = require_auth()
user_id = user["id"]

# ── Per-User Session State ───────────────────────────────────────────────────
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

if user_id not in st.session_state.user_data:
    default_id = str(uuid.uuid4())
    st.session_state.user_data[user_id] = {
        "notebooks": {
            default_id: {
                "id": default_id,
                "title": "My First Notebook",
                "created_at": datetime.now().isoformat(),
                "sources": [],
                "messages": [],
                "artifacts": [],
            }
        },
        "active_notebook_id": default_id,
    }

udata = st.session_state.user_data[user_id]


# ── Helper Functions ─────────────────────────────────────────────────────────
def get_active_notebook():
    nb_id = udata["active_notebook_id"]
    if nb_id and nb_id in udata["notebooks"]:
        return udata["notebooks"][nb_id]
    return None


def create_notebook(title: str):
    nb_id = str(uuid.uuid4())
    udata["notebooks"][nb_id] = {
        "id": nb_id,
        "title": title,
        "created_at": datetime.now().isoformat(),
        "sources": [],
        "messages": [],
        "artifacts": [],
    }
    udata["active_notebook_id"] = nb_id


def delete_notebook(nb_id: str):
    if nb_id in udata["notebooks"]:
        del udata["notebooks"][nb_id]
        remaining = list(udata["notebooks"].keys())
        udata["active_notebook_id"] = remaining[0] if remaining else None


def rename_notebook(nb_id: str, new_title: str):
    if nb_id in udata["notebooks"]:
        udata["notebooks"][nb_id]["title"] = new_title


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f'<div style="padding: 8px 0 4px 0;">'
        f'<img src="data:image/svg+xml;base64,{LOGO_B64}" style="width:100%; max-width:240px;" />'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p style="font-size:0.82rem; color:#7070888; margin: 4px 0 0 0;">'
        f'Signed in as <strong style="color:#a0a0f0;">{user["name"]}</strong></p>',
        unsafe_allow_html=True,
    )
    st.divider()

    # ── Create notebook ──
    with st.popover("+ New Notebook", use_container_width=True):
        new_title = st.text_input(
            "Name", placeholder="e.g. Biology 101", label_visibility="collapsed"
        )
        if st.button("Create Notebook", use_container_width=True, type="primary"):
            if new_title.strip():
                create_notebook(new_title.strip())
                st.rerun()
            else:
                st.warning("Enter a name.")

    st.markdown("")  # spacer

    # ── Notebook list ──
    if not udata["notebooks"]:
        st.markdown(
            '<p style="text-align:center; color:#606078; padding:20px 0;">'
            "No notebooks yet</p>",
            unsafe_allow_html=True,
        )
    else:
        for nb_id, nb in udata["notebooks"].items():
            is_active = nb_id == udata["active_notebook_id"]
            source_count = len(nb["sources"])
            msg_count = len(nb["messages"])

            col1, col2 = st.columns([5, 1])
            with col1:
                label = nb["title"]
                if source_count > 0 or msg_count > 0:
                    label += f"  ({source_count}s, {msg_count}m)"
                if st.button(
                    f"{'> ' if is_active else '  '}{label}",
                    key=f"sel_{nb_id}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                ):
                    udata["active_notebook_id"] = nb_id
                    st.rerun()
            with col2:
                if st.button(
                    "x", key=f"del_{nb_id}",
                    help="Delete this notebook",
                    use_container_width=True,
                ):
                    delete_notebook(nb_id)
                    st.rerun()

    st.divider()

    # ── Rename ──
    notebook = get_active_notebook()
    if notebook:
        with st.popover("Rename", use_container_width=True):
            rename_val = st.text_input(
                "New name", value=notebook["title"], key="rename_input"
            )
            if st.button("Save", use_container_width=True, type="primary"):
                if rename_val.strip():
                    rename_notebook(notebook["id"], rename_val.strip())
                    st.rerun()

    # ── Footer ──
    st.markdown("")
    st.markdown(
        '<p style="font-size:0.75rem; color:#50506a; text-align:center;">'
        "Built with Streamlit on HF Spaces</p>",
        unsafe_allow_html=True,
    )


# ── Main Content ─────────────────────────────────────────────────────────────
notebook = get_active_notebook()

if not notebook:
    st.markdown(
        f"""
        <div class="welcome-hero">
            <img src="data:image/svg+xml;base64,{ICON_B64}" style="width:64px; margin-bottom:16px;" />
            <h1>NotebookLM</h1>
            <p>Your AI-powered study companion.<br>
            Create a notebook from the sidebar to get started.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ── Notebook header ──
source_count = len(notebook["sources"])
msg_count = len(notebook["messages"])
artifact_count = len(notebook["artifacts"])
st.markdown(
    f"""
    <div class="notebook-header">
        <h2>{notebook["title"]}</h2>
        <div class="meta">{source_count} sources &nbsp;&bull;&nbsp; {msg_count} messages &nbsp;&bull;&nbsp; {artifact_count} artifacts</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Tabs ──
tab_chat, tab_sources, tab_artifacts = st.tabs(
    ["   Chat   ", "   Sources   ", "   Artifacts   "]
)

from ui.chat_page import render_chat
from ui.upload_page import render_sources
from ui.artifact_page import render_artifacts

with tab_chat:
    render_chat(notebook)

with tab_sources:
    render_sources(notebook)

with tab_artifacts:
    render_artifacts(notebook)
