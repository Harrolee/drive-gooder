from typing import BinaryIO
from flask import send_file
from backend.request_models import ReadTextRequestDto
from backend.llm.factory import build_text_to_speech


def get_audio_for_text_handler(data: ReadTextRequestDto):
    text_to_speech = build_text_to_speech()
    audio_content = text_to_speech(data.text, data.emotion, data.speed)

    buffer = BinaryIO()
    buffer.write(audio_content)
    buffer.seek(0)

    # TODO: Figure out why this is returning an emtpy file
    return send_file(buffer, mimetype="audio/wav", download_name="output.wav")
