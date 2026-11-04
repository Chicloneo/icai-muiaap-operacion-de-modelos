## `api_key_demo.py`

En la terminal, desde examples:

```bash
uv run fastapi dev api_key_demo.py
```

En otra terminal (sin eliminar la primera):

```bash
 curl -i -X POST http://127.0.0.1:8000/v1/scores -H "Content-Type: application/json" -d '{"age": 42, "income": 38000}'
```

Estos ejemplos están al principio de `api_key_demo.py`.

`[url]/docs` para la documentación de la API

## `jwt_demo.py`

```bash 
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/token -H "Content-Type: application/json" -d '{"sub": "Santi"}' | jq -r .access_token)
```

```bash 
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/token -H "Content-Type: application/json" -d '{"sub": "Santi"}' | jq -r .access_token)

echo $TOKEN  

curl -i http://127.0.0.1:8000/v1/me -H "Authorization: Bearer $TOKEN"
```

En internet: jwt decoder 

y añadir `TOKEN`

## CORS
```bash
uv run fastapi dev examples/cors_demo.py

curl -i -X OPTIONS http://127.0.0.1:8000/v1/scores 
      -H "Origin: http://localhost:8501" 
      -H "Access-Control-Request-Method: POST" 
      -H "Access-Control-Request-Headers: content-type,x-api-key"
```

## locust y limit

Iniciamos la API limits

```bash
DEMO_API_KEY=demo-limits-key DEMO_RATE_LIMIT_PER_MINUTE=60 \
  uv run fastapi dev examples/limits_demo.py
```

En otra terminal

```bash
LOCUST_API_KEY=demo-limits-key uv run --group load locust \
      -f examples/locustfile.py -u 20 -r 5 -t 1m \
      --host http://127.0.0.1:8000
```

y pulsamos enter. Si falla, abrir `http://localhost:8089`, y personalizar las peticinoes. Locust es una librería Python para simular APIs y ver su comportamiento (sobre todo en casos de estrés).