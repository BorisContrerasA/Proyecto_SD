#!/bin/bash
set -e

echo "[INFO] Esperando a que Elasticsearch esté disponible..."
until curl -s http://elasticsearch:9200 | grep -q cluster_name; do
  echo "⏳ Aún no disponible, esperando..."
  sleep 5
done

echo "✅ Elasticsearch disponible"

# Opcional: espera unos segundos más por seguridad
sleep 5

echo "[1/4] Ejecutando scrapping.py..."
# python3 scrapping.py

echo "[2/4] Ejecutando almacenamiento.py..."
python3 almacenamiento.py

echo "[3/4] Ejecutando filtrado con Pig..."
pig filtrar.pig

echo "[4/4] Ejecutando visualización..."
python3 visualizacion.py

exec /bin/bash