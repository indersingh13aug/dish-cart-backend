from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatResponse
from app.services.recipe_service import handle_recipe, product_listing

router = APIRouter()

@router.get("/recipe")
def get_recipe(query: str) -> ChatResponse:
    """
    Generate a recipe for the given query.
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    recipe = handle_recipe(query)
    return ChatResponse(
        assistant_message=recipe,
        intent="recipe_request"
    )


@router.get("/ingredient")
def get_ingredient_options(query: str) -> ChatResponse:
    """
    Return product listing options for an ingredient.
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    products = product_listing(query)
    return ChatResponse(
        assistant_message=products,
        intent="ingredient_query"
    )
