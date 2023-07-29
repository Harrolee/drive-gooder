from request_models import SummarizeRequestDto
from llm.factory import build_summarizer

def summarize_handler(data: SummarizeRequestDto):
    summarizer = build_summarizer()
    return summarizer(data.text)
