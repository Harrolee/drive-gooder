from langchain_community.utilities import ArxivAPIWrapper

def supplementary_info(question_text: str, answer_text: str):
    
    return """
        Here is an arxiv article related to your question.
        The title is "". The summary is "" and the authors are "".
        Would you like to hear the article? Or,
        would you like to hear a summary of a different article"
        """


def arxiv_wrapper_summarizer():
    ...


def play():
    arxiv = ArxivAPIWrapper()
    articles = arxiv.run("cnn")
# use langchain arxiv retriever to put documents into a vector db



# retrieve arxiv texts from vector db when user asks a question that would require an arxiv text
# ^^ do the same thing for topics that require data from other sources