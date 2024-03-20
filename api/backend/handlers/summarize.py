import io

from flask import send_file
from backend.request_models import SummarizeRequestDto
from backend.llm.factory import build_summarizer, build_text_to_speech


def summarize_handler(data: SummarizeRequestDto):
    summarizer = build_summarizer()
    summary = summarizer(data.text)
    apology_string = "Apologies, friendo. We could not summarize that for you."
    summary_text = summary.get('output_text', apology_string)

    text_to_speech = build_text_to_speech()
    audio_content = text_to_speech(summary_text, data.emotion, data.speed)
    file_contents = io.BytesIO(audio_content)
    file_contents.seek(0)

    return send_file(file_contents, mimetype="audio/wav", download_name="output.wav")
