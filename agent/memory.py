from langchain.memory import ConversationBufferMemory

def get_memory():
    memory = ConversationBufferMemory(
        memory_key="chat_history",  # key for save chat
        return_messages=True
    )
    return memory
