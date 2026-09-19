import asyncio
import time


async def fake_nutrition_lookup(name: str):
    """Simulate a nutrition API request."""
    await asyncio.sleep(0.5)
    return {"name": name}


async def sequential_lookup(ingredients):
    results = []

    for ingredient in ingredients:
        result = await fake_nutrition_lookup(ingredient)
        results.append(result)

    return results


async def concurrent_lookup(ingredients):
    tasks = [
        fake_nutrition_lookup(ingredient)
        for ingredient in ingredients
    ]

    return await asyncio.gather(*tasks)


async def main():
    ingredients = [
        "white rice",
        "grilled chicken breast",
        "broccoli",
        "tomato",
        "avocado",
    ]

    print("Concurrency Benchmark")
    print("---------------------")
    print(f"Ingredients: {len(ingredients)}")

    start = time.perf_counter()
    await sequential_lookup(ingredients)
    sequential_time = time.perf_counter() - start

    start = time.perf_counter()
    await concurrent_lookup(ingredients)
    concurrent_time = time.perf_counter() - start

    speedup = sequential_time / concurrent_time

    print(f"Sequential time: {sequential_time:.2f} seconds")
    print(f"Concurrent time: {concurrent_time:.2f} seconds")
    print(f"Speedup: {speedup:.2f}x")


if __name__ == "__main__":
    asyncio.run(main())