import streamlit as st
st.title("Contador con callback")
if "count" not in st.session_state:
    st.session_state.count = 0 # session_state es un diccionario, así que puedo crear también 
                                # session_state.resta = 0 (puedo meter todo lo que quiera dentro de ese diccionario)
def increment():
    st.session_state.count += 1
st.button("Sumar", on_click=increment)

# Documentación:
# (parameter) on_click: WidgetCallback | None
# on_click : callable
# An optional callback invoked when this button is clicked.

# Yo:
# Es decir, recibe un callable, una función que sea llamable. 
# Me permite introducir un callback sin modificar el código de .button()

st.metric("Cuenta", st.session_state.count)