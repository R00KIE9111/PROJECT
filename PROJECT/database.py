import os
import pymysql
from azure.cosmos import CosmosClient
import uuid
from dotenv import load_dotenv

load_dotenv()

#COSMO DB
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = os.getenv("DATABASE_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = cosmos_client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

#SQL DB
def conexion():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

#FUNCIONES
def registrar_evento(usuario, accion, detalle, resultado="OK"):
    evento = {
        "id": str(uuid.uuid4()),
        "usuario": usuario,
        "accion": accion,
        "detalle": detalle,
        "resultado": resultado
    }
    container.create_item(body=evento)
