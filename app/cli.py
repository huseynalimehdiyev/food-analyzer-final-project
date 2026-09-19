import argparse
import asyncio

from app.service import analyze_image


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI Food Analyzer"
    )

    parser.add_argument(
        "image",
        help="Path to the meal image",
    )

    return parser


async def run(image_path: str) -> None:
    result = await analyze_image(image_path)

    ingredients = result["ingredients"]
    totals = result["totals"]

    if not ingredients:
        print("No meal recognized.")
        return

    print("\nIngredients:")

    for ingredient in ingredients:
        print(
            f"- {ingredient.name}: "
            f"{ingredient.estimated_grams:.0f} g "
            f"(confidence: {ingredient.confidence:.2f})"
        )

    print("\nNutrition totals:")
    print(f"Calories: {totals.kcal:.1f} kcal")
    print(f"Protein: {totals.protein_g:.1f} g")
    print(f"Carbs: {totals.carbs_g:.1f} g")
    print(f"Fat: {totals.fat_g:.1f} g")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        asyncio.run(run(args.image))
    except FileNotFoundError as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()