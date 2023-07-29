from backend.request_models import ChunkTextRequestDto
from langchain.text_splitter import CharacterTextSplitter


def chunk_text_handler(data: ChunkTextRequestDto):
    text_splitter = CharacterTextSplitter()
    return text_splitter.split_text(data.text)
