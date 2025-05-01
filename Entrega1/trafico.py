import random
import mysql.connector
import redis

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="waze_user",
    password="wazepassword",
    database="waze_db",
    port=3307
)

cursor = db.cursor(buffered=True)

# Conexión a Redis
cache = redis.Redis(host='localhost', port=6379, db=0)

# Función para insertar en cache 
def insert_in_cache(key, value):
    cache.set(key, value)
    keys = cache.keys('*')

# Traer todos los datos de la base
cursor.execute("SELECT street, subtype FROM eventos")
eventos = cursor.fetchall()

# Generar tráfico sintético
def RandomDist(eventos, n=1000):
    return random.choices(eventos, k=n)

def FreqDist(eventos, n=1000):
    street_subtype_counts = {}
    for event in eventos:
        street_subtype_counts[event] = street_subtype_counts.get(event, 0) + 1
    
    events, weights = zip(*street_subtype_counts.items())
    total = sum(weights)
    probabilities = [w/total for w in weights]
    
    return random.choices(events, weights=probabilities, k=n)

# Calcular tasa de aciertos del cache
def CalcularHitrate(name, queries):
    hits = 0
    total = 0
    for street, subtype in queries:
        key = f"{street}:{subtype}"
        if cache.exists(key):
            hits += 1
        else:
            # Si no está en cache, buscar en la base de datos
            cursor.execute("SELECT street, subtype FROM eventos WHERE street=%s AND subtype=%s", (street, subtype))
            result = cursor.fetchone()
            if result:
                insert_in_cache(key, f"Street: {street}, Subtype: {subtype}")
        total += 1
    
    hit_rate = (hits / total) * 100
    print(f"Patrón {name}: {hit_rate:.2f}% de acierto en cache")

# -----------------
# Ejecución
# -----------------

print("Realizando pruebas de tráfico sintético:")

queries_random = RandomDist(eventos, n=1000)
queries_freq = FreqDist(eventos, n=1000)

CalcularHitrate("Random", queries_random)
CalcularHitrate("Frecuencia", queries_freq)

cursor.close()
db.close()