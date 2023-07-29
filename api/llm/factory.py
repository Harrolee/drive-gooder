from os import environ
from llm.openai_wrappers import summarize as openai_summarize

summarize_model = environ["SUMMARIZE_MODEL"].lower()

def build_summarizer():
    match summarize_model:
        case "openai":
            return openai_summarize
    raise Exception("Unsupported SUMMARIZE_MODEL value")
