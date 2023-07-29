from os import environ
from llm.hosted_openai_wrappers import summarize as hosted_openai_summarize, speech_to_text as hosted_openai_speech_to_text, ask_question as hosted_openai_ask_question

summarize_model = environ["SUMMARIZE_MODEL"].lower()
speech_to_text_model = environ["SPEECH_TO_TEXT_MODEL"].lower()
question_model = environ["QUESTION_MODEL"].lower()

def build_summarizer():
    match summarize_model:
        case "hosted_openai":
            return hosted_openai_summarize
    raise Exception("Unsupported SUMMARIZE_MODEL value")

def build_speech_to_text():
    match speech_to_text_model:
        case "hosted_openai":
            return hosted_openai_speech_to_text
    raise Exception("Unsupported SPEECH_TO_TEXT_MODEL value")

def build_ask_question():
    match question_model:
        case "hosted_openai":
            return hosted_openai_ask_question
    raise Exception("Unsupported QUESTION_MODEL value")