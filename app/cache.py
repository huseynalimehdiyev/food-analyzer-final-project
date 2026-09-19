import time

from ai.schemas import NutritionFacts
from app.config import settings


class NutritionCache:
    def __init__(self):
        self._data: dict[str, tuple[float, NutritionFacts]] = {}

    def get(self, name: str) -> NutritionFacts | None:
        key = name.lower().strip()

        if key not in self._data:
            return None

        created_at, nutrition = self._data[key]

        age = time.time() - created_at

        if age > settings.nutrition_cache_ttl_seconds:
            del self._data[key]
            return None

        return nutrition

    def set(self, name: str, nutrition: NutritionFacts) -> None:
        key = name.lower().strip()

        self._data[key] = (
            time.time(),
            nutrition,
        )


nutrition_cache = NutritionCache()