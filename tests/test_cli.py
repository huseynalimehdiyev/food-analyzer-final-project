import asyncio
from unittest.mock import patch

from ai.schemas import Ingredient, Nutrition
from app.cli import run


def test_cli_prints_analysis(capsys):
    fake_result = {
        "ingredients": [
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
        ],
        "totals": Nutrition(
            kcal=482,
            protein_g=51.4,
            carbs_g=50.4,
            fat_g=5.9,
        ),
    }

    async def fake_analyze_image(_):
        return fake_result

    with patch(
        "app.cli.analyze_image",
        side_effect=fake_analyze_image,
    ):
        asyncio.run(
            run("data/rice_chicken.png")
        )

    output = capsys.readouterr().out

    assert "white rice" in output
    assert "grilled chicken breast" in output
    assert "482.0 kcal" in output
    assert "51.4 g" in output