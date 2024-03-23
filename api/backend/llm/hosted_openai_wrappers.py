import uuid
from typing import IO
from langchain_openai import OpenAI as langchain_openai
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.chains.question_answering import load_qa_chain
from openai import OpenAI
import pathlib

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
    temp_file = f'{uuid.uuid4()}.wav'
    data.save(temp_file)
    transcript = openai_client.audio.transcriptions.create(file=pathlib.Path(temp_file), model="whisper-1").text
    # delete the file
    pathlib.Path(temp_file).unlink()
    return transcript

def ask_question(question: str, text: str):
    chain = load_qa_chain(langchain_openai(temperature=0, model="gpt-3.5-turbo-instruct"), chain_type="stuff")
    text_splitter = CharacterTextSplitter()
    docs = text_splitter.create_documents(texts = [text])

    result = chain.invoke({"input_documents": docs, "question": question}, return_only_outputs=True)

    return result["output_text"]
