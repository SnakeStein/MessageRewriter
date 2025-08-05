import os
import streamlit as st

st.set_page_config(
    page_title="Message Rewriter",
    page_icon="✉️",
    layout="centered",
)

st.title("✉️ Message Rewriter")
st.caption("Paste a rough email or message, pick a tone, and get a polished version.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API key", type="password")
    tone = st.radio("Tone", options=["Formal", "Friendly", "Short"])

draft = st.text_area("Your rough message", height=180)
rewrite_btn = st.button("Rewrite", type="primary")
