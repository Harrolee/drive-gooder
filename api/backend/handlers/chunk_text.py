from backend.request_models import ChunkTextRequestDto
from langchain.text_splitter import TokenTextSplitter


def chunk_text_handler(data: ChunkTextRequestDto):
    text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=0)
    return text_splitter.split_text(data.text)
