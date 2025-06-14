"""
Defines API routes for recipe and grocery list endpoints.

- /generate_recipe: accepts PDF upload, returns generated recipe text.
"""

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/generate_recipe")
async def generate_recipe(file: UploadFile = File(...)):
    # TODO: call LangGraph node for PDF parsing + recipe generation
    content = await file.read()
    # stub response for MVP
    return JSONResponse({"recipe_text": "Example recipe generated from PDF."})
