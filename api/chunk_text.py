from request_models import ChunkTextRequestDto


def chunk_text_handler(input_text: ChunkTextRequestDto):
    return [letter for letter in input_text]
