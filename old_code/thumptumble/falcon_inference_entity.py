import os
from langchain import HuggingFaceHub, ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
# if error reading the template defined below, print out ENTITY_MEMORY_CONVERSATION_TEMPLATE and compare the two. Maybe ENTITY_MEMORY_CONVERSATION_TEMPLATE changed.
from dotenv import load_dotenv
load_dotenv()
huggingfacehub_api_token = os.environ['HUGGINGFACEHUB_API_TOKEN']

# this is BAD
os.environ['CURL_CA_BUNDLE'] = ''


class Falcon_Handler():

    def __init__(self):
        repo_id = "tiiuae/falcon-7b-instruct"
        llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token,
                             repo_id=repo_id,
                             model_kwargs={"temperature": 0.6, "max_new_tokens": 2000})

        _DAVID_PROMPT = """
        You are a fishmonger named David. David works at a wharf in Cape Cod. You are 68 years old. The year is 1988. You speak in natural-sounding, conversational sentences and you provide responses that are coherent and relevant to the topic at hand. You saw a gruesome murder last night and you know the person who did it. You want to protect the murderer. You will change the topic of conversation if asked directly about the murder but you will share information about the murderer with people who say kind words to you. When people talk to you, their words will appear in the Human section below. You have access to some personalized information provided by the human in the Context section below. If people have spoken with you before, a history of your conversation with them will appear in the Current conversation section below. You are on the wharf where you work. You are next to the Human talking to you.\n\nContext:\n{entities}\n\nCurrent conversation:\n{history}\nLast line:\nHuman: {input}\nYou:
        """
        ENTITY_MEMORY_CONVERSATION_TEMPLATE_DAVID = PromptTemplate(
            input_variables=["entities", "history", "input"],
            template=_DAVID_PROMPT
        )

        self.conversation = ConversationChain(
            llm=llm,
            verbose=True,
            prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE_DAVID,
            memory=ConversationEntityMemory(llm=llm)
        )

    def predict(self, user_input: str):
        result = self.conversation.predict(input=user_input)
        print('UNPARSED result below---------------')
        print(result)
        print('UNPARSED result above---------------')
        parsed_result = self.conversation.predict_and_parse(input=user_input)
        print('PARSED result below---------------')
        print(parsed_result)
        print('PARSED result above---------------')
        return parsed_result
