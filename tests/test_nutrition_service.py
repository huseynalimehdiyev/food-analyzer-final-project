from unittest.mock import MagicMock, patch

from ai.schemas import NutritionFacts
from app.nutrition_service import get_nutrition, get_nutrition_for_ingredients
import asyncio

def test_get_nutrition():
    fake_nutrition = NutritionFacts(
        name="white rice",
        kcal_per_100g=130,
        protein_g_per_100g=2.7,
        carbs_g_per_100g=28.0,
        fat_g_per_100g=0.3,
    )

    fake_provider = MagicMock()
    fake_provider.lookup.return_value = fake_nutrition

    with patch(
        "app.nutrition_service.get_nutrition_provider",
        return_value=fake_provider,
    ):
        result = get_nutrition("white rice")

    assert result.name == "white rice"
    assert result.kcal_per_100g == 130
    assert result.protein_g_per_100g == 2.7
    assert result.carbs_g_per_100g == 28.0
    assert result.fat_g_per_100g == 0.3
def test_get_nutrition_for_ingredients():
    rice = NutritionFacts(
        name="white rice",
        kcal_per_100g=130,
        protein_g_per_100g=2.7,
        carbs_g_per_100g=28.0,
        fat_g_per_100g=0.3,
    )

    chicken = NutritionFacts(
        name="grilled chicken breast",
        kcal_per_100g=165,
        protein_g_per_100g=31.0,
        carbs_g_per_100g=0.0,
        fat_g_per_100g=3.6,
    )

    fake_results = {
        "white rice": rice,
        "grilled chicken breast": chicken,
    }

    async def fake_get_nutrition_async(name):
        return fake_results[name]

    with patch(
        "app.nutrition_service.get_nutrition_async",
        side_effect=fake_get_nutrition_async,
    ):
        result = asyncio.run(
            get_nutrition_for_ingredients(
                ["white rice", "grilled chicken breast"]
            )
        )

    assert len(result) == 2
    assert result["white rice"].kcal_per_100g == 130
    assert result["grilled chicken breast"].protein_g_per_100g == 31.0
def test_get_nutrition_uses_cache():
    fake_nutrition = NutritionFacts(
        name="broccoli",
        kcal_per_100g=35,
        protein_g_per_100g=2.4,
        carbs_g_per_100g=7.2,
        fat_g_per_100g=0.4,
    )

    fake_provider = MagicMock()
    fake_provider.lookup.return_value = fake_nutrition

    with patch(
        "app.nutrition_service.get_nutrition_provider",
        return_value=fake_provider,
    ):
        first_result = get_nutrition("broccoli")
        second_result = get_nutrition("broccoli")

    assert first_result.name == "broccoli"
    assert second_result.name == "broccoli"

    assert fake_provider.lookup.call_count == 1