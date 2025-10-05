
# System Design: Vessel Identification & AI Agent

This document outlines the high-level design for the AI-powered vessel identification and search system.

## 1. Overview

The system is designed to solve the problem of vessel identity resolution from noisy data and provide a robust search solution with a conversational AI interface.

The architecture is divided into four main components:

1.  **Data Ingestion & Processing:** A pipeline to ingest, clean, and process raw vessel data to create "golden records".
2.  **Storage:** A database to store the golden records.
3.  **Search & Retrieval API:** A REST API to search and retrieve vessel information.
4.  **Conversational AI:** A conversational interface to interact with the system using natural language.

## 2. System Architecture

Raw Data (CSV) --> Data Ingestion & Processing (Python Script) --> Storage (Elasticsearch) <-- Search & Retrieval API (FastAPI) <-- Conversational AI (LLM)

## 3. Components

### 3.1. Data Ingestion & Processing

-   **Input:** Raw vessel data in CSV format.
-   **Processing:** A Python script (`vessel_analysis.py`) performs the following steps:
    1.  **Data Cleaning:** Removes unreliable columns and validates IMO numbers.
    2.  **Identity Resolution:** Groups records by IMO and creates a "golden record" for each vessel using a defined merging strategy.
-   **Orchestration:** This process can be automated using a workflow manager like **Apache Airflow** to run periodically.

### 3.2. Storage

-   **Database:** **Elasticsearch** is chosen as the primary data store.
-   **Reasoning:**
    -   Excellent full-text search capabilities, which are crucial for the conversational AI.
    -   Scalable and can handle large volumes of data.
    -   Flexible schema to accommodate the structure of our golden records.
-   **Data Model:** The golden records will be stored as documents in an Elasticsearch index. Fields with multiple values (like `mmsi` and `name`) will be stored as arrays.

### 3.3. Search & Retrieval API

-   **Framework:** A REST API will be built using **FastAPI** (a modern, fast Python web framework).
-   **Endpoint:**
    -   `GET /vessels/search`: Searches for vessels based on query parameters.
        -   `q`: A query string for general search.
        -   `imo`, `mmsi`, `name`: Specific fields for targeted search.
-   **Implementation:** The API will query the Elasticsearch index and return the search results in JSON format.

### 3.4. Conversational AI

-   **Model:** A large language model (LLM) will be used to power the conversational interface.
-   **Interaction Flow:**
    1.  The user asks a question in natural language (e.g., "What is the current position of the vessel with IMO 9710749?").
    2.  The LLM understands the user's intent and constructs a query for our Search & Retrieval API.
    3.  The API returns the relevant vessel information.
    4.  The LLM uses the API response to generate a natural language answer for the user.
-   **Preventing Hallucinations:** The LLM will be given a strict prompt that forces it to only use the information returned from the API. The prompt will include instructions like: "You must only use the information provided in the API response. If the information is not in the response, state that you do not have that information."

## 4. Next Steps

-   **Implementation:**
    1.  Set up an Elasticsearch instance.
    2.  Develop the FastAPI application for the search API.
    3.  Integrate the LLM with the search API.
-   **Evaluation:**
    -   The effectiveness of the search system can be measured using standard information retrieval metrics (e.g., precision, recall, F1-score).
    -   The conversational AI can be evaluated based on user satisfaction and the accuracy of its responses.
