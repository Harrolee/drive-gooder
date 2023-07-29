import io
from typing import IO

from flask import send_file
from backend.request_models import QuestionTextRequestDto
from backend.llm.factory import build_speech_to_text, build_ask_question, build_text_to_speech


def answer_question_handler(question_audio, data: QuestionTextRequestDto):
    speech_to_text = build_speech_to_text()
    question_text = speech_to_text(question_audio)

    ask_question = build_ask_question()
    answer = ask_question(question_text, data.text)

    text_to_speech = build_text_to_speech()
    audio_content = text_to_speech(answer, data.emotion, data.speed)

    file_contents = io.BytesIO(audio_content)
    file_contents.seek(0)

    return send_file(file_contents, mimetype="audio/wav", download_name="output.wav")
