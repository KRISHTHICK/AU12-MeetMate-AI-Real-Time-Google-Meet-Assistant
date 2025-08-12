Quick Setup Steps (summary)
Install system tools:

Ubuntu / Debian:

bash
Copy
Edit
sudo apt update
sudo apt install -y ffmpeg tesseract-ocr
macOS (Homebrew):

bash
Copy
Edit
brew install ffmpeg tesseract
Create Python virtualenv & install Python deps:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
Google Drive API:

Create a Google Cloud project, enable Drive API.

Create OAuth 2.0 Client ID (Desktop app) credentials.

Download credentials.json and place it in the repo root.

On first run the app will open a browser for OAuth consent.

Run the app:

bash
Copy
Edit
streamlit run app.py
Open the Streamlit UI and follow instructions:

Authenticate with Google (browser will open).

Enter Meet ID / Meeting name or Drive folder id and click Run.

The pipeline downloads recordings for that Meet and processes them.

Important notes / tradeoffs
This pipeline processes recordings after the meeting — near real-time by polling Drive is possible (we can add), but live in-meeting capture is complex and fragile.

Speech diarization (speaker labeling) is approximate (Whisper timestamps help; for high quality diarization consider pyannote.audio).

OCR quality depends on slide/video resolution — more frequent frame sampling gives better capture but costs time.

LLM calls send text to external API if you use OpenAI — redact PII if required.
