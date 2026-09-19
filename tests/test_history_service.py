import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from ai.schemas import Nutrition
from app.history_service import save_analysis, get_history


def test_save_analysis():
    totals = Nutrition(
        kcal=482,
        protein_g=51.4,
        carbs_g=50.4,
        fat_g=5.9,
    )

    ingredients = [
        {
            "name": "white rice",
            "estimated_grams": 180,
            "confidence": 0.95,
        },
        {
            "name": "grilled chicken breast",
            "estimated_grams": 150,
            "confidence": 0.95,
        },
    ]

    fake_session = AsyncMock()
    fake_session.add = MagicMock()

    session_context = AsyncMock()
    session_context.__aenter__.return_value = fake_session
    session_context.__aexit__.return_value = None

    with patch(
        "app.history_service.SessionLocal",
        return_value=session_context,
    ):
        result = asyncio.run(
            save_analysis(
                image_path="data/rice_chicken.png",
                ingredients=ingredients,
                totals=totals,
            )
        )

    fake_session.add.assert_called_once()
    fake_session.commit.assert_awaited_once()
    fake_session.refresh.assert_awaited_once()

    assert result.image_path == "data/rice_chicken.png"
    assert result.kcal == 482
    assert result.protein_g == 51.4
def test_get_history_returns_list():
    history = asyncio.run(get_history(limit=10))

    assert isinstance(history, list)