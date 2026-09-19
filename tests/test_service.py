import asyncio
from unittest.mock import patch, AsyncMock

import pytest

from ai.schemas import Ingredient, NutritionFacts
from app.service import analyze_image


def test_analyze_image_returns_complete_result():
    fake_ingredients = [
        Ingredient(
            name="white rice",
            estimated_grams=180,
            confidence=0.90,
        ),
        Ingredient(
            name="grilled chicken breast",
            estimated_grams=150,
            confidence=0.95,
        ),
    ]

    fake_facts = {
        "white rice": NutritionFacts(
            name="white rice",
            kcal_per_100g=130,
            protein_g_per_100g=2.7,
            carbs_g_per_100g=28.0,
            fat_g_per_100g=0.3,
        ),
        "grilled chicken breast": NutritionFacts(
            name="grilled chicken breast",
            kcal_per_100g=165,
            protein_g_per_100g=31.0,
            carbs_g_per_100g=0.0,
            fat_g_per_100g=3.6,
        ),
    }

    async def fake_nutrition_lookup(_):
        return fake_facts

    with patch(
            "app.service.identify_ingredients",
            return_value=fake_ingredients,
    ), patch(
        "app.service.get_nutrition_for_ingredients",
        side_effect=fake_nutrition_lookup,
    ), patch(
        "app.service.save_analysis",
        new_callable=AsyncMock,
    ) as mock_save:
        result = asyncio.run(
            analyze_image("data/rice_chicken.png")
        )

    assert len(result["ingredients"]) == 2

    assert result["ingredients"][0].name == "white rice"
    assert result["ingredients"][0].estimated_grams == 180

    assert result["totals"].kcal > 0
    assert result["totals"].protein_g > 0
    mock_save.assert_awaited_once()


def test_analyze_image_file_not_found():
    with pytest.raises(FileNotFoundError):
        asyncio.run(
            analyze_image("data/test_yoxdur.png")
        )


def test_analyze_image_unknown_meal():
    with patch(
        "app.service.identify_ingredients",
        return_value=[],
    ):
        result = asyncio.run(
            analyze_image("data/rice_chicken.png")
        )

    assert result["ingredients"] == []
    assert result["totals"] is None