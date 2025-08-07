import os
from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from app.document_loader import cargar_documentos
from dotenv import load_dotenv

load_dotenv()

embedding_model_name = os.getenv("VERTEXAI_EMBEDDING_MODEL", "gemini-embedding-001")
llm_model_name = os.getenv("VERTEXAI_LLM_MODEL", "gemini-2.5-flash-lite")

def construir_chain():
    embedding = VertexAIEmbeddings(model_name=embedding_model_name)

    if not os.path.exists("app/vectores_dental/index.faiss"):
        docs = cargar_documentos()
        vectorstore = FAISS.from_documents(docs, embedding)
        vectorstore.save_local("app/vectores_dental")
    else:
        vectorstore = FAISS.load_local("app/vectores_dental", embedding, allow_dangerous_deserialization=True)

    llm = ChatVertexAI(model=llm_model_name, temperature=0.3)
    retriever = vectorstore.as_retriever()
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return chain
