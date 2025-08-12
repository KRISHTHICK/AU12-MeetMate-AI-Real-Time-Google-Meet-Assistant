# app.py
import streamlit as st
from pipeline import process_meeting
import os, json

st.set_page_config(page_title="MeetMate Agent", layout="wide")
st.title("MeetMate Agent — Process Google Meet Recordings")

st.write("This app downloads a Google Meet recording from your Drive (you will authenticate), extracts audio and frames, transcribes, OCRs, and summarizes.")

meet_code = st.text_input("Enter meet code or a unique part of meeting name (e.g. 'Project Phoenix 2025-08-01'):")
folder_id = st.text_input("Optional: Google Drive folder id where recordings are stored (leave blank to search whole Drive):")
use_llm = st.checkbox("Use OpenAI for final summary", value=False)
openai_key = ""
if use_llm:
    openai_key = st.text_input("OpenAI API key", type="password")

if st.button("Run Pipeline"):
    if not meet_code:
        st.error("Please enter a meet code / meeting name fragment.")
    else:
        st.info("This may take several minutes depending on recording length.")
        try:
            report = process_meeting(meet_code, openai_key if use_llm else None, folder_id=folder_id or None)
            st.success("Processing complete. Report saved to output/report.json")
            st.json(report.get('llm_summary') or {"note":"LLM summary not generated"})
            st.markdown("### Transcript segments (first 10)")
            st.write(report['transcript_segments'][:10])
            st.markdown("### Sample OCR from frames")
            for ts, fp, txt in report['frames'][:5]:
                st.write(f"ts={ts:.1f}s ({os.path.basename(fp)})")
                st.write(txt[:400])
        except Exception as e:
            st.error(f"Pipeline failed: {e}")
