meetmate-agent/
├── app.py                        # Streamlit UI / orchestrator
├── pipeline.py                   # High-level pipeline runner
├── google_drive.py               # Drive API helpers (download meeting recording)
├── audio.py                      # video -> audio extraction and sampling
├── ocr.py                        # extract frames + run OCR (pytesseract)
├── transcribe.py                 # whisper transcription wrapper
├── merge.py                      # merge transcript and screen OCR with timestamps
├── llm_agent.py                  # calls OpenAI / local LLM to summarize & analyze
├── utils/
│   └── helpers.py
├── requirements.txt
├── README.md
└── credentials.json (place your Google OAuth here)
