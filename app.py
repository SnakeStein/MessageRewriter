import html
import os

import google.generativeai as genai
import streamlit as st

st.set_page_config(
    page_title="Message Rewriter",
    page_icon="✉️",
    layout="centered",
)

st.markdown(
    """
<style>
    .stApp { max-width: 960px; margin: 0 auto; }
    .panel-before {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem 1.25rem;
        border-radius: 0 8px 8px 0;
        min-height: 120px;
        white-space: pre-wrap;
    }
    .panel-after {
        background: #ecfdf5;
        border-left: 4px solid #10b981;
        padding: 1rem 1.25rem;
        border-radius: 0 8px 8px 0;
        min-height: 120px;
        white-space: pre-wrap;
    }
    .tone-chip {
        display: inline-block;
        background: #eef2ff;
        color: #4338ca;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        font-size: 0.8rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

TONE_PRESETS = {
    "Formal": (
        "Rewrite in a formal, professional tone. Use complete sentences, "
        "proper greetings and closings where appropriate, and avoid slang or "
        "overly casual phrasing. Stay polite and respectful."
    ),
    "Friendly": (
        "Rewrite in a warm, friendly tone. Sound approachable and human while "
        "remaining clear. Light warmth is fine; avoid stiffness or corporate jargon."
    ),
    "Short": (
        "Rewrite to be as short as possible while keeping the same meaning. "
        "Cut filler, redundancy, and unnecessary pleasantries. Be direct."
    ),
}


def build_prompt(draft: str, tone: str) -> str:
    guide = TONE_PRESETS[tone]
    return f"""You are an expert email and message editor.

Task: Polish the user's rough draft into a clear, send-ready message.

Tone: {tone}
{guide}

Rules:
- Preserve the original intent, facts, names, dates, and requests.
- Do not invent information that is not implied by the draft.
- Fix grammar, spelling, and awkward phrasing.
- Return ONLY the rewritten message — no preamble, labels, or explanations.

ROUGH DRAFT:
---
{draft}
---"""


def rewrite_message(draft: str, tone: str, model_name: str) -> str:
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config={"temperature": 0.4},
    )
    response = model.generate_content(build_prompt(draft, tone))
    return response.text.strip()


# --- UI ---
st.title("✉️ Message Rewriter")
st.caption("Paste a rough email or message, pick a tone, and get a polished version.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input(
        "Gemini API key",
        value=os.environ.get("GEMINI_API_KEY", ""),
        type="password",
        help="Get a free key at Google AI Studio.",
    )
    if api_key:
        genai.configure(api_key=api_key)

    st.divider()
    tone = st.radio(
        "Tone",
        options=list(TONE_PRESETS.keys()),
        index=0,
        help="Formal = professional · Friendly = warm · Short = concise",
    )
    model_name = st.selectbox(
        "Model",
        ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        index=0,
    )

draft = st.text_area(
    "Your rough message",
    height=180,
    placeholder="e.g. hey can u send me the report by fri?? thx",
    key="draft_input",
)

col_go, col_clear = st.columns(2)
with col_go:
    rewrite_btn = st.button("Rewrite", type="primary", use_container_width=True)
with col_clear:
    if st.button("Clear", use_container_width=True):
        st.session_state.pop("last_rewrite", None)
        st.rerun()

MAX_CHARS = 20_000
if draft and len(draft) > MAX_CHARS:
    st.warning(f"Message trimmed to {MAX_CHARS:,} characters.")
    draft = draft[:MAX_CHARS]

if rewrite_btn:
    if not api_key:
        st.error("Add your Gemini API key in the sidebar.")
    elif not draft.strip():
        st.warning("Enter a message to rewrite.")
    else:
        with st.spinner("Polishing…"):
            try:
                polished = rewrite_message(draft.strip(), tone, model_name)
                st.session_state["last_rewrite"] = {
                    "draft": draft.strip(),
                    "polished": polished,
                    "tone": tone,
                }
            except Exception as exc:
                st.error(f"Rewrite failed: {exc}")

if result := st.session_state.get("last_rewrite"):
    st.divider()
    st.markdown(f'<span class="tone-chip">{result["tone"]}</span>', unsafe_allow_html=True)

    col_before, col_after = st.columns(2)
    with col_before:
        st.subheader("Before")
        st.markdown(
            f'<div class="panel-before">{html.escape(result["draft"])}</div>',
            unsafe_allow_html=True,
        )
    with col_after:
        st.subheader("After")
        st.markdown(
            f'<div class="panel-after">{html.escape(result["polished"])}</div>',
            unsafe_allow_html=True,
        )

    st.copy_button(
        "Copy polished message",
        result["polished"],
        use_container_width=True,
    )
