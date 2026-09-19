from app.database import SessionLocal
from app.models import AnalysisHistory
from sqlalchemy import select


async def save_analysis(
    image_path: str,
    ingredients: list,
    totals,
) -> AnalysisHistory:

    record = AnalysisHistory(
        image_path=image_path,
        ingredients=ingredients,
        kcal=totals.kcal,
        protein_g=totals.protein_g,
        carbs_g=totals.carbs_g,
        fat_g=totals.fat_g,
    )

    async with SessionLocal() as session:
        session.add(record)
        await session.commit()
        await session.refresh(record)

    return record
async def get_history(limit: int = 20) -> list[AnalysisHistory]:
    async with SessionLocal() as session:
        result = await session.execute(
            select(AnalysisHistory)
            .order_by(AnalysisHistory.created_at.desc())
            .limit(limit)
        )

        return list(result.scalars().all())