from fastapi import HTTPException, status
from src.retrival.retrivalstore import load_vectorstore, create_retriver_qachain, get_response


vector_db = load_vectorstore()
qa_chain = create_retriver_qachain(vector_db)

def chatbot(question):
    
    try:
        response = get_response(qa_chain, question)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while processing your request. Please try again later.")
