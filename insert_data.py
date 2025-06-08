from pyspark.sql import SparkSession
import requests
import json

# URL del endpoint
url = 'http://localhost:8010/users'

# Cabeceras de la solicitud
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

# Crear una SparkSession
spark = SparkSession.builder.config("spark.eventLog.gcMetrics.youngGenerationGarbageCollectors", "G1 Concurrent GC") \
    .config("spark.eventLog.gcMetrics.oldGenerationGarbageCollectors", "G1 Concurrent GC") \
    .appName("Leer CSV en Spark") \
    .getOrCreate()

# Leer un archivo CSV
tb_claim_checklist_responses = spark.read.csv("data/tb_claim_checklist_responses.csv", header=True, inferSchema=True)
tb_claim_checklist_tasks = spark.read.csv("data/tb_claim_checklist_tasks.csv", header=True, inferSchema=True)
tb_claim = spark.read.csv("data/tb_claim.csv", header=True, inferSchema=True)
tb_holdingcompanies = spark.read.csv("data/tb_holdingcompanies.csv", header=True, inferSchema=True)
tb_policies = spark.read.csv("data/tb_policies.csv", header=True, inferSchema=True)
tb_poriskadditionalfloodinfos = spark.read.csv("data/tb_poriskadditionalfloodinfos.csv", header=True, inferSchema=True)
tb_users = spark.read.csv("data/tb_users.csv", header=True, inferSchema=True)  # Leer un archivo CSV en Spark



# Convertir el DataFrame a JSON
json_data = tb_users.toJSON().collect()  # Cada fila es un objeto JSON

# Iterar sobre cada fila del DataFrame y enviarla a la API
for row in json_data:
    # Convertir la fila a un diccionario de Python (si es necesario)

    row_data = json.loads(row)
    # Eliminar 'Admin_ID' y obtener su valor
    row_data.pop('Admin_ID', None)

        # Enviar la solicitud POST
    response = requests.post(url, headers=headers, json=row_data)
    try:
        # Verificar la respuesta
        if response.status_code == 201:
            print("Datos insertados correctamente.",response.json())
        else:
            print(f"Error al insertar datos: {response.status_code}")
    except:
        print(f"Error al insertar datos ")
