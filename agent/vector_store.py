from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

def load_vector_store():
    """
    Create vector DB used knowledge.txt.
    """
    with open("data/knowledge.txt", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        raise ValueError(" Файл knowledge.txt порожній або нечитабельний!")

    # split text
    text_splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    texts = text_splitter.split_text(content)

    if not texts:
        raise ValueError(" Текст не розбито на частини. Перевір файл з інформацією.")

    # create documeent
    documents = [Document(page_content=t) for t in texts]

    # generate vector used OpenAI
    embeddings = OpenAIEmbeddings()

    # Create FAISS vector DB
    vectorstore = FAISS.from_documents(documents, embeddings)

    return vectorstore
