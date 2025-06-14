"""
Defines API routes for recipe and grocery list endpoints.

- /weekly_plan: accepts selected recipes, returns grocery list with calories/prices.
"""

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/weekly_plan")
async def weekly_plan(selected_recipes: list[str]):
    # TODO: call LangGraph node for grocery list generation
    # stub response for MVP
    grocery_list = [{"item": "Tomatoes", "quantity": "3", "calories": 60, "price": 1.5}]
    return JSONResponse({"grocery_list": grocery_list})