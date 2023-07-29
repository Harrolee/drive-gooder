from langchain import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

def summarize(text: str):
    text_splitter = CharacterTextSplitter()
    split_texts = text_splitter.split_text(text)

    docs = [Document(page_content=t) for t in split_texts]

    llm = OpenAI(temperature=0)

    chain = load_summarize_chain(llm, chain_type="map_reduce")

    summary = chain.run(docs)

    return summary
