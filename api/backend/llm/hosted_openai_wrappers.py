from langchain import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.chains.question_answering import load_qa_chain
import openai

def summarize(text: str):
    text_splitter = CharacterTextSplitter()
    split_texts = text_splitter.split_text(text)

    docs = [Document(page_content=t) for t in split_texts]

    llm = OpenAI(temperature=0)

    chain = load_summarize_chain(llm, chain_type="map_reduce")

    summary = chain.run(docs)

    return summary

def speech_to_text(data: object):
    transcript = openai.Audio.translate("whisper-1", data)
    return transcript

def ask_question(question: str, text: str):
    chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")

    text_splitter = CharacterTextSplitter()
    docs = text_splitter.create_documents(texts = [text])

    result = chain({"input_documents": docs, "question": question}, return_only_outputs=True)

    return result["output_text"]
