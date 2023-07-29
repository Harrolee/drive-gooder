from typing import IO
from backend.request_models import QuestionTextRequestDto
from backend.llm.factory import build_speech_to_text, build_ask_question


def answer_question_handler(question_audio, data: QuestionTextRequestDto):
    speech_to_text = build_speech_to_text()
    question_text = speech_to_text(question_audio)

    ask_question = build_ask_question()
    answer = ask_question(question_text, data.text)

    return answer
