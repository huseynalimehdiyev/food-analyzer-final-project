from pathlib import Path

from ai.calculator import compute_totals
from ai.vlm import identify_ingredients
from app.nutrition_service import get_nutrition_for_ingredients
from app.history_service import save_analysis


async def analyze_image(image_path: str):
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    ingredients = identify_ingredients(str(path))

    if not ingredients:
        return {
            "ingredients": [],
            "totals": None,
        }

    ingredient_names = [
        ingredient.name
        for ingredient in ingredients
    ]

    facts_by_name = await get_nutrition_for_ingredients(
        ingredient_names
    )

    totals = compute_totals(
        ingredients,
        facts_by_name,
    )

    ingredients_data = [
        {
            "name": ingredient.name,
            "estimated_grams": ingredient.estimated_grams,
            "confidence": ingredient.confidence,
        }
        for ingredient in ingredients
    ]

    await save_analysis(
        image_path=str(path),
        ingredients=ingredients_data,
        totals=totals,
    )

    return {
        "ingredients": ingredients,
        "totals": totals,
    }