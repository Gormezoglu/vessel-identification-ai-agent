
# Implementation Examples

This document provides illustrative code snippets for the Search & Retrieval API and the Conversational AI, as described in the `system_design.md` file.

## 1. Search & Retrieval API (FastAPI)

This code snippet shows a simplified implementation of the search endpoint using FastAPI. It demonstrates how to connect to Elasticsearch and perform a search query.

```python
from fastapi import FastAPI
from elasticsearch import Elasticsearch

app = FastAPI()

# Connect to Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

@app.get("/vessels/search")
def search_vessels(q: str = None, imo: int = None, mmsi: int = None, name: str = None):
    """
    Search for vessels in the Elasticsearch index.
    """
    if not any([q, imo, mmsi, name]):
        return {"error": "Please provide a search query."}

    query = {
        "query": {
            "bool": {
                "should": []
            }
        }
    }

    if q:
        query["query"]["bool"]["should"].append({"multi_match": {"query": q, "fields": ["name", "imo", "mmsi"]}})
    if imo:
        query["query"]["bool"]["should"].append({"term": {"imo": imo}})
    if mmsi:
        query["query"]["bool"]["should"].append({"term": {"mmsi": mmsi}})
    if name:
        query["query"]["bool"]["should"].append({"match": {"name": name}})

    res = es.search(index="vessels", body=query)

    return {"results": [hit["_source"] for hit in res["hits"]["hits"]]}

```

## 2. Conversational AI (LLM Prompt)

This is an example of a prompt that could be used to instruct a large language model (LLM) to interact with our search API. The key is to provide a clear set of instructions and constraints to ensure the LLM behaves as expected.

```
**System Prompt:**

You are a helpful assistant for querying vessel information. Your task is to answer user questions about vessels by using the provided Search API. 

**Instructions:**

1.  When the user asks a question, you must first determine the user's intent and the key information they are looking for.
2.  Based on the user's query, you must construct a URL for the Search API. The available endpoints are:
    -   `/vessels/search?q=<query>`
    -   `/vessels/search?imo=<imo_number>`
    -   `/vessels/search?mmsi=<mmsi_number>`
    -   `/vessels/search?name=<vessel_name>`
3.  You will be given the JSON response from the API. You must use **only** the information from this response to answer the user's question.
4.  If the API response is empty or does not contain the information needed to answer the question, you must inform the user that you do not have that information. **Do not make up information.**
5.  Present the answer to the user in a clear and concise way.

**Example Interaction:**

**User:** "What is the current position of the vessel with IMO 9710749?"

**LLM (Internal Thought):** The user is asking for the position of a vessel with a specific IMO. I need to call the Search API with the IMO number.

**LLM (API Call):** `/vessels/search?imo=9710749`

**API Response:**
```json
{
  "results": [
    {
      "imo": 9710749,
      "name": ["HOEGH TROTTER"],
      "last_position_latitude": 34.805867,
      "last_position_longitude": 129.374107,
      "last_position_updateTimestamp": "2025-09-15 08:47:32.000"
    }
  ]
}
```

**LLM (Response to User):** "The vessel with IMO 9710749, named HOEGH TROTTER, was last reported at latitude 34.805867 and longitude 129.374107 on September 15, 2025."

```
