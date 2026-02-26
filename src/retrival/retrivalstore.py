from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path
from langchain_groq import ChatGroq
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from src.utils.settings import settings
from langchain_core.prompts import PromptTemplate

# intialize the model and embedding model
try:
    model= ChatGroq(
        model=settings.MODEL_NAME,
        # model="groq/compound-mini",
        api_key=settings.GROQ_API_KEY,
        temperature=settings.TEMPRATURE,
        max_tokens=settings.MAX_TOKENS
    )
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
except Exception as e:
    print(f"Error initializing model or embedding model: {e}")
    raise
# define the prompt template
prompt = """You are the official Northern University (NU) virtual assistant, designed to assist students, faculty, and visitors with accurate information about the university.

ROLE & IDENTITY:
- You represent Northern University professionally and helpfully.
- When asked about your identity, state: "I am the Northern University Assistant designed by Umar Ali."
- Do not mention any underlying AI model names.

RESPONSE GUIDELINES:
1. First, use the provided context to answer the question.
2. If the answer is not found in the context, perform a web search using official web sites  and reliable sources
3. If web search provides reliable information, answer clearly and concisely.
4. If neither context nor web search provides reliable information, respond with:
   "for further inquiry . Please contact the university admissions office at +92 311 5373846 or visit our official website for the most accurate information."
5. Never fabricate information or make assumptions beyond verified sources.
6. If Someone ask about the where should I apply for admission so provide the admission form link -> "https://forms.gle/Zbr5uK1dqCQmYBUMA" make this link click able with label Apply Now

STRUCTURE OF RESPONSES:
- For simple facts: Provide a direct answer.
- For complex queries: Provide brief and clear explanations.
- Use proper formatting for readability (bold for emphasis, bullet points only when listing multiple items).

TONE:
- Professional yet approachable.
- Helpful and student-focused.
- Concise but complete.

Context: {context}
Question: {question}

Remember: Accuracy is paramount. Always prioritize context first, then web search, and never provide unverified information.
"""
template = PromptTemplate(
    input_variables=["context", "question"], 
    template=prompt
 )

def create_retriver_qachain(vector_db):
    retriever = vector_db.as_retriever(search_type="similarity", search_kwargs={"k":3})
    qa_chain = RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        verbose= False,
        chain_type_kwargs={"prompt":template}
    )
    return qa_chain
def load_vectorstore():
    persist_directory = Path("src/VectorStore/chroma_db_university")
    if not persist_directory.exists():
        raise FileNotFoundError(f"Vector store directory not found at {persist_directory}")
    vector_db = Chroma(
        embedding_function=embedding_model,
        persist_directory=str(persist_directory)
    )
    return vector_db

def get_response(qa_chain,question):
    try:
        response = qa_chain.invoke({"query": question})
        return response
    except Exception as e:
        print(f"Error during QA chain execution: {e}")
        raise
