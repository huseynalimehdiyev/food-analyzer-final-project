import os
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.service import analyze_image
from app.config import settings
from app.history_service import save_analysis

app = FastAPI(
    title="AI Food Analyzer API",
    version="1.0.0",
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
    }


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    allowed_types = {
        "image/jpeg",
        "image/png",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG and PNG images are allowed.",
        )
    suffix = os.path.splitext(file.filename or "")[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    ) as temp_file:
        content = await file.read()

        max_size_bytes = settings.max_image_size_mb * 1024 * 1024

        if len(content) > max_size_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"Image is too large. Maximum size is {settings.max_image_size_mb} MB.",
            )

        temp_file.write(content)
        temp_path = temp_file.name

    try:
        result = await analyze_image(temp_path)

        ingredients = [
            {
                "name": ingredient.name,
                "estimated_grams": ingredient.estimated_grams,
                "confidence": ingredient.confidence,
            }
            for ingredient in result["ingredients"]
        ]

        totals = result["totals"]

        if totals is None:
            return {
                "ingredients": [],
                "totals": None,
            }
        await save_analysis(
            image_path=file.filename or temp_path,
            ingredients=ingredients,
            totals=totals,
        )
        return {
            "ingredients": ingredients,
            "totals": totals.to_dict(),
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)