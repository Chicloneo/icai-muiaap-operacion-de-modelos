# Semana 2 — Proyectos reproducibles con uv y Git

- **Clase 1 — [Assignment 2.1](../assignments/semana02_clase01_assignment.pdf):** crear el proyecto local `env-demo`, ejecutar una misma base de código en DEV/PRE/PRO, comprobarla con tests y registrar tres commits locales.

    - __Santi__: el assignment 2.1 está hecho en el repo ![primer-proyecto-uv](https://github.com/Chicloneo/primer-proyecto-uv)

- **Clase 2 — [Assignment 2.2](../assignments/semana02_clase02_assignment.pdf):** reorganizar el caso Wine de S1, comprobarlo y trabajar con una rama, `push` y pull request contra `main` del fork de la pareja.

| Fichero para la clase 2 | Uso |
| --- | --- |
| [`starter/WineQT.csv`](starter/WineQT.csv) | Dataset del caso Wine que se reorganiza como proyecto reproducible. |
| [`starter/train.py`](starter/train.py) | Punto de partida del entrenamiento que debe integrarse en la nueva estructura. |
| [`starter/test_train.py`](starter/test_train.py) | Test inicial para comprobar que el entrenamiento conserva su comportamiento. |

Los assignments contienen todo el recorrido; durante la práctica no hay otra documentación que consultar.


__Santi__: Explicación assignment 2.

- Hemos creado un proyecto uv con diferentes carpetas y scripts de python ejecutables, siguiendo una estructura ordenada y moderna mediante `uv`. 

- Para no tener conflictos con el proyecto uv "grande" `icai-muiaap-operacion-de-modelos` y otros entornos dentro del proyecto, ejecutamos el comando `--vcs none` al hacer `uv init`.

- Para que otra persona lo pueda instalar y ejecutar, debe descargar (o clonar) la carpeta `icai-muiaap-operacion-de-modelos/semana2/wine-quality-project`.

- Dicha persona ejecutará `uv run archivo.py`, y uv se encarga de resolver todos los posibles conflictos entre entornos, librerías, etc.

- Debe sustituir `archivo.py` por alguno de los que hemos añadido, como `train.py` o `test_train.py`.

#### ¿Cómo saber que el proyecto _funciona_?

```bash
uv run pytest
````

y debería devolver (en verde):

```bash
test_train.py .                                                                                      [100%]

============================================ 1 passed in 1.53s =============================================
```