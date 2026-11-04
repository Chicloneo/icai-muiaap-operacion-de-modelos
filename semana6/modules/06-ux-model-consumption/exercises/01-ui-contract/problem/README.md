# Práctica 01 — Diseñar una interfaz de inferencia operable

**Modalidad:** parejas · **Duración:** 45–60 minutos

## Objetivo

Partir de la app básica de S5 y convertirla, primero visualmente, en una
interfaz que comunique una inferencia. Decidiréis qué debe persistir entre
reruns, qué evento provoca cada transición y qué debe ver la persona mientras
se sirve una predicción.

No rediseñéis el formulario de S5 ni añadáis lógica de inferencia. La práctica
es una app Streamlit: el trabajo es observarla, modificar decisiones de
presentación justificadamente y especificar la evolución que se implementará
en el taller.

## Material

- [Laboratorio visual Streamlit](ui_playground.py): actividad principal.
- [Notebook del alumnado](01-estado-streamlit-alumno.ipynb): hoja de trabajo
  y evidencia de las decisiones.
- Vuestra app de S5 o la [solución base de S5](../../../../../../semana5/modules/05-streamlit-basic-model-ui/solutions/02-first-streamlit/README.md).
- Contrato de salida y manifiesto de [S4](../../../../../../semana4/assets/04-model-packaging/manifest_example.json).

## Ejecutar el laboratorio

Desde `semana6`:

```bash
uv sync --extra app
uv run streamlit run modules/06-ux-model-consumption/exercises/01-ui-contract/problem/ui_playground.py
```

Seleccionad los cinco escenarios. Después, cambiad una decisión visual por
pareja —por ejemplo, un mensaje, la jerarquía de métricas o el detalle de
trazabilidad— y explicad qué problema de consumo del modelo resuelve. No
modifiquéis las constantes de ejemplo para «mejorar» la predicción.

## Entrega

### 1. Estado de sesión

Completad una tabla:

| Clave o recurso | Dónde vive | ¿Sobrevive a un rerun? | ¿Se limpia al pulsar «Limpiar»? | Motivo |
| --- | --- | --- | --- | --- |
| `last_state` | `st.session_state` | Sí | No, pero depende de session_state | Podemos construirlo como un diccionario que guarda valores, o como una variable que reasignamos |
| `last_values` | `st.session_state` | Sí | No | ídem que `last_state` |
| `telemetry` | sistema de logs/observabilidad | Sí | No | Registra metadatos, nunca secretos |
| gateway / bundle | `st.cache_resource` | Sí | No | El bundle se carga una única vez, y está disponible en cada rerun |
| respuesta de una petición | json | No | Sí | La respuesta que damos es distinta para cada usuario |

### 2. Máquina de estados

| Estado | Evento de entrada| Zona de pantalla que cambia | Acción / evidencia |
| --- | --- | --- | --- |
| `idle` | Inicio o limpiar | Formulario disponible; sin resultado anterior. | Enviar una predicción. Evidencia: estado inicial. |
| `loading` | Envío válido | Zona de operación indica que se está procesando; evita mostrar resultados antiguos como actuales. | Esperar. Evidencia: transición visible a `loading`. |
| `success` | Respuesta válida | Mostrar categoría, confianza y latencia; añadir aviso si supera 300 ms; trazabilidad si se selecciona. | Revisar el resultado o volver a enviar. Evidencia: respuesta y `request_id`. |
| `error` | Fallo controlado | Mensaje comprensible y seguro, sin traceback ni detalles internos; conservar el formulario para corregir o reintentar. | Corregir la entrada o reintentar más tarde. Evidencia: tipo de error registrado sin datos sensibles. |

Una respuesta con salida válida pero latencia superior a 300 ms permanece en
`success` y añade una señal técnica de lentitud.

### 3. Plano de interfaz, caché y UX

Justificad:

- qué función se protege con `st.cache_resource`;
- qué dato no debe cachearse como recurso;
- qué componente representa `loading`, resultado, advertencia y trazabilidad;
- por qué la confianza se presenta con una métrica y un mensaje, no como una
  barra de progreso;
- qué mensaje se muestra con confianza baja;
- qué recuperación se ofrece para bundle ausente, timeout y error de entrada.

## Criterios de aceptación

- el diseño parte explícitamente de una limitación de S5;
- no introduce una segunda definición del contrato de S4;
- las transiciones tienen eventos y acciones observables;
- distingue estado de sesión, recurso cacheado y datos de una petición;
- el laboratorio presenta los escenarios `idle`, `loading`, `success` y
  `error` sin ejecutar ni reimplementar el modelo;
- categoría, confianza y latencia se entienden sin abrir la trazabilidad;
- otra pareja puede implementar el taller sin inventar estados.
