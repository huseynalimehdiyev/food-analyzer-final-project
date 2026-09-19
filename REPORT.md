    # AI Food Analyzer
    ## Software Engineering Final Project Report

    **Topic:** Topic 2 — AI Food Analyzer

    ---

    # 1. Introduction

    AI Food Analyzer is a Python-based application designed to analyze meal images and estimate their nutritional content.

    The system receives an image of a meal, identifies visible food ingredients using a Vision Language Model (VLM), estimates the amount of each ingredient in grams, retrieves nutritional information, and calculates the total calories and macronutrients of the meal.

    The project focuses not only on AI functionality but also on software engineering principles. The implementation therefore includes asynchronous programming, concurrency, caching, persistence, input validation, error handling, automated testing, an HTTP API, a command-line interface, configuration management, and Docker containerization.

    The provided `ai/` package contains the core AI-related functionality. The Software Engineering layer is implemented separately in the `app/` package.

    ---

    # 2. Project Objectives

    The main objective of the project is to build a structured software application around the provided AI Food Analyzer components.

    The system is designed to:

    1. Accept a meal image.
    2. Identify visible ingredients.
    3. Estimate ingredient portions in grams.
    4. Retrieve nutritional information.
    5. Calculate total calories, protein, carbohydrates, and fat.
    6. Perform independent nutrition lookups concurrently.
    7. Cache nutrition results.
    8. Store analysis history using PostgreSQL.
    9. Provide both CLI and HTTP interfaces.
    10. Validate user input and handle errors gracefully.
    11. Support automated testing.
    12. Run inside a Docker container.

    ---

    # 3. System Architecture

    The application uses a layered architecture.

    ```text
    User
      |
      +-------------------+
      |                   |
     CLI               HTTP API
      |                   |
      +--------+----------+
               |
          Validation
               |
               v
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
        Nutrition Totals
               |
               v
          PostgreSQL
    ```

    This separation makes individual components easier to understand, test, maintain, and extend.

    ---

    # 4. AI Layer

    The `ai/` package contains the provided AI functionality.

    Important modules include:

    - `vlm.py` — image analysis and ingredient recognition.
    - `schemas.py` — structured data models for ingredients and nutrition.
    - `nutrition.py` — nutrition provider functionality.
    - `calculator.py` — nutrition calculations.
    - `providers/` — configurable VLM provider implementations.

    The VLM produces structured ingredient information including:

    - Ingredient name
    - Estimated grams
    - Confidence

    The AI layer is kept separate from the Software Engineering application layer.

    ---

    # 5. Application Layer

    The `app/` package contains the main Software Engineering implementation.

    The application layer contains:

    ```text
    api.py
    cache.py
    cli.py
    config.py
    database.py
    history_service.py
    models.py
    nutrition_service.py
    service.py
    ```

    Each module has a separate responsibility.

    This modular design reduces coupling and improves testability.

    ---

    # 6. Main Analysis Service

    The main application service coordinates the analysis workflow.

    The workflow is:

    ```text
    Image
      ↓
    Image Validation
      ↓
    VLM Analysis
      ↓
    Ingredients
      ↓
    Concurrent Nutrition Lookup
      ↓
    Nutrition Calculation
      ↓
    Final Result
    ```

    The service acts as an orchestration layer between the AI functionality and the rest of the application.

    ---

    # 7. Nutrition Processing

    After ingredients are identified, nutritional information is retrieved for each ingredient.

    Nutrition data includes:

    - Calories
    - Protein
    - Carbohydrates
    - Fat

    The nutrition values are scaled according to the VLM-estimated amount of each ingredient.

    For example, if nutrition information is provided per 100 grams, the application calculates the appropriate nutritional value for the estimated portion.

    The final nutrition values for all ingredients are then combined to produce the total meal nutrition.

    During real nutrition-provider verification, USDA search results were found to include Energy in both `KCAL` and `kJ`. The nutrition extraction logic was adjusted to use the `KCAL` Energy entry for `kcal_per_100g` and ignore the `kJ` Energy entry. This prevents kilojoule values from being interpreted as kilocalories.

    ---

    # 8. Asynchronous Programming

    Nutrition lookups are I/O-oriented operations.

    If multiple ingredients are identified, performing the lookups sequentially would increase total waiting time.

    The application therefore uses asynchronous programming with Python `asyncio`.

    Independent nutrition lookups can execute concurrently.

    The main concurrency mechanism is:

    ```python
    asyncio.gather()
    ```

    This allows the application to wait for multiple independent operations at the same time instead of waiting for each lookup sequentially.

    ---

    # 9. Concurrency Benchmark

    A benchmark was created to measure the benefit of concurrent execution.

    The benchmark used five simulated nutrition lookups. Each lookup contained a simulated I/O delay.

    The measured results were:

    ```text
    Ingredients: 5
    Sequential time: 2.56 seconds
    Concurrent time: 0.50 seconds
    Speedup: 5.11x
    ```

    The concurrent implementation was therefore approximately 5.11 times faster in this controlled benchmark.

    The benchmark uses simulated delays instead of an external API. This makes the experiment deterministic and prevents network latency, API availability, or rate limits from affecting the comparison.

    The benchmark can be executed with:

    ```bash
    python benchmark.py
    ```

    ---

    # 10. Nutrition Cache

    The project implements caching for nutrition lookups.

    If the same nutrition information is requested repeatedly, the application can use a cached value rather than performing the same lookup again.

    The default cache TTL is 86400 seconds, which corresponds to 24 hours.

    Caching can reduce repeated external API requests and improve response time.

    ---

    # 11. PostgreSQL Persistence

    The application includes persistence for analysis history.

    PostgreSQL is used as the database, while SQLAlchemy and AsyncPG provide asynchronous database access.

    Analysis history can contain:

    - Timestamp
    - Image path
    - Detected ingredients
    - Calories
    - Protein
    - Carbohydrates
    - Fat

    Database operations are performed asynchronously.

    This allows analysis results to be retained instead of existing only during a single application execution.

    ---

    # 12. Command Line Interface

    The project provides a CLI for running analysis directly from a terminal.

    General usage:

    ```bash
    python -m app.cli <image_path>
    ```

    Example:

    ```bash
    python -m app.cli data/rice_chicken.png
    ```

    The CLI displays identified ingredients and total nutritional values.

    The CLI also includes user-friendly error handling.

    For example:

    ```bash
    python -m app.cli data/not_existing_image.png
    ```

    produces:

    ```text
    Error: Image not found: data/not_existing_image.png
    ```

    instead of displaying an unhandled Python traceback.

    ---

    # 13. HTTP API

    The application provides an HTTP interface using FastAPI.

    The server can be started with:

    ```bash
    uvicorn app.api:app --host 0.0.0.0 --port 8000
    ```

    The API includes:

    ```text
    GET /health
    ```

    and:

    ```text
    POST /analyze
    ```

    The health endpoint returns:

    ```json
    {
      "status": "ok"
    }
    ```

    The `/analyze` endpoint accepts meal images.

    Supported image content types include:

    ```text
    image/jpeg
    image/png
    ```

    The API also validates image size.

    The configured default maximum image size is:

    ```text
    5 MB
    ```

    Unsupported file types return HTTP status `400`, while oversized images return HTTP status `413`.

    The real provider workflow was also verified through the Swagger interface. A meal image was uploaded to `POST /analyze`, and the API completed the analysis successfully with HTTP status `200 OK`. This verified the end-to-end flow from image upload through VLM analysis, nutrition lookup, calculation, and JSON response.

    ---

    # 14. Input Validation and Error Handling

    Input validation is an important part of the application.

    The implementation handles scenarios such as:

    - Missing image paths
    - Unsupported uploaded file types
    - Oversized uploaded images
    - Images where no meal is detected
    - Missing provider credentials
    - Provider-related failures

    The objective is to avoid uncontrolled application failures and provide understandable responses to users.

    ---

    # 15. Offline Demonstration

    External AI and nutrition APIs require valid credentials.

    For demonstration and deterministic testing, the project includes an offline mode through `demo_ai.py`.

    The required offline demonstration commands are:

    ```bash
    python demo_ai.py --offline
    python demo_ai.py --offline --image data/rice_chicken_broccoli.png
    python demo_ai.py --offline --image data/no_meal_blue.png
    ```

    The offline implementation uses deterministic sample mappings and local nutrition values.

    Therefore, it demonstrates the application workflow without claiming to perform real VLM inference.

    ---

    # 16. Sample Image Testing

    The `data/` directory contains multiple sample meal images.

    The offline demonstration was executed against the sample images to verify different ingredient combinations.

    Examples include:

    - Bread and cheese
    - Broccoli and egg
    - Egg, avocado and bread
    - Pasta and chicken
    - Potato and chicken
    - Rice and chicken
    - Rice, chicken and broccoli
    - Salad combinations
    - Salmon meals

    The dataset also includes:

    ```text
    no_meal_blue.png
    ```

    This image represents the no-meal scenario.

    The application returned:

    ```text
    Meal not recognized in image.
    ```

    This demonstrates graceful handling of a non-meal sample.

    ---

    # 17. Automated Testing

    Automated testing is implemented using `pytest`.

    The test suite covers the main application components, including:

    - AI smoke testing
    - API behavior
    - Cache behavior
    - CLI behavior
    - History service
    - Nutrition service
    - Main application service

    The AI-layer smoke tests were executed with:

    ```bash
    python -m pytest tests/test_ai_smoke.py -v
    ```

    The verified result was:

    ```text
    29 passed
    ```

    The complete test suite was then executed with:

    ```bash
    python -m pytest -v
    ```

    The verified result was:

    ```text
    45 passed
    ```

    After improving CLI error handling, the full test suite was executed again to perform regression testing.

    The result remained:

    ```text
    45 passed
    ```

    This confirmed that the change did not break the existing tested functionality.

    ---

    # 18. Test Coverage

    Test coverage was measured using `pytest-cov`.

    Command:

    ```bash
    python -m pytest --cov=app --cov-report=term-missing
    ```

    The measured total application coverage was:

    ```text
    89%
    ```

    The project target is a minimum of 60% test coverage.

    The implementation therefore exceeds the required coverage target.

    ---

    # 19. Docker Containerization

    The application was containerized using Docker.

    The Docker image is built with:

    ```bash
    docker build -t food-analyzer .
    ```

    The container is started with:

    ```bash
    docker run --name food-analyzer-container -p 8000:8000 food-analyzer
    ```

    During verification, the Docker image was built successfully and the FastAPI application started successfully inside the container.

    Uvicorn reported:

    ```text
    Application startup complete.
    Uvicorn running on http://0.0.0.0:8000
    ```

    The host health endpoint was then tested and returned:

    ```json
    {
      "status": "ok"
    }
    ```

    This confirmed that the HTTP API could run successfully from the Docker container.

    ---

    # 20. Technology Stack

    The project uses the following technologies:

    - Python
    - asyncio
    - FastAPI
    - Uvicorn
    - Pydantic
    - SQLAlchemy
    - AsyncPG
    - PostgreSQL
    - USDA FoodData Central integration
    - Vision Language Model providers
    - pytest
    - pytest-cov
    - Docker

    ---

    # 21. Verified Results

    The main verified project results are summarized below:

    | Verification | Result |
    |---|---:|
    | AI smoke tests | 29 passed |
    | Automated tests | 45 passed |
    | Test coverage | 89% |
    | Sequential benchmark | 2.56 s |
    | Concurrent benchmark | 0.50 s |
    | Concurrency speedup | 5.11x |
    | Docker image build | Successful |
    | Docker API startup | Successful |
    | Docker health check | Successful |
    | Offline sample processing | Successful |
    | Non-meal handling | Successful |
    | CLI invalid-path handling | Successful |
    | Real HTTP `/analyze` workflow | 200 OK |

    ---

    # 22. Limitations

    The current project has several practical limitations.

    First, real meal recognition depends on an external VLM provider and valid API credentials.

    Second, nutritional accuracy depends on the correctness of ingredient identification, portion estimation, and the nutritional data returned by the configured nutrition provider.

    Third, the concurrency benchmark uses simulated I/O delays. It demonstrates the behavior and potential benefit of concurrent I/O, but it should not be interpreted as a guaranteed 5.11x performance improvement for every real external API request.

    Fourth, the offline demonstration is deterministic and designed for testing and demonstration. It does not replace real VLM inference.

    ---

    # 23. Future Improvements

    Possible future improvements include:

    - More advanced portion-size estimation
    - Additional nutrition providers
    - Persistent or distributed caching
    - Improved logging and observability
    - More detailed API error responses
    - Extended database history queries
    - Additional integration tests
    - Authentication and user accounts
    - A graphical web interface
    - Deployment to a cloud environment

    ---

    # 24. Conclusion

    The AI Food Analyzer project demonstrates how AI functionality can be integrated into a structured Software Engineering application.

    The implementation combines meal-image analysis and nutritional calculation with application-level engineering features such as asynchronous execution, concurrency, caching, persistence, CLI and HTTP interfaces, configuration management, validation, automated testing, and containerization.

    The final implementation achieved:

    ```text
    29 passing AI smoke tests
    45 passing automated tests
    89% application test coverage
    5.11x speedup in the controlled concurrency benchmark
    Successful real HTTP API analysis with 200 OK
    Successful Docker deployment and API health verification
    ```

    The project therefore demonstrates both the AI analysis workflow and the Software Engineering practices required to build a maintainable and testable application.
