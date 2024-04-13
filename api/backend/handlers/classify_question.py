def classify_question_type(question_text: str):
    """
    Guess at the kind of supplementary information the user would appreciate.
    Some example types: research paper, medium article, recipe, news story
    """
    # how to implement? 

    #🏆- use vector-similarity to find the closest match in a list of possible answers
    # - Use a pre-trained model to classify the kind of question
    # - Use a general purpose llm to classify the kind of question
    return "research_paper"