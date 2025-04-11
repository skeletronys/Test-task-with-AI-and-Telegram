from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from .memory import get_memory
from .vector_store import load_vector_store
import os
from dotenv import load_dotenv

load_dotenv()


def create_agent():
    llm = ChatOpenAI(
        temperature=0.3,            # answer creativity
        model_name="gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # connect memory
    memory = get_memory()

    # create vector
    retriever = load_vector_store().as_retriever()

    # combine all
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        verbose=True  # logs
    )

    return qa_chain
