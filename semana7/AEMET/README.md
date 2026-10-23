# Semana 7 - Práctica AEMET (Requests + AEMET)

## ¿Qué hace esta práctica?

Esta práctica es una introducción a las APIs (_Application Programming Interface_). Para ello utilizamos la librería `requests` de Python. En particular, hacemos un _request_ a la API de la AEMET (Agencia Estatal de Meteorología), para obtener datos sobre las temperaturas de cada día durante el mes de Octubre en Ciudad Universitaria, Madrid.

Desde `AEMET/`, debe ejecutarse el siguiente comando:

```bash
uv run src/aemet/oct_19_ciu.py
```

Ello devolverá un `.csv` en una carpeta temporal con los datos citados.

# Comentarios profesor

Práctica complementaria de la semana 7: hacer peticiones HTTP con Python y la
librería `requests` contra la API de la AEMET.

- Enunciado: [enunciado_aemet.pdf](enunciado_aemet.pdf)
  (también en `assignments/semana07_aemet_assignment.pdf`).

## Qué se pide

1. Crear un entorno virtual para el proyecto e instalar `requests`.
2. Solicitar una API key en la web de la AEMET (guárdala en una variable de
   entorno; no la subas al repositorio).
3. Llamar con `requests` al inventario de estaciones, buscar la estación
   "MADRID, CIUDAD UNIVERSITARIA" y obtener su `indicativo` (idema).
4. Llamar a las climatologías diarias de esa estación para octubre de 2019.

La API key se pasa como query string (`api_key`).
