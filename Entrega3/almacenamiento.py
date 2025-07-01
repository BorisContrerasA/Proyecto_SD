from elasticsearch import Elasticsearch, helpers
import pandas as pd
from datetime import datetime

# Conectar a Elasticsearch
es = Elasticsearch("http://elasticsearch:9200")

# Verificar conexión
if not es.ping():
    raise ValueError("No se puede conectar a Elasticsearch")

# Crear el índice "eventos" si no existe
index_name = "eventos"

mapping = {
    "mappings": {
        "properties": {
            "city": {"type": "keyword"},
            "subtype": {"type": "keyword"},
            "type": {"type": "keyword"},
            "x": {"type": "float"},
            "y": {"type": "float"},
            "timestamp": {"type": "date"}
        }
    }
}

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)
    print(f"Índice '{index_name}' creado.")
else:
    print(f"Índice '{index_name}' ya existe.")

# Leer CSV y preparar datos
df = pd.read_csv("tiempo1.csv")

# Asegurar tipos
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["x"] = df["x"].astype(float)
df["y"] = df["y"].astype(float)

# Crear acciones bulk
actions = [
    {
        "_index": index_name,
        "_source": {
            "city": row["city"],
            "subtype": row["subtype"],
            "type": row["type"],
            "x": row["x"],
            "y": row["y"],
            "timestamp": row["timestamp"].isoformat()
        }
    }
    for _, row in df.iterrows()
]

# Insertar en bloque
helpers.bulk(es, actions)
print(f"{len(actions)} documentos insertados en el índice '{index_name}'.")