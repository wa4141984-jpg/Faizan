# Faiz# 🎓 AI Study Assistant

A beginner-friendly AI chatbot built with **Python + Streamlit**, powered by the **Anthropic Claude API**.
Ask questions, upload study material, and choose a study mode (Explain simply, Quiz me, Summarize, Study plan).

## Features
- Chat with streaming answers and a loading indicator
- Upload `.pdf`, `.docx`, `.txt`, `.md`, `.csv`, `.py`, `.json` and images (`.png`, `.jpg`, `.webp`)
- Input validation (empty/too-long messages, file type, size, count, unreadable files)
- Friendly errors (bad key, rate limit, network issues)
- API key kept out of the code (environment variable or Streamlit secrets)
- Responsive layout (works on phones)

## Project structure
```
ai-study-assistant/
├── app.py              # Streamlit user interface
├── ai_client.py        # Claude API calls + error handling
├── file_utils.py       # File validation and text extraction
├── config.py           # Settings and API-key loading
├── requirements.txt
├── .env.example        # Template (no real secrets)
├── .gitignore
└── .streamlit/
    ├── config.toml             # Theme
    └── secrets.toml.example    # Template for Streamlit secrets
```

## 1. Get an API key
1. Go to <https://console.anthropic.com> and sign up / log in.
2. Add credits under **Billing** (the API is pay-as-you-go).
3. Open **API Keys → Create Key**, name it, and copy it (shown only once).

## 2. Install
Requires Python 3.9+.
```bash
cd ai-study-assistant
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configure the key
```bash
cp .env.example .env            # Windows: copy .env.example .env
```
Open `.env` and replace `your-api-key-here` with your real key. `.env` is git-ignored — never share or commit it.

## 4. Run locally
```bash
streamlit run app.py
```
Open <http://localhost:8501>.

## 5. Deploy (Streamlit Community Cloud, free)
1. Push the project to a GitHub repo (confirm `.env` is NOT included).
2. Go to <https://share.streamlit.io> → **New app** → pick your repo, branch, and `app.py`.
3. Open **Advanced settings → Secrets** and paste:
   ```toml
   ANTHROPIC_API_KEY = "your-real-key"
   ```
4. Click **Deploy**. Other hosts (Render, Railway, Hugging Face Spaces) work too: set `ANTHROPIC_API_KEY` as an environment variable and use the start command
   `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`.

> Anyone with your public app link can use your API credits. Set a spend limit in the Anthropic console, or restrict app access in Streamlit's sharing settings.

## Changing the model
Set `ANTHROPIC_MODEL` in `.env` (e.g. a cheaper/faster model) or edit `DEFAULT_MODEL` in `config.py`.

## Limitations
- **Chat history is not saved**; it resets when you refresh the page.
- **Long files are truncated** (first 30,000 characters each) and large chats only send the last 20 messages.
- **Scanned PDFs** (images of text) can't be read; use a text-based PDF or upload page screenshots as images.
- Images are re-sent with each question while uploaded, which uses more tokens.
- AI can make mistakes — verify important facts, especially for exams, medical, legal, or financial topics.
- No user accounts or per-user rate limiting; all users share one API key.
- Only `.docx` (not old `.doc`) Word files are supported.

## Troubleshooting
| Message | Fix |
|---|---|
| "API key not found" | Create `.env` (local) or add secrets (deployed) |
| "API key was rejected" | Re-copy the key; check for extra spaces/quotes |
| "Usage limit reached" | Add credits or wait and retry |
| Model not found error | Set `ANTHROPIC_MODEL` to a model your account can use |an
