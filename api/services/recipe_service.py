from typing import List, Optional, Tuple
from sqlmodel import Session, select
from ..schemas.recipe_schema import Recipe, Ingredient, RecipeIngredientLink

def get_or_create_ingredient(session: Session, name: str) -> Ingredient:
    """Retrieves an ingredient by name if it exists, otherwise creates a new one."""
    statement = select(Ingredient).where(Ingredient.name == name.lower())
    ingredient = session.exec(statement).first()
    if not ingredient:
        ingredient = Ingredient(name=name.lower())
        session.add(ingredient)
        session.commit()
        session.refresh(ingredient)
    return ingredient

def create_recipe(session: Session, name: str, instructions: str, ingredients_data: List[Tuple[str, str, str]]) -> Recipe:
    """Creates a new recipe and its ingredients."""
    try:
        recipe = Recipe(name=name, instructions=instructions)
        for ingredient_name, quantity, unit in ingredients_data:
            ingredient = get_or_create_ingredient(session, ingredient_name)
            link = RecipeIngredientLink(quantity=quantity, unit=unit, recipe=recipe, ingredient=ingredient)
            session.add(link)
        session.add(recipe)
        session.commit()
        session.refresh(recipe)
        return recipe
    except Exception as e:
        session.rollback()
        raise e

def get_all_recipes(session: Session) -> List[Recipe]:
    """Retrieves all recipes."""
    return session.exec(select(Recipe)).all()

def get_recipe_by_name(session: Session, recipe_name: str) -> Optional[Recipe]:
    """Retrieves a single recipe by its name."""
    statement = select(Recipe).where(Recipe.name == recipe_name)
    return session.exec(statement).first()
