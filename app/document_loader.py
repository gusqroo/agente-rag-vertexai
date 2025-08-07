from langchain_community.document_loaders import PyPDFLoader

def cargar_documentos():
    loader = PyPDFLoader("app/files/dentistarag.pdf")
    documentos = loader.load()
    return documentos
