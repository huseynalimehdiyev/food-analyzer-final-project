````
# AI Food Analyzer

AI Food Analyzer is a Software Engineering final project that analyzes meal images, identifies visible food ingredients, estimates portion sizes, retrieves nutritional information, and calculates total calories and macronutrients.

The project provides both a Command Line Interface (CLI) and an HTTP API.

---

## Features

- Meal image analysis using a Vision Language Model (VLM)
- Ingredient identification
- Estimated ingredient portion sizes in grams
- Nutrition lookup using USDA FoodData Central
- Calculation of:
  - Calories
  - Protein
  - Carbohydrates
  - Fat
- Concurrent nutrition lookups using `asyncio.gather()`
- Nutrition result caching
- PostgreSQL analysis history
- Command Line Interface (CLI)
- FastAPI HTTP API
- Input validation and error handling
- Non-food image handling
- Automated tests
- Docker support
- Offline demonstration mode
- Concurrency benchmark

---

## Project Architecture

The application follows a layered architecture:

```text
User
  |
  +-------------------+
  |                   |
 CLI               HTTP API
  |                   |
  +--------+----------+
           |
      Food Service
           |
           v
          VLM
           |
           v
 Ingredients + Estimated Grams
           |
           v
   Nutrition Service
           |
      +----+----+
      |         |
    Cache      USDA
      |         |
      +----+----+
           |
     asyncio.gather()
           |
           v
      Calculator
           |
           v
   Nutrition Result
           |
           v
      PostgreSQL
```

The provided `ai/` package contains the AI and nutrition-related core components. The `app/` package contains the Software Engineering layer developed for this project.

---

## Project Structure

```text
topic-2-food-analyzer/
|
├── ai/
│   ├── providers/
│   ├── __init__.py
│   ├── calculator.py
│   ├── nutrition.py
│   ├── schemas.py
│   └── vlm.py
│
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── cache.py
│   ├── cli.py
│   ├── config.py
│   ├── database.py
│   ├── history_service.py
│   ├── models.py
│   ├── nutrition_service.py
│   └── service.py
│
├── data/
│   ├── _make_samples.py
│   ├── bread_cheese.png
│   ├── broccoli_egg.png
│   ├── egg_avocado_bread.png
│   ├── no_meal_blue.png
│   └── other sample images
│
├── tests/
│   ├── conftest.py
│   ├── test_ai_smoke.py
│   ├── test_api.py
│   ├── test_cache.py
│   ├── test_cli.py
│   ├── test_history_service.py
│   ├── test_nutrition_service.py
│   └── test_service.py
│
├── .dockerignore
├── benchmark.py
├── demo_ai.py
├── Dockerfile
├── README.md
├── requirements.txt
├── requirements-ai.txt
└── TOPIC.md
```

---

## Requirements

- Python 3.12 or compatible version
- pip
- PostgreSQL for persistent history storage
- Docker (optional)

---

## Installation

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-ai.txt
```

---

## Command Line Interface

To analyze an image using the application CLI:

```bash
python -m app.cli data/rice_chicken.png
```

The CLI returns the identified ingredients, estimated portion sizes, confidence values, and total nutrition information.

Example output format:

```text
Ingredients:
- white rice: 180 g
- grilled chicken breast: 150 g

Nutrition totals:
Calories: ...
Protein: ...
Carbs: ...
Fat: ...
```

---

## Offline Demo

The project includes an offline demonstration mode that does not require external API keys or network access.

Run:

```bash
python demo_ai.py --offline
python demo_ai.py --offline --image data/rice_chicken_broccoli.png
python demo_ai.py --offline --image data/no_meal_blue.png
```

The provided images in the `data/` directory can be used with the offline demo.

For example:

```bash
python demo_ai.py --offline --image data/salmon_broccoli_rice.png
```

The offline demo uses deterministic sample mappings and nutrition data. It is intended for demonstrating the application workflow without external API services.

---

## Non-Food Image Handling

The sample dataset contains:

```text
data/no_meal_blue.png
```

This image is intentionally not a meal.

Run:

```bash
python demo_ai.py --offline --image data/no_meal_blue.png
```

Expected result:

```text
Meal not recognized in image.
```

This demonstrates graceful handling when no meal can be identified.

---

## HTTP API

Start the FastAPI server with:

```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000
```

The API is available at:

```text
http://localhost:8000
```

Interactive Swagger documentation is available at:

```text
http://localhost:8000/docs
```

### Health Check

Endpoint:

```text
GET /health
```

Expected response:

```json
{
  "status": "ok"
}
```

### Analyze Image

Endpoint:

```text
POST /analyze
```

The endpoint accepts an uploaded JPEG or PNG image.

The API validates the uploaded file type and maximum image size before processing it.

---

## Nutrition Lookup and Concurrency

Nutrition information is retrieved for identified ingredients.

When multiple ingredients are detected, nutrition lookups are executed concurrently using:

```python
asyncio.gather()
```

This reduces the total waiting time compared with sequential nutrition lookups.

---

## Nutrition Cache

Nutrition lookup results are cached to avoid unnecessary repeated external requests.

The default cache Time-To-Live (TTL) is:

```text
86400 seconds
```

which is equivalent to 24 hours.

The value can be configured using:

```env
NUTRITION_CACHE_TTL_SECONDS=86400
```

---

## Database and History

The project uses PostgreSQL with AsyncPG for persistent analysis history.

The database connection is configured using:

```env
DATABASE_URL=postgresql+asyncpg://postgres:dev@localhost:5432/foodanalyzer
```

Analysis history can store information such as:

- Timestamp
- Image path
- Detected ingredients
- Calories
- Protein
- Carbohydrates
- Fat

Database operations are implemented asynchronously.

---

## Input Validation and Error Handling

The application includes validation and error handling for cases such as:

- Missing image files
- Unsupported uploaded file types
- Images larger than the configured maximum size
- Images where no meal is recognized
- Provider-related failures

For example, when a CLI image path does not exist:

```bash
python -m app.cli data/not_existing_image.png
```

the application reports:

```text
Error: Image not found: data/not_existing_image.png
```

instead of displaying an unhandled traceback to the user.

---

## Testing

Run the AI-layer smoke tests:

```bash
python -m pytest tests/test_ai_smoke.py -v
```

Current verified AI smoke-test result:

```text
29 passed
```

Run the complete test suite:

```bash
python -m pytest -v
```

Current verified result:

```text
45 passed
```

The test suite covers the main application components, including:

- AI smoke tests
- API
- Cache
- CLI
- History service
- Nutrition service
- Main analysis service

---

## Test Coverage

Run:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Current measured application coverage:

```text
89%
```

This exceeds the project's minimum testing coverage target of 60%.

---

## Concurrency Benchmark

The project includes:

```text
benchmark.py
```

Run the benchmark with:

```bash
python benchmark.py
```

Measured result:

```text
Ingredients: 5
Sequential time: 2.56 seconds
Concurrent time: 0.50 seconds
Speedup: 5.11x
```

The benchmark demonstrates the benefit of concurrent execution for independent I/O-style nutrition lookups.

The benchmark uses simulated asynchronous lookup delays so that the comparison is deterministic and does not depend on external API or network performance.

---

## USDA Energy Unit Handling

USDA search responses may include energy values in both `KCAL` and `kJ`. The nutrition parser uses the `KCAL` value for `kcal_per_100g` and ignores the duplicate `kJ` energy entry. This prevents kilojoule values from being interpreted as kilocalories.

---

## Docker

The application can also run inside a Docker container.

### Build the Docker image

```bash
docker build -t food-analyzer .
```

### Run the container

```bash
docker run --name food-analyzer-container -p 8000:8000 food-analyzer
```

After the container starts, Uvicorn serves the API on port `8000`.

Open:

```text
http://localhost:8000/docs
```

to access the interactive API documentation.

To stop the running container, press:

```text
CTRL+C
```

If the stopped container needs to be removed:

```bash
docker rm food-analyzer-container
```

---

## Sample Images

The `data/` directory contains multiple sample images for demonstration and testing, including combinations such as:

- Bread and cheese
- Broccoli and egg
- Egg, avocado and bread
- Pasta and chicken
- Potato and chicken
- Rice and chicken
- Rice, chicken and broccoli
- Salads
- Salmon meals

It also contains `no_meal_blue.png` for testing the no-meal case.

---

## Technologies Used

- Python
- asyncio
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- AsyncPG
- PostgreSQL
- USDA FoodData Central
- Vision Language Models
- Pytest
- pytest-cov
- Docker

---

## Verified Project Results

The current implementation has been verified with the following results:

| Item | Result |
|---|---:|
| AI smoke tests | 29 passed |
| Automated tests | 45 passed |
| Application test coverage | 89% |
| Sequential benchmark | 2.56 s |
| Concurrent benchmark | 0.50 s |
| Concurrency speedup | 5.11x |
| Docker image build | Successful |
| Docker API startup | Successful |
| Non-food sample handling | Successful |
| Real HTTP `POST /analyze` workflow | 200 OK |

---

## Notes

The `ai/` package contains the provided AI functionality and is kept separate from the Software Engineering application layer.

The `app/` package implements the main application architecture around the provided AI components, including CLI/API access, caching, concurrency, persistence, validation, and error handling.

The offline demo provides deterministic testing without external services, while the provider workflow supports real VLM analysis and USDA nutrition lookup.

---

## Project

**Software Engineering Final Project**

**Topic 2: AI Food Analyzer**
````