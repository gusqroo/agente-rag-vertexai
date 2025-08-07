import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Función para obtener variable obligatoria
def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise EnvironmentError(f"La variable de entorno '{name}' no está definida o está vacía.")
    return value

# Variables requeridas
PROJECT_ID = get_env_variable("PROJECT_ID")
REGION = get_env_variable("REGION")
VERTEX_MODEL = get_env_variable("VERTEX_MODEL")
