from elasticsearch import Elasticsearch
import redis

# Configuración Elasticsearch
ES_CONFIG = {
    "host": "localhost",
    "port": 9200
}
INDEX_NAME = "eventos"

# Configuración Redis
REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}
TTL_SEGUNDOS = 3600  # 1 hora

# Conectar a Elasticsearch
es = Elasticsearch([f"http://{ES_CONFIG['host']}:{ES_CONFIG['port']}"])
if not es.ping():
    raise ValueError("No se puede conectar a Elasticsearch")

# Conectar a Redis
r = redis.Redis(**REDIS_CONFIG)

# Buscar todos los documentos
query = {
    "query": {
        "match_all": {}
    }
}

scroll = es.search(index=INDEX_NAME, body=query, scroll='2m', size=1000)
scroll_id = scroll['_scroll_id']
hits = scroll['hits']['hits']

contador = 0

while hits:
    for doc in hits:
        source = doc['_source']
        city = source.get('city')
        subtype = source.get('subtype')

        if city and subtype:
            cache_key = f"evento:{city}"
            r.setex(cache_key, TTL_SEGUNDOS, subtype)
            contador += 1

    scroll = es.scroll(scroll_id=scroll_id, scroll='2m')
    scroll_id = scroll['_scroll_id']
    hits = scroll['hits']['hits']

print(f"{contador} eventos seteados en Redis con TTL de {TTL_SEGUNDOS} segundos.")