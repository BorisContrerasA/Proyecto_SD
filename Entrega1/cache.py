import mysql.connector
import redis

# Configuración DB
DB_CONFIG = {
    'host': 'localhost',
    'user': 'waze_user',
    'password': 'wazepassword',
    'database': 'waze_db',
    'port': 3307
}

REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}

# Conexión a MySQL
db_conn = mysql.connector.connect(**DB_CONFIG)
db_cursor = db_conn.cursor()

# Conexión a Redis
r = redis.Redis(**REDIS_CONFIG)

# Leer todos los eventos
db_cursor.execute("SELECT street, subtype FROM eventos")
eventos = db_cursor.fetchall()

# Cargar en Redis
contador = 0
for street, subtype in eventos:
    if street and subtype:  
        cache_key = f"evento:{street}"
        r.set(cache_key, subtype)  
        contador += 1

print(f"{contador} eventos seteados en Redis.")

# Cerrar conexiones
db_cursor.close()
db_conn.close()