import asyncio

from ai.nutrition import get_nutrition_provider
from ai.schemas import NutritionFacts
from app.cache import nutrition_cache


def get_nutrition(ingredient_name: str) -> NutritionFacts:
    cached = nutrition_cache.get(ingredient_name)

    if cached is not None:
        return cached

    provider = get_nutrition_provider()
    nutrition = provider.lookup(ingredient_name)

    nutrition_cache.set(
        ingredient_name,
        nutrition,
    )

    return nutrition


async def get_nutrition_async(
    ingredient_name: str,
) -> NutritionFacts:
    return await asyncio.to_thread(
        get_nutrition,
        ingredient_name,
    )


async def get_nutrition_for_ingredients(
    ingredient_names: list[str],
) -> dict[str, NutritionFacts]:

    tasks = [
        get_nutrition_async(name)
        for name in ingredient_names
    ]

    results = await asyncio.gather(*tasks)

    return dict(zip(ingredient_names, results))