# pipeline.py
import os, json
from google_drive import authenticate, list_recordings_for_meet, download_file
from audio import extract_audio_from_video, extract_frames
from transcribe import transcribe_whisper
from ocr import ocr_image
from merge import merge_transcript_and_screens
from llm_agent import summarize_with_openai

def process_meeting(meet_code, openai_key=None, credentials_json='credentials.json', folder_id=None):
    creds = authenticate(credentials_json)
    files = list_recordings_for_meet(creds, meet_code=meet_code, folder_id=folder_id)
    if not files:
        raise FileNotFoundError("No recordings found for the given meet code/folder.")
    # pick latest
    files_sorted = sorted(files, key=lambda x: x['createdTime'], reverse=True)
    selected = files_sorted[0]
    vid_path = os.path.join("output", selected['name'])
    download_file(creds, selected['id'], vid_path)
    audio_path = extract_audio_from_video(vid_path, out_audio="output/audio.wav")
    frames = extract_frames(vid_path, out_dir="output/frames", fps=0.33)  # 1 frame every 3 seconds
    # OCR frames
    frames_with_times = []
    # If using ffmpeg frame pattern, frames don't have timestamps; we can approximate timestamps by frame index * (1/fps)
    fps = 0.33
    for idx, fp in enumerate(frames):
        ts = idx / fps
        txt = ocr_image(fp)
        frames_with_times.append((ts, fp, txt))
    # Transcribe
    trans_result = transcribe_whisper(audio_path)
    segments = trans_result.get('segments', [])
    # Convert to simplified segments
    segments_simple = [{'start': s['start'], 'end': s['end'], 'text': s['text']} for s in segments]
    merged = merge_transcript_and_screens(segments_simple, frames_with_times)
    merged_text = "\n\n".join([f"[{m['start']:.1f}-{m['end']:.1f}] {m['text']}\nScreens: {len(m['screens'])}" for m in merged])
    llm_summary = None
    if openai_key:
        llm_summary = summarize_with_openai(merged_text, openai_key)
    report = {
        "file": selected,
        "transcript_segments": segments_simple,
        "frames": frames_with_times,
        "merged": merged,
        "llm_summary": llm_summary
    }
    out_path = "output/report.json"
    os.makedirs("output", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return report
