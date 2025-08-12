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


How to use (detailed)
Put credentials.json (OAuth client ID for Desktop app) in repo root.

pip install -r requirements.txt and install ffmpeg and tesseract.

Run streamlit run app.py. The app will prompt you to authenticate Google Drive on first use (it will open a browser).

In Google Meet, record the meeting (host or co-host must record). After meeting ends, the recording lands in Drive (usually My Drive/Meet Recordings).

In UI enter a distinctive part of the meeting name (or folder id) and click Run Pipeline.

Wait — the pipeline downloads the latest recording that matches and processes it. Outputs placed in output/report.json and output/ frame images and audio.

Extensions & Next Steps (I can implement for you if you want)
Real-time / near-real-time by polling Drive for a recording file as soon as it appears.

Speaker diarization using pyannote.audio (needs GPU or CPU heavy model).

Better frame timestamps by using ffprobe to map extracted frame filenames to exact timestamps.

Flowchart generation: create Graphviz DOT or Mermaid text using LLM prompt.

Automatic action-item extraction into a table with responsible persons and due dates (LLM).

Slack / Email notifier for result delivery.

Final notes & safety
Make sure you have permission to record meetings and process participant audio.

Be careful sending PII or confidential content to external LLMs like OpenAI — consider local LLM if privacy required.

The provided pipeline is best-effort: audio/video lengths and quality vary — test with short recordings first.
