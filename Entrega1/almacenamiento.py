import pandas as pd
import mysql.connector

# Cargar CSV
df = pd.read_csv("eventos_ciclo.csv")

# Conexión a mysql
conn = mysql.connector.connect(
    host="localhost",
    user="waze_user",
    password="wazepassword",
    port=3307,
    charset='utf8mb4'  
)

cursor = conn.cursor()

cursor.execute("""
    CREATE DATABASE IF NOT EXISTS waze_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
""")
print("[INFO] Base de datos 'waze_db' verificada o creada.")


conn.database = 'waze_db'

# Crear tabla eventos si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    street VARCHAR(255) CHARACTER SET utf8mb4,
    subtype VARCHAR(255) CHARACTER SET utf8mb4
);
""")
print("[INFO] Tabla 'eventos'creada.")

# Insertar datos del CSV
for index, row in df.iterrows():
    cursor.execute(
        "INSERT INTO eventos (street, subtype) VALUES (%s, %s)",
        (row['street'], row['subtype'])
    )

conn.commit()
print(f"{len(df)} eventos insertados.")

cursor.close()
conn.close()
