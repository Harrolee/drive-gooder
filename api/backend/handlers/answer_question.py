import io
from typing import IO

from flask import send_file
from backend.request_models import QuestionTextRequestDto
from backend.llm.factory import build_speech_to_text, build_ask_question, build_text_to_speech, build_supplementary_info
from backend.handlers.classify_question import classify_question_type

def supplementary_info(question_text: str, answer_text: str):
    
    return """
        Here is an arxiv article related to your question.
        The title is "". The summary is "" and the authors are "".
        Would you like to hear the article? Or,
        would you like to hear a summary of a different article"
        """


def answer_question_handler(question_audio: IO, data: QuestionTextRequestDto):
    speech_to_text = build_speech_to_text()
    question_text = speech_to_text(question_audio)

    ask_question = build_ask_question()
    answer_text = ask_question(question_text, data.text)

    question_type = classify_question_type(question_text)
    supplementary_info = build_supplementary_info(question_type)
    followup_answer = supplementary_info(question_text, answer_text)
    # add follow-up answer:
        # "here is an arxiv article related to your question.
        # The title is "". The summary is "" and the authors are "".
        # Would you like to hear the article?
        # Or would you like to hear a summary of a different article"

    text_to_speech = build_text_to_speech()
    audio_content = text_to_speech(answer_text, data.emotion, data.speed)

    file_contents = io.BytesIO(audio_content)
    file_contents.seek(0)

    return send_file(file_contents, mimetype="audio/wav", download_name="output.wav")
