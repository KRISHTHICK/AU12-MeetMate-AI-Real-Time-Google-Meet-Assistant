# merge.py
from bisect import bisect_left

def merge_transcript_and_screens(transcript_segments, frames_with_times):
    """
    transcript_segments: list of {start, end, text}
    frames_with_times: list of (timestamp_sec, frame_path, text)
    We'll assign screen texts to nearest transcript segment by timestamp.
    """
    merged = []
    # Create list of segment start times for binary search
    starts = [seg['start'] for seg in transcript_segments]
    for seg in transcript_segments:
        attached_screens = []
        for ts, frame_path, frame_text in frames_with_times:
            if seg['start'] <= ts <= seg['end']:
                attached_screens.append({"time": ts, "frame": frame_path, "ocr": frame_text})
        merged.append({
            "start": seg['start'],
            "end": seg['end'],
            "text": seg['text'],
            "screens": attached_screens
        })
    return merged
