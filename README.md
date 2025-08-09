# Message Rewriter

Polish rough emails and messages with Gemini. Pick a tone (Formal, Friendly, or Short) and compare before/after side by side.

## Setup

```bash
cd MessageRewriter
pip install -r requirements.txt
```

Set your API key (optional if you enter it in the app sidebar):

```bash
# PowerShell
$env:GEMINI_API_KEY = "your-key-here"
```

Get a key at [Google AI Studio](https://aistudio.google.com/apikey).

## Run

```bash
streamlit run app.py
```

## Features

- **Tone presets** — Formal, Friendly, Short
- **Before / after** — side-by-side comparison
- **Copy button** — one click to copy the polished text
