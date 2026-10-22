"""AI Study Assistant - Streamlit UI. Run with:  streamlit run app.py"""
import os
import sys

import streamlit as st

st.set_page_config(page_title="AI Study Assistant", page_icon="🎓", layout="centered")

# Make sure Python can find our sibling files no matter where the app is launched from.
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# Friendly check: all project files must be uploaded next to app.py.
_missing = [f for f in ("ai_client.py", "config.py", "file_utils.py")
            if not os.path.exists(os.path.join(APP_DIR, f))]
if _missing:
    st.error(
        f"**Missing project files:** {', '.join(_missing)}. "
        "Upload ALL files from the project (not just app.py) to the same folder / GitHub repo."
    )
    st.stop()

try:
    import ai_client
    import config
    import file_utils
except ModuleNotFoundError as e:
    st.error(
        f"**Missing Python package: `{e.name}`.** Make sure `requirements.txt` is in your repo "
        "root and contains all packages, then reboot the app."
    )
    st.stop()

st.markdown(
    """
    <style>
      .block-container {max-width: 820px; padding-top: 2rem;}
      .hero {background: linear-gradient(135deg, #6C5CE7, #8E7BFF); color: white;
             padding: 1.4rem 1.6rem; border-radius: 16px; margin-bottom: 1.2rem;}
      .hero h1 {margin: 0; font-size: 1.8rem; color: white;}
      .hero p {margin: .3rem 0 0; opacity: .9;}
      [data-testid="stChatMessage"] {border-radius: 14px;}
      @media (max-width: 640px) {.hero h1 {font-size: 1.4rem;} .block-container {padding: 1rem;}}
    </style>
    <div class="hero"><h1>🎓 AI Study Assistant</h1>
    <p>Ask questions, upload notes, and learn faster.</p></div>
    """,
    unsafe_allow_html=True,
)

# ---- session state ----
st.session_state.setdefault("messages", [])
st.session_state.setdefault("files", [])

api_key = config.get_api_key()
if not api_key:
    st.error(
        "**API key not found.** Add `ANTHROPIC_API_KEY` to a `.env` file (local) or to "
        "Streamlit secrets (deployment). See the README for step-by-step instructions."
    )
    st.stop()

# ---- sidebar ----
with st.sidebar:
    st.header("⚙️ Settings")
    mode = st.selectbox("Study mode", list(ai_client.MODES.keys()))

    st.subheader("📎 Study material")
    uploads = st.file_uploader(
        f"Up to {config.MAX_FILES} files, {config.MAX_FILE_MB} MB each",
        type=config.ALLOWED_TYPES,
        accept_multiple_files=True,
    )
    if uploads:
        with st.spinner("Reading your files..."):
            files, problems = file_utils.process_files(uploads)
        st.session_state.files = files
        for p in problems:
            st.warning(p)
        for f in files:
            st.caption(f"✅ {f['name']}" + (" (truncated)" if f.get("truncated") else ""))
    else:
        st.session_state.files = []

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---- chat history ----
if not st.session_state.messages:
    st.info("👋 Try: *“Explain photosynthesis simply”*, or upload notes and pick **Quiz me**.")
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ---- new message ----
prompt = st.chat_input("Ask a question...")
if prompt is not None:
    prompt = prompt.strip()
    if not prompt:
        st.warning("Please type a question first.")
    elif len(prompt) > config.MAX_MESSAGE_CHARS:
        st.warning(f"Your message is {len(prompt)} characters; the limit is {config.MAX_MESSAGE_CHARS}.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                with st.spinner("Thinking..."):
                    stream = ai_client.stream_reply(
                        api_key, mode, st.session_state.messages, st.session_state.files
                    )
                    first = next(stream, "")  # spinner shows until the first words arrive
                def _chain():
                    yield first
                    yield from stream

                reply = st.write_stream(_chain())
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except ai_client.AIError as e:
                st.error(f"⚠️ {e}")
                st.session_state.messages.pop()  # let the user resend
            except Exception:
                st.error("⚠️ Something unexpected went wrong. Please try again.")
                st.session_state.messages.pop()
