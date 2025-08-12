# transcribe.py
import whisper
from tqdm import tqdm

def transcribe_whisper(audio_path, model_name='small'):
    model = whisper.load_model(model_name)
    # returns segments with timestamps
    result = model.transcribe(audio_path, verbose=False)
    # result["segments"] is list of dicts with start, end, text
    return result
