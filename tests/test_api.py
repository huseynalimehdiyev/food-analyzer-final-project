from unittest.mock import patch

from fastapi.testclient import TestClient

from ai.schemas import Ingredient, Nutrition
from app.api import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_endpoint():
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
            "app.api.analyze_image",
            side_effect=fake_analyze_image,
    ), patch(
        "app.api.save_analysis",
    ) :
        response = client.post(
            "/analyze",
            files={
                "file": (
                    "meal.jpg",
                    b"fake image content",
                    "image/jpeg",
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert len(data["ingredients"]) == 2
    assert data["ingredients"][0]["name"] == "white rice"
    assert data["ingredients"][0]["estimated_grams"] == 180

    assert data["totals"]["kcal"] == 482
    assert data["totals"]["protein_g"] == 51.4
    assert data["totals"]["carbs_g"] == 50.4
    assert data["totals"]["fat_g"] == 5.9
def test_analyze_rejects_non_image():
    response = client.post(
        "/analyze",
        files={
            "file": (
                "notes.txt",
                b"this is not an image",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Only JPEG and PNG images are allowed."
    )
def test_analyze_rejects_large_image():
    large_content = b"x" * (6 * 1024 * 1024)

    response = client.post(
        "/analyze",
        files={
            "file": (
                "large.jpg",
                large_content,
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 413
    assert "Image is too large" in response.json()["detail"]