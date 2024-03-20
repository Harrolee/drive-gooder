import io
import tempfile
from typing import IO
from langchain_openai import OpenAI as langchain_openai
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.chains.question_answering import load_qa_chain
from openai import OpenAI

openai_client = OpenAI()

def summarize(text: str):
    text_splitter = CharacterTextSplitter()
    split_texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in split_texts]

    llm = langchain_openai(temperature=0, model="gpt-3.5-turbo-instruct")

    chain = load_summarize_chain(llm, chain_type="map_reduce")

    summary = chain.invoke(docs)
    return summary

def speech_to_text(data: IO):
    # this is a wav file
    print(f'\n\n\n unicorns \n\n\n')
    print(f'\n\n\n {type(data)} \n\n\n')
    print(f'\n\n\n {dir(data)} \n\n\n')
    print(f'\n\n\n unicorns \n\n\n')

    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        # Save the contents of the FileStorage object to the temporary file
        data.save(temp_file.name)
        # Open the temporary file as an io.IOBase instance
        with open(temp_file.name, 'rb') as f:
            io_base_instance = io.BytesIO(f.read())

    transcript = openai_client.audio.transcriptions.create(file=io_base_instance, model="whisper-1")

    return transcript

def ask_question(question: str, text: str):
    chain = load_qa_chain(langchain_openai(temperature=0, model="gpt-3.5-turbo"), chain_type="stuff")

    text_splitter = CharacterTextSplitter()
    docs = text_splitter.create_documents(texts = [text])

    result = chain({"input_documents": docs, "question": question}, return_only_outputs=True)

    return result["output_text"]
