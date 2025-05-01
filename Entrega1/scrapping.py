import requests
import pandas as pd
import time
import random

# -- Configuración general --

# Coordenadas aproximadas región Metropolitana
TOP = -33.2
BOTTOM = -33.8
LEFT = -71.0
RIGHT = -70.3

# Variación del mapa
DELTA = 0.09
META_EVENTOS = 10000

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

def construir_url(top, bottom, left, right):
    return f"https://www.waze.com/live-map/api/georss?top={top}&bottom={bottom}&left={left}&right={right}&env=row&types=alerts"

def consultar_cuadro(cuadro_top, cuadro_bottom, cuadro_left, cuadro_right):
    eventos_locales = []
    try:
        url = construir_url(cuadro_top, cuadro_bottom, cuadro_left, cuadro_right)
        response = requests.get(url, headers=HEADERS, timeout=10)
            # Función para ignorar las alertas sin subtype
        if response.status_code == 200:
            data = response.json()
            if 'alerts' in data:
                for alerta in data['alerts']:
                    street = alerta.get('street', 'Sin calle')
                    subtype = alerta.get('subtype', '')

                    if not subtype.strip():
                        continue  

                    eventos_locales.append({"street": street, "subtype": subtype})

        elif response.status_code == 429:
            print("Código 429: Demasiadas peticiones, durmiendo 10 segundos")
            time.sleep(10)

        else:
            print(f"Código de respuesta: {response.status_code}")

    except Exception as e:
        print(f"[Error consultando cuadro: {e}")

    time.sleep(random.uniform(0.5, 1.5))  
    return eventos_locales

# Función para "mover" el mapa en busca de eventos
def barrer_area():
    eventos = []
    lat = BOTTOM
    while lat < TOP:
        lng = LEFT
        while lng < RIGHT:
            cuadro_top = min(lat + DELTA, TOP)
            cuadro_bottom = lat
            cuadro_left = lng
            cuadro_right = min(lng + DELTA, RIGHT)

            eventos.extend(consultar_cuadro(cuadro_top, cuadro_bottom, cuadro_left, cuadro_right))
            lng += DELTA
        lat += DELTA
    return eventos

def guardar_eventos(eventos, archivo='eventos_ciclo.csv'):
    df = pd.DataFrame(eventos)
    df.to_csv(archivo, index=False)
    print(f"{len(eventos)} Eventos guardados en {archivo}")

# -- Programa principal --

todos_eventos = []

ciclo = 1
while len(todos_eventos) < META_EVENTOS:
    print(f"Iniciando barrido número: {ciclo}")
    eventos_ciclo = barrer_area()
    todos_eventos.extend(eventos_ciclo)

    if len(todos_eventos) // 1000 > (len(todos_eventos) - len(eventos_ciclo)) // 1000:
        print(f"Eventos recolectados: {len(todos_eventos)}")
  
    time.sleep(random.uniform(5, 10))
    ciclo += 1

guardar_eventos(todos_eventos)