from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate

_template = """Given the following chat history and a follow up question, rephrase the follow up question to be standalone.

Chat history:
{chat_history}
Follow up question: {question}
Standalone question:  """
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}
Helpful answer:  """
QA_PROMPT = ChatPromptTemplate.from_template(prompt_template)
