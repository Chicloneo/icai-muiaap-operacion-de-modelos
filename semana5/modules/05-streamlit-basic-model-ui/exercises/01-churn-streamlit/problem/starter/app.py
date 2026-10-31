"""Starter: conecta una función de inferencia pura con Streamlit."""

from collections.abc import Callable
from typing import Any

from churn_demo.model import ChurnPrediction, predict

Predictor = Callable[..., ChurnPrediction]


def collect_profile(st: Any) -> tuple[bool, dict[str, object]]:
    """Renderiza cuatro widgets dentro de un único formulario."""
    # TODO 1 (alumno): usa st.form("churn_form"), los cuatro widgets con las
    # claves indicadas en el README y st.form_submit_button. El formulario evita
    # inferencias durante cada edición. Compruébalo con el primer test de app.

    #Ayuda de la documentación de Streamlit

    form = st.form(key="churn_form", #string that identifies the form
                   # clear_on_submit=False, #If True, all widgets inside the form will be reset 
                                    #to their default values after the user presses the Submit button.
                    # enter_to_submit=False, #submits the form when a user presses Enter
                    # border=True, #shows a border around the form
                    # width='stretch', #matches the width of the parent container
                    # height='content' #matches the height of its content
                    )

    with form:

        tenure_months = st.slider(
            label="Antigüedad", #what this slider is for.
            min_value=0,
            max_value=120,
            value=12, #The value of the slider when it first renders.
            # step=1,
            #format=None, #how the interface displays values
            key="tenure_months", #string to use as the unique key for the widget
                                #la key guarda el valor en session_state al ejecutar otra vez de arriba a abajo el script
            #help="Choose your tenure months", #A tooltip that gets displayed next to the widget label.
            #label_visibility='visible', #displays the "help" tooltip when label_visibility="visible"
            #width='stretch'
        ) #returns int in this case

        monthly_spend_eur = st.number_input(
            label="Gasto mensual",
            min_value=0,
            max_value=300,
            value=60,
            step=1,
            format=None, #This does not impact the return value of the widget
            key="monthly_spend_eur",
            help="Choose your monthly spending (€)",
            placeholder="Enter monthly spending... (required field)", #string displayed when the number input is empty
            required=True, # requires a non-empty value 
            label_visibility='visible',
            icon=":material/paid:", #displays within the input field to the left of the value
            width='stretch'
        ) #int

        support_calls = st.slider(
            label="Llamadas a soporte", 
            min_value=0,
            max_value=20,
            value=1, 
            # step=1,
            #format=None,
            key="support_calls", 
            #help="Select your support calls",
            #label_visibility='visible',
            #width='stretch'
        ) #int

        has_annual_contract = st.checkbox(
            label="Contrato Anual",
            value=False, #Inicialmente desactivado
            key="has_annual_contract",
            #help="Selecciona si tienes contrato anual",
            #label_visibility='visible',
            #width='stretch',
            #wrap=True #If the label is too wide for the checkbox, it wraps onto additional lines
        ) #True/False

        submitted = st.form_submit_button("Calcular Riesgo") #True (False) if the button was (not) clicked

    values = {
            "tenure_months": tenure_months,
            "monthly_spend_eur": monthly_spend_eur,
            "support_calls": support_calls,
            "has_annual_contract": has_annual_contract
            }

    if submitted:
        return submitted, values


def render_prediction(st: Any, result: ChurnPrediction) -> None:
    """Muestra etiqueta, score orientativo y explicación."""
    # TODO 3 (alumno): presenta label, risk_score y explanation con componentes
    # Streamlit. No recalcules el score. Compruébalo con el test de presentación.
    raise NotImplementedError("STUDENT TASK: presenta la predicción")


def run_app(st: Any, predictor: Predictor) -> None:
    """Conecta submit, llamada al predictor y actualización visible."""
    # TODO 2 (alumno): llama a collect_profile, ejecuta predictor(**values) solo
    # tras el submit y una única vez; convierte ValueError en un mensaje seguro.
    # Los tests de 0/1 llamadas y de error verifican este contrato.
    submitted, values = collect_profile(st)
    prediccion = predictor(**values)

    #Predictor devuelve un objeto ChurnPrediction, que está definido como TypeDict
    #así que hay que acceder a sus elementos como un diccionario
    st.write(prediccion["label"])


def main() -> None:
    """Configura la página real y delega el flujo comprobable en run_app."""
    import streamlit as st
    #se pasa st como parámetro por eficiencia: 
    # para importar la librería solo cuando sea necesario

    st.set_page_config(page_title="Churn sintético · S5", page_icon="📉")
    st.title("¿Qué cliente podría darse de baja?")
    st.caption("Caso docente sintético; el score no es una probabilidad calibrada.")
    run_app(st, predict)


if __name__ == "__main__":
    main()
