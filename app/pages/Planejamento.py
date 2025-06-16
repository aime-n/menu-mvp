# app/pages/2_Planejamento.py
import streamlit as st
from collections import defaultdict
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para encontrar o módulo 'utils'
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# -------------------------------------------------------------------
# ARQUIVO 1: app/utils.py
# CRIE ESTE NOVO ARQUIVO para funções compartilhadas.
# -------------------------------------------------------------------
import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"

@st.cache_data(ttl=60)
def get_recipes_from_api():
    """Busca todas as receitas da API."""
    try:
        response = requests.get(f"{API_BASE_URL}/recipes/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar receitas: {e}")
        return []

@st.cache_data(ttl=60)
def get_ingredients_from_api():
    """Busca todos os ingredientes da API."""
    try:
        response = requests.get(f"{API_BASE_URL}/ingredients/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return []


st.set_page_config(page_title="Lista de Compras", layout="wide")
st.title("🛒 Gerador de Lista de Compras")
st.markdown("Escolha as receitas e a quantidade desejada para gerar sua lista de compras consolidada.")

# --- Carregar Dados ---
all_recipes = get_recipes_from_api()

if not all_recipes:
    st.info("Nenhuma receita disponível. Adicione algumas na página 'Gestão de Receitas'.")
else:
    # Mapeia nome da receita para seus detalhes completos
    recipe_map = {recipe['name']: recipe for recipe in all_recipes}
    
    with st.form("shopping_list_generator"):
        st.header("Selecione suas receitas")
        
        recipe_quantities = {}

        for recipe_name in sorted(recipe_map.keys()):
            cols = st.columns([1, 5])
            with cols[0]:
                quantity = st.number_input(
                    label="",
                    min_value=0,
                    step=1,
                    key=f"qty_{recipe_name}",
                    placeholder="Qtd."
                )
            with cols[1]:
                st.markdown(f"**{recipe_name}**")
            if quantity > 0:
                recipe_quantities[recipe_name] = quantity

        submitted = st.form_submit_button("Gerar Lista de Compras", type="primary")

        if submitted:
            if not recipe_quantities:
                st.warning("Você não selecionou nenhuma receita. Escolha a quantidade de pelo menos uma.")
            else:
                shopping_list = defaultdict(lambda: {"total": 0.0, "units": set()})
                non_numeric_ingredients = defaultdict(list)

                for recipe_name, multiplier in recipe_quantities.items():
                    recipe_details = recipe_map.get(recipe_name)
                    if recipe_details and 'ingredients' in recipe_details:
                        for ingredient in recipe_details['ingredients']:
                            ing_name = ingredient.get("name")
                            ing_qty_str = str(ingredient.get("quantity", "1"))
                            ing_unit = ingredient.get("unit", "")
                            try:
                                ing_qty_float = float(ing_qty_str.replace(",", "."))
                                shopping_list[(ing_name, ing_unit)]["total"] += ing_qty_float * multiplier
                                shopping_list[(ing_name, ing_unit)]["units"].add(ing_unit)
                            except ValueError:
                                for _ in range(multiplier):
                                    non_numeric_ingredients[ing_name].append(f"{ing_qty_str} {ing_unit}".strip())
                
                st.subheader("✅ Sua Lista de Compras")
                for (name, unit), data in sorted(shopping_list.items()):
                    total_qty = data['total']
                    unit_str = f" {unit}" if unit else ""
                    st.markdown(f"- **{name.capitalize()}**: {total_qty:g}{unit_str}")
                for name, amounts in sorted(non_numeric_ingredients.items()):
                    st.markdown(f"- **{name.capitalize()}**: {', '.join(amounts)}")

