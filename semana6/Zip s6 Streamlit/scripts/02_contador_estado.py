import streamlit as st
st.title("Contador con estado")
if "count" not in st.session_state: # session_state es un diccionario protegido de streamlit
                                    # solo se reinicia si refrescas la página
                                    # nadie la ha creado antes, está ahí
                                    # se accede a sus variables con .variable
    st.session_state.count = 0
if st.button("Sumar"):
    st.session_state.count += 1
st.metric("Cuenta", st.session_state.count)
