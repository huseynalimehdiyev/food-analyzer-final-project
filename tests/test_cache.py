from ai.schemas import NutritionFacts
from app.cache import NutritionCache


def test_cache_set_and_get():
    cache = NutritionCache()

    nutrition = NutritionFacts(
        name="white rice",
        kcal_per_100g=130,
        protein_g_per_100g=2.7,
        carbs_g_per_100g=28.0,
        fat_g_per_100g=0.3,
    )

    cache.set("white rice", nutrition)

    result = cache.get("white rice")

    assert result is not None
    assert result.name == "white rice"
    assert result.kcal_per_100g == 130


def test_cache_returns_none_for_missing_item():
    cache = NutritionCache()

    result = cache.get("unknown food")

    assert result is None


def test_cache_normalizes_name():
    cache = NutritionCache()

    nutrition = NutritionFacts(
        name="white rice",
        kcal_per_100g=130,
        protein_g_per_100g=2.7,
        carbs_g_per_100g=28.0,
        fat_g_per_100g=0.3,
    )

    cache.set(" White Rice ", nutrition)

    result = cache.get("white rice")

    assert result is not None
    assert result.name == "white rice"