import streamlit as st
import requests

st.title("Ingredientes")

API_URL = "http://localhost:8000/ingredients/"

# --- Adicionar Ingrediente ---
st.header("Adicionar novo ingrediente")
with st.form("add_ingredient_form", clear_on_submit=True):
    name = st.text_input("Nome do ingrediente", max_chars=50)
    submitted = st.form_submit_button("Adicionar")
    if submitted:
        if not name.strip():
            st.warning("O nome do ingrediente não pode ser vazio.")
        else:
            response = requests.post(API_URL, json={"name": name})
            if response.status_code == 200:
                st.success(f"Ingrediente '{name}' adicionado com sucesso!")
            elif response.status_code == 400:
                st.error("Ingrediente já existe.")
            else:
                st.error("Erro ao adicionar ingrediente.")

st.divider()

# --- Visualizar Ingredientes ---
st.header("Lista de ingredientes")
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        ingredients = response.json()
        if ingredients:
            for ingredient in ingredients:
                st.write(f"- {ingredient['name']}")
        else:
            st.info("Nenhum ingrediente cadastrado ainda.")
    else:
        st.error("Erro ao buscar ingredientes.")
except Exception as e:
    st.error(f"Erro de conexão com o backend: {e}")