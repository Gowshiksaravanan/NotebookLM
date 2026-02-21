---
title: NotebookLM Clone
emoji: 📓
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.31.0"
app_file: app.py
pinned: false
hf_oauth: true
hf_oauth_scopes:
  - openid
  - profile
---

# NotebookLM Clone

AI-powered study companion — upload documents, chat with them, and generate study artifacts.

## Features (Frontend MVP)

- **Notebook Management**: Create, rename, delete, and switch between notebooks
- **Source Upload**: Upload PDF, PPTX, TXT files or add URLs / YouTube links
- **Chat Interface**: Conversational UI with citation rendering (mock responses)
- **Artifact Generation**: Generate summaries, quizzes, and podcast scripts (mock content)
- **Download Artifacts**: Export generated content as markdown files

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```
app.py                  # Streamlit entrypoint
ui/
  chat_page.py          # Chat interface with mock RAG responses
  upload_page.py        # Source upload and management
  artifact_page.py      # Artifact generation and viewer
requirements.txt        # Python dependencies
```
