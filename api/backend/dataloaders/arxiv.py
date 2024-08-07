from langchain_community.document_loaders import ArxivLoader
from langchain_core.documents.base import Document
import modal
# yanekyuk/bert-uncased-keyword-extractor -- this model is very fast but does not always find tokens. Perhaps it is the correct choice for general questions 
# ml6team/keyphrase-extraction-distilbert-inspec -- use this model for science-y questions: 

def supplementary_info(question_text: str, answer_text: str):
    
    find_keywords = modal.Function.lookup("find_keyword", "find_keywords")
    # convert question_text into a query for arxiv
        # extract topic from string
    query = find_keywords.remote(question_text)
    document = find_arxiv_document(query)
    

    # convert answer_text into a query for arxi

    return f"""
        Here is an arxiv article related to your question.
        The title is {document.metadata.get("Title")}. 
        The summary is {document.metadata.get("Summary")}.
        The authors are {document.metadata.get("Authors")}. 
        It was published in {document.metadata.get("Published")}.
        Would you like to hear the article?
        Would you like to hear a summary of a different article?"
        """

def find_arxiv_document(query_string) -> Document:
    docs = ArxivLoader(query=query_string, load_max_docs=1).load() 
    # consider adding a layer of LLM-comparison here.
        # LLM skims the paper summaries in reference to the question and then selects the most relevant summary.
            # Or, it says that no relevant summaries were found.
    # for now, select and return the top article.
    return docs[0]
# use langchain arxiv retriever to put documents into a vector db



# retrieve arxiv texts from vector db when user asks a question that would require an arxiv text
# ^^ do the same thing for topics that require data from other sources
