from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path



def load_docs():
    loader = TextLoader("src/data/university_data.txt")
    documents = loader.load()
    return documents

def create_vectorstore(documents):
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=["###", "---", "\n\n", "\n", "|"]
    )

    splits = text_splitter.split_documents(documents)

    persist_directory = Path("src/VectorStore/chroma_db_university")
    persist_directory.parent.mkdir(parents=True, exist_ok=True)

    vector_db = Chroma.from_documents(
        documents=splits,
        embedding=embedding_model,
        persist_directory=str(persist_directory),
    )

    return vector_db

if __name__ == "__main__":
    documents = load_docs()
    vector_db = create_vectorstore(documents)
    print("Vector store created and persisted successfully.")
