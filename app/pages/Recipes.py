# app/main.py
import streamlit as st
import requests

st.set_page_config(page_title="App de Receitas", layout="wide")
st.title("📖 App de Receitas")

API_RECIPES_URL = "http://localhost:8000/recipes/"
API_INGREDIENTS_URL = "http://localhost:8000/ingredients/"

def format_recipe_display(recipe):
    with st.expander(f"**{recipe['name']}**"):
        st.markdown("##### Instruções")
        st.write(recipe.get('instructions', 'Nenhuma instrução fornecida.'))
        st.markdown("##### Ingredientes")
        if recipe.get('ingredients'):
            for ingredient in recipe['ingredients']:
                st.write(f"- {ingredient.get('name', 'Ingrediente sem nome')}")
        else:
            st.write("Nenhum ingrediente listado.")

# --- Busca de Dados Iniciais ---
try:
    response = requests.get(API_INGREDIENTS_URL)
    response.raise_for_status()
    all_ingredients = response.json()
    ingredient_names = sorted([ing['name'] for ing in all_ingredients])
except (requests.exceptions.RequestException, KeyError):
    st.warning(
        f"Não foi possível carregar a lista de ingredientes da API. "
        f"Certifique-se que o endpoint '{API_INGREDIENTS_URL}' está ativo. "
        "Você precisará digitar os nomes manualmente."
    )
    all_ingredients = []
    ingredient_names = []

st.header("Ver Receitas Existentes")

if st.button("Atualizar Lista de Receitas"):
    st.rerun()

try:
    response = requests.get(API_RECIPES_URL)
    if response.status_code == 200:
        recipes = response.json()
        if recipes:
            for recipe in recipes:
                format_recipe_display(recipe)
        else:
            st.info("Nenhuma receita encontrada no banco de dados.")
    else:
        st.error(f"Erro ao buscar receitas. Status: {response.status_code}")
except requests.exceptions.ConnectionError:
    st.error("Não foi possível conectar à API. Verifique se o backend está rodando.")

st.markdown("---")

if 'ingredients_list' not in st.session_state:
    st.session_state.ingredients_list = []

def reset_recipe_modal():
    st.session_state.ingredients_list = []
    st.session_state.recipe_modal_open = False

@st.dialog("Adicionar Nova Receita")
def recipe_modal():
    recipe_name = st.text_input("Nome da Receita", key="modal_recipe_name")
    recipe_instructions = st.text_area("Instruções", key="modal_recipe_instructions")

    st.markdown("##### Adicionar Ingredientes")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        if ingredient_names:
            ingredient_name = st.selectbox("Ingrediente", options=ingredient_names, key="modal_ingredient_name")
        else:
            ingredient_name = st.text_input("Ingrediente (digite o nome)", key="modal_ingredient_name_text")
    with col2:
        quantity = st.text_input("Quantidade", key="modal_quantity")
    with col3:
        unit = st.text_input("Unidade (ex: kg)", key="modal_unit")

    add_button = st.button("Adicionar Ingrediente", key="modal_add_ingredient")
    if add_button:
        if ingredient_name and quantity:
            st.session_state.ingredients_list.append((ingredient_name, quantity, unit))
            st.success(f"Ingrediente '{ingredient_name}' adicionado!")
        else:
            st.warning("Selecione/digite um ingrediente e preencha a quantidade.")
        st.rerun()

    if st.session_state.ingredients_list:
        st.write("**Ingredientes a serem adicionados:**")
        for i, (name, qty, u) in enumerate(st.session_state.ingredients_list):
            st.write(f"{i + 1}. {name} - {qty} {u}")

    submitted = st.button("✅ Criar Receita", key="modal_submit_recipe")
    if submitted:
        if not recipe_name.strip():
            st.warning("O nome da receita não pode ser vazio.")
        elif not st.session_state.ingredients_list:
            st.warning("Adicione pelo menos um ingrediente.")
        else:
            ingredients_payload = [
                [name, qty, u if u else None]
                for (name, qty, u) in st.session_state.ingredients_list
            ]
            payload = {
                "name": recipe_name,
                "instructions": recipe_instructions,
                "ingredients": ingredients_payload
            }
            try:
                response = requests.post(API_RECIPES_URL, json=payload)
                if response.status_code == 200:
                    st.success(f"Receita '{recipe_name}' criada com sucesso!")
                    reset_recipe_modal()
                    st.rerun()
                else:
                    st.error(f"Erro ao criar receita: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Erro de conexão com a API.")

    if st.button("Cancelar", key="modal_cancel"):
        reset_recipe_modal()
        st.rerun()

if st.button("➕ Nova Receita"):
    st.session_state.recipe_modal_open = True
    recipe_modal()
