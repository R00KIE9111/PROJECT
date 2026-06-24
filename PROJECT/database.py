import pymysql
from azure.cosmos import CosmosClient
import uuid

#COSMO DB
COSMOS_ENDPOINT = "https://eva3-aws-azure.documents.azure.com/"
COSMOS_KEY = "SPtw9GduUqydI6HtdSgHkAE1AN1mhQGmQXqflZp5uWgrejwmlWHHVtkE7xGzqodNhxjCnoQdr8slACDbtmXN8w=="
DATABASE_NAME = "eva3-aws-azure"
CONTAINER_NAME = "container1"
cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = cosmos_client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

#SQL DB
def conexion():
    return pymysql.connect(
        host="eva3-aws-azure-db.c7saowikmas3.us-east-1.rds.amazonaws.com",
        user="admin",
        password="kt7GphhcBsqf.",
        database="project"
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
