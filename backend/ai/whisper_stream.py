import whisper, base64, tempfile

model = whisper.load_model("base")

def transcribe_audio(data_url):
    # Fallback mode for Windows without torch
    return "Voice transcription disabled (fallback mode)"

