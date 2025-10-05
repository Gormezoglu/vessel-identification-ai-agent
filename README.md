# Vessel Identification & AI Agent

This project is a solution to the case study on vessel identification and AI-powered search. It includes a data processing pipeline to clean and de-duplicate vessel data, and a web API to search for vessels.

## Project Structure
-   `app/`: Contains the FastAPI application code.
-   `Dockerfile`: Docker configuration file.
- `vessel_analysis.py`: Python script for data ingestion and processing.
-   `system_design.md`: Document outlining the system design.
-   `answers_of_key_questions.md`: Document answering key questions about the project.
- `implementation_examples.md`: Document with code examples for implementation.
-   `requirements.txt`: Python dependencies.

## Prerequisites

- Docker installed on your machine.

## How to Run

1.  **Build the Docker image:**

    ```bash
    docker build -t vessel-identification-app .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run -p 8000:8000 vessel-identification-app
    ```

3.  **Access the API:**

    The API will be available at `http://localhost:8000`.

## API Usage

-   **Root:** `http://localhost:8000/`

    Returns a welcome message.

-   **Search:** `http://localhost:8000/search`

    Search for vessels using the following query parameters:

    -   `imo`: Search by IMO number.
    -   `mmsi`: Search by MMSI number.
    -   `name`: Search by vessel name (case-insensitive, partial match).

    **Example Queries:**

    -   `http://localhost:8000/search?imo=9710749`
    -   `http://localhost:8000/search?mmsi=259274000`
    -   `http://localhost:8000/search?name=HOEGH`



