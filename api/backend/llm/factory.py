from os import environ
from backend.llm.hosted_openai_wrappers import summarize as hosted_openai_summarize, speech_to_text as hosted_openai_speech_to_text, ask_question as hosted_openai_ask_question
from backend.llm.modal_coqui_wrappers import text_to_speech as modal_coqui_text_to_speech
from backend.dataloaders.arxiv import supplementary_info as arxiv_supplementary_info

summarize_model = environ["SUMMARIZE_MODEL"].lower()
speech_to_text_model = environ["SPEECH_TO_TEXT_MODEL"].lower()
text_to_speech_model = environ["TEXT_TO_SPEECH_MODEL"].lower()


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


def build_text_to_speech():
    match text_to_speech_model:
        case "modal_coqui":
            return modal_coqui_text_to_speech
    raise Exception("Unsupported TEXT_TO_SPEECH_MODEL value")


def build_supplementary_info(question_type):
    match question_type:
        case "research_paper":
            return arxiv_supplementary_info
    raise Exception("Unsupported supplementary_info value")
