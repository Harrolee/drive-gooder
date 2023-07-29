from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from request_models import SummarizeRequestDto

llm = OpenAI(temperature=0)

text_splitter = CharacterTextSplitter()

def summarize_handler(data: SummarizeRequestDto):
    split_texts = text_splitter.split_text(data.text)

    docs = [Document(page_content=t) for t in split_texts]

    llm = OpenAI(temperature=0)

    chain = load_summarize_chain(llm, chain_type="map_reduce")

    summary = chain.run(docs)

    return summary
