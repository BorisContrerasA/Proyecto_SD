#!/bin/bash

echo "▶️ Ejecutando script Pig desde contenedor Hadoop"

docker run --rm \
  -v "$(pwd):/scripts" \
  fluddeni/hadoop-pig \
  pig -x local /scripts/filtrar.pig

echo "Proceso Pig completado."