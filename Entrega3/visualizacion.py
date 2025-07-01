from elasticsearch import Elasticsearch
import redis
import os

# Configuración
ES_HOST = os.environ.get("ES_HOST", "localhost")
ES_PORT = os.environ.get("ES_PORT", "9200")
INDEX_NAME = "eventos"

# Conexión a Elasticsearch
es = Elasticsearch([f"http://{ES_HOST}:{ES_PORT}"])

# Conexión a Redis
REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}
r = redis.Redis(**REDIS_CONFIG)

def test_conexion():
    if not es.ping():
        raise ConnectionError("No se pudo conectar a Elasticsearch.")
    print("[INFO] Conexión exitosa a Elasticsearch.")

def buscar_eventos_por_tipo(tipo):
    cache_key = f"eventos_tipo:{tipo}"
    cached = r.get(cache_key)

    if cached:
        print(f"[CACHE] Resultados desde Redis para tipo '{tipo}':")
        print(cached.decode())
        return

    query = {
        "query": {
            "match": {
                "type": tipo
            }
        }
    }
    result = es.search(index=INDEX_NAME, body=query)

    eventos = [hit['_source'] for hit in result['hits']['hits']]
    print(f"[INFO] Se encontraron {len(eventos)} eventos del tipo '{tipo}':")
    for e in eventos:
        print(e)

    r.setex(cache_key, 3600, str(eventos))

def contar_por_ciudad():
    query = {
        "size": 0,
        "aggs": {
            "por_ciudad": {
                "terms": {
                    "field": "city.keyword",
                    "size": 10
                }
            }
        }
    }
    result = es.search(index=INDEX_NAME, body=query)
    print("[INFO] Cantidad de eventos por ciudad:")
    for bucket in result['aggregations']['por_ciudad']['buckets']:
        print(f"{bucket['key']}: {bucket['doc_count']}")

def eventos_entre_fechas(inicio, fin):
    query = {
        "query": {
            "range": {
                "timestamp": {
                    "gte": inicio,
                    "lte": fin
                }
            }
        }
    }
    result = es.search(index=INDEX_NAME, body=query)
    print(f"[INFO] Eventos entre {inicio} y {fin}:")
    for hit in result['hits']['hits']:
        print(hit['_source'])

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Consultas sobre índice 'eventos' en Elasticsearch")
    parser.add_argument("--tipo", help="Buscar eventos por tipo")
    parser.add_argument("--cuenta-ciudades", action="store_true", help="Contar eventos por ciudad")
    parser.add_argument("--rango-fechas", nargs=2, metavar=('inicio', 'fin'), help="Buscar eventos entre fechas (YYYY-MM-DD)")

    args = parser.parse_args()
    test_conexion()

    if args.tipo:
        buscar_eventos_por_tipo(args.tipo)
    elif args.cuenta_ciudades:
        contar_por_ciudad()
    elif args.rango_fechas:
        eventos_entre_fechas(args.rango_fechas[0], args.rango_fechas[1])