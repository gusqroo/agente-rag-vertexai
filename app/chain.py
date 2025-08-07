import os
from dotenv import load_dotenv

from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate

from app.document_loader import cargar_documentos

load_dotenv()

embedding_model_name = os.getenv("VERTEXAI_EMBEDDING_MODEL", "gemini-embedding-001")
llm_model_name = os.getenv("VERTEXAI_LLM_MODEL", "gemini-2.5-flash-lite")

# --- System Prompt (ajústalo al tono que quieras) ---
RAG_SYSTEM_PROMPT = (
    "Eres un asistente especializado en una clínica dental.\n"
    "Responde con precisión, claridad y tono profesional.\n"
    "Usa exclusivamente la información del contexto recuperado; "
    "si no hay evidencia suficiente, indica que no cuentas con datos en los documentos.\n"
    "Cuando corresponda, incluye una referencia breve (por ejemplo, el nombre del archivo o título)."
)

# Prompt para RetrievalQA: RetrievalQA inyecta {context} y {question}
QA_PROMPT = ChatPromptTemplate.from_messages([
    ("system", RAG_SYSTEM_PROMPT),
    ("human", "Contexto:\n{context}\n\nPregunta: {question}")
])

def construir_chain():
    # Embeddings (Vertex AI)
    embedding = VertexAIEmbeddings(model_name=embedding_model_name)

    # Vector store local (FAISS)
    vectorstore_dir = "app/vectores_dental"
    index_path = os.path.join(vectorstore_dir, "index.faiss")
    if not os.path.exists(index_path):
        docs = cargar_documentos()
        vectorstore = FAISS.from_documents(docs, embedding)
        vectorstore.save_local(vectorstore_dir)
    else:
        vectorstore = FAISS.load_local(vectorstore_dir, embedding, allow_dangerous_deserialization=True)

    # LLM (Vertex AI)
    llm = ChatVertexAI(model=llm_model_name, temperature=0.2)

    # RetrievalQA con System Prompt y retorno de fuentes
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff",
        chain_type_kwargs={"prompt": QA_PROMPT},
        return_source_documents=False,  # útil para mostrar evidencias
    )

    return chain

