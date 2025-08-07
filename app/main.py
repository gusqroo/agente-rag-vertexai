from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.chain import construir_chain
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Verificar credenciales de GCP
if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    raise EnvironmentError("La variable GOOGLE_APPLICATION_CREDENTIALS no está definida en el entorno.")

app = FastAPI(title="RAG Clínica Dental", version="1.0.0")
chain = construir_chain()

class QueryIn(BaseModel):
    pregunta: str

class Fuente(BaseModel):
    source: Optional[str] = None
    title: Optional[str] = None
    page: Optional[int] = None

class AnswerOut(BaseModel):
    respuesta: str
    fuentes: List[Fuente] = []

@app.get("/")
def home():
    return {"mensaje": "Servidor RAG activo"}

# Opción GET (retrocompatible con tu cliente actual)
@app.get("/preguntar", response_model=AnswerOut)
def preguntar_get(pregunta: str):
    try:
        result = chain({"query": pregunta})  # RetrievalQA espera 'query'
        respuesta = result["result"] if "result" in result else result.get("answer", "")
        fuentes = []
        for d in result.get("source_documents", []):
            meta = d.metadata or {}
            fuentes.append(Fuente(
                source=meta.get("source"),
                title=meta.get("title"),
                page=meta.get("page") or meta.get("page_number")
            ))
        return AnswerOut(respuesta=respuesta, fuentes=fuentes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Opción POST (recomendada)
@app.post("/preguntar", response_model=AnswerOut)
def preguntar_post(body: QueryIn):
    try:
        result = chain({"query": body.pregunta})
        respuesta = result["result"] if "result" in result else result.get("answer", "")
        fuentes = []
        for d in result.get("source_documents", []):
            meta = d.metadata or {}
            fuentes.append(Fuente(
                source=meta.get("source"),
                title=meta.get("title"),
                page=meta.get("page") or meta.get("page_number")
            ))
        return AnswerOut(respuesta=respuesta, fuentes=fuentes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

