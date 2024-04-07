from flask import send_file
from backend.request_models import ReadTextRequestDto
from backend.llm.factory import build_text_to_speech
import io


def get_audio_for_text_handler(data: ReadTextRequestDto):
    text_to_speech = build_text_to_speech()
    audio_content = text_to_speech(data.text, data.emotion, data.speed)

    file_contents = io.BytesIO(audio_content)
    file_contents.seek(0)

    return send_file(file_contents, mimetype="audio/wav", download_name="output.wav")
