# Proyecto SD: Entrega 3
## Para esta entrega se presenta la implementacion final del sistema.
### 1. Primero compilar el dockerfile para setear el entorno
```
docker build -t entrega3_app .
```
### 2. Finalizado el dockerfile se debe realizar el docker compose.
```
docker compose up --build
```
### 2.1 En caso de haber problemas de permisos
```
chmod +x start.sh
```
### 2.2 En caso de haber problemas con el compose
```
docker compose down -v
```
### Luego reaplicar compose up.
