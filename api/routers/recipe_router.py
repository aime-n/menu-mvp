from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..core.supabase_client import get_session
from ..services import recipe_service
from ..schemas.recipe_schema import RecipeCreate, RecipePublic, Recipe

router = APIRouter()

@router.post("/", response_model=RecipePublic)
def handle_create_recipe(recipe_data: RecipeCreate, session: Session = Depends(get_session)):
    """
    API endpoint to create a new recipe.
    """
    try:
        recipe = recipe_service.create_recipe(
            session=session,
            name=recipe_data.name,
            instructions=recipe_data.instructions,
            ingredients_data=recipe_data.ingredients
        )
        return recipe
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[RecipePublic])
def handle_get_all_recipes(session: Session = Depends(get_session)):
    """
    API endpoint to retrieve all recipes.
    """
    return recipe_service.get_all_recipes(session=session)

@router.get("/{recipe_name}", response_model=RecipePublic)
def handle_get_recipe_by_name(recipe_name: str, session: Session = Depends(get_session)):
    """
    API endpoint to get a single recipe by its name.
    """
    recipe = recipe_service.get_recipe_by_name(session=session, recipe_name=recipe_name)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
