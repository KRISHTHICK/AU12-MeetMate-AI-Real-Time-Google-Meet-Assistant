# audio.py
import ffmpeg
import os

def extract_audio_from_video(video_path, out_audio="output/audio.wav"):
    os.makedirs(os.path.dirname(out_audio), exist_ok=True)
    # convert to mono 16k WAV for whisper
    (
        ffmpeg
        .input(video_path)
        .output(out_audio, ac=1, ar='16000', vn=None)
        .overwrite_output()
        .run(quiet=True)
    )
    return out_audio

def extract_frames(video_path, out_dir="output/frames", fps=0.5):
    # extract frames at fps frames per second (e.g., 0.5 -> 1 frame every 2 seconds)
    os.makedirs(out_dir, exist_ok=True)
    # use ffmpeg -r to sample
    out_pattern = os.path.join(out_dir, "frame_%05d.jpg")
    (
        ffmpeg
        .input(video_path)
        .filter('fps', fps)
        .output(out_pattern, vsync=0)
        .overwrite_output()
        .run(quiet=True)
    )
    # list files
    frames = sorted([os.path.join(out_dir, f) for f in os.listdir(out_dir) if f.startswith("frame_")])
    return frames
