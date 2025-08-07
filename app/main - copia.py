from fastapi import FastAPI, HTTPException
from app.chain import construir_chain
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Verificar que la variable esencial esté presente
if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    raise EnvironmentError("La variable GOOGLE_APPLICATION_CREDENTIALS no está definida en el entorno.")

app = FastAPI()
chain = construir_chain()

@app.get("/")
def home():
    return {"mensaje": "Servidor RAG activo"}

@app.get("/preguntar/")
def preguntar(pregunta: str):
    try:
        respuesta = chain.run(pregunta)
        return {"respuesta": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
