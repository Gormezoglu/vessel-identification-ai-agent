# Key Questions Answers

## 1. How can you determine when two records refer to the same vessel?

To determine if two records refer to the same vessel, we employ an identity resolution process:

- **Primary Identifiers:** Prioritize globally unique identifiers like the IMO Number. Records sharing the same valid IMO are strong candidates for being the same vessel.
- **Secondary Identifiers:** Utilize other unique or semi-unique identifiers such as MMSI Number, Vessel Name, and Callsign. While these can change or be duplicated, they serve as strong grouping mechanisms.
- **Attribute Similarity:** For records grouped by primary/secondary identifiers, compare static attributes (e.g., length, width, vessel_type, builtYear). High similarity across multiple attributes further confirms they are the same vessel.
- **Temporal Proximity:** Consider the UpdateDate or InsertDate to prioritize more recent or relevant records when merging.
- **Merging Strategy:** Implement a "golden record" creation process where conflicting values are resolved (e.g., taking the most frequent value for static attributes, or the most recent for dynamic attributes).

## 2. How would you detect and flag invalid or conflicting records?

Detecting and flagging invalid or conflicting records is crucial for data quality:

- **Data Validation Rules:**
  - *IMO Number Validation:* Implement a check-digit algorithm to verify the mathematical validity of IMO numbers. Invalid IMOs (like '0' or those failing the check) are flagged.
  - *MMSI Validation:* Check for correct length and format of MMSI numbers.
  - *Range Checks:* Ensure numerical values (e.g., length, width, draught) fall within plausible ranges.
  - *Categorical Consistency:* Validate vessel_type and flag against predefined lists.
- **Duplicate Detection:** Identify records with identical primary keys (IMO) but differing secondary attributes, or records with different primary keys but highly similar secondary attributes.
- **Conflict Resolution during Identity Resolution:** During golden record creation, if conflicting values for a supposedly static attribute are found (e.g., two different vessel_type for the same IMO), these are flagged for review or resolved using predefined rules (e.g., majority vote, most recent).
- **Outlier Detection:** Use statistical methods to identify values that deviate significantly from the norm for a given vessel type or attribute.

## 3. How could you track a vessel’s changes over time (e.g., name, flag, MMSI)?

Tracking changes over time is essential for maintaining an accurate vessel history:

- **Versioning Golden Records:** Instead of simply overwriting, each update to a golden record could create a new version, preserving the historical state.
- **Historical Data Tables:** Maintain separate tables or fields to store historical values for attributes prone to change (e.g., a list of all known MMSIs, a log of name changes with dates).
- **Timestamping:** Every record and every change should be associated with a timestamp (UpdateDate, staticData_updateTimestamp) to understand the chronology of information.
- **Audit Logs:** Implement an audit trail for all modifications to vessel records, detailing who made the change, when, and what was changed.

## 4. Is it realistic to create a “ground truth” vessel database? How?

Yes, it is realistic to create a "ground truth" vessel database, but it's an ongoing process rather than a one-time event.

- **Robust Identity Resolution:** The core is a sophisticated identity resolution system that consistently and accurately merges disparate records into single, authoritative "golden records."
- **Continuous Data Ingestion & Cleaning:** A pipeline that continuously ingests new data, applies validation rules, and updates existing golden records or creates new ones.
- **Human-in-the-Loop:** For complex or ambiguous conflicts that automated rules cannot resolve, a human review process is essential. Data stewards would manually verify and correct records.
- **Feedback Loops:** Mechanisms to incorporate feedback from users or external sources to correct errors and improve data quality over time.
- **Data Governance:** Clear policies and procedures for data entry, updates, and quality control.

## 5. What system design would you propose for a search & retrieval solution?

For a robust search and retrieval solution, I propose the following system design:

- **Data Ingestion & Processing Layer:** A Python-based pipeline (e.g., orchestrated by Apache Airflow) that ingests raw data, performs cleaning and identity resolution (generating golden records), and loads them into the storage layer.
- **Storage Layer (Elasticsearch):** Elasticsearch is ideal for storing the golden records. Its strengths include:
  - Full-Text Search: Excellent for searching vessel names, callsigns, and other textual data.
  - Scalability: Easily scales horizontally to handle large datasets and high query loads.
  - Flexible Schema: Accommodates the semi-structured nature of vessel data, including lists of identifiers.
  - Fast Retrieval: Optimized for quick search and aggregation queries.
- **API Layer (FastAPI):** A RESTful API built with FastAPI (Python) to expose search functionalities. This API would:
  - Receive search queries (e.g., by IMO, MMSI, name, or general keywords).
  - Translate these queries into Elasticsearch queries.
  - Retrieve and format results from Elasticsearch.
  - Provide a clean, well-documented interface for various clients.
- **Caching Layer:** Implement caching (e.g., Redis) for frequently accessed queries to reduce load on Elasticsearch and improve response times.

## 6. How could a conversational AI interface support vessel search?

A conversational AI interface can significantly enhance vessel search by making it more intuitive and accessible:

- **Natural Language Understanding (NLU):** An LLM would process user queries in natural language (e.g., "Where is the vessel with IMO 9710749?").
- **Intent Recognition:** The LLM would identify the user's intent (e.g., get_position, get_name, search_by_type).
- **Entity Extraction:** The LLM would extract relevant entities from the query (e.g., imo_number=9710749, vessel_type=cargo ship).
- **API Integration:** The extracted intent and entities would be used to construct a structured query to our FastAPI search API.
- **Response Generation:** The LLM would then take the structured results from the API and synthesize them into a natural, human-readable answer for the user.
- **Contextual Conversations:** The AI could maintain conversational context, allowing follow-up questions (e.g., "What about its flag?") without needing to re-specify the vessel.

## 7. How would you prevent LLM hallucinations when answering vessel-related queries?

Preventing LLM hallucinations is critical for factual accuracy:

- **Retrieval-Augmented Generation (RAG):** The LLM is explicitly instructed to only use information retrieved from our authoritative vessel database (via the search API). It should not generate facts from its own training data.
- **Strict Prompt Engineering:** The system prompt for the LLM would include clear directives:
  - "You must only use the information provided in the API response."
  - "If the information is not in the response, state that you do not have that information."
  - "Do not make up information or infer facts not present in the provided data."
- **Structured API Responses:** Ensure the search API returns data in a clear, structured format that the LLM can easily parse and understand.
- **Confidence Scoring (Advanced):** If the LLM's confidence in its answer is below a certain threshold, it could either ask for clarification or state that it's unsure.

## 8. What evaluation methods would you use to measure the effectiveness of an AI-powered vessel search system?

Evaluating the effectiveness requires a multi-faceted approach:

- **For the Search & Retrieval Component (API):**
  - Precision, Recall, F1-Score: Standard information retrieval metrics to measure the accuracy and completeness of search results for given queries.
  - Mean Average Precision (MAP): For ranked search results.
  - Latency: Measuring the response time of the API.
  - Throughput: Assessing the number of queries the system can handle per second.
- **For the Conversational AI Component:**
  - Intent Recognition Accuracy: How often the LLM correctly identifies the user's intent.
  - Entity Extraction Accuracy: How accurately the LLM extracts relevant entities.
  - Factuality/Hallucination Rate: Manually or semi-automatically checking if the LLM's answers are factually correct and grounded in the database, or if it hallucinates.
  - User Satisfaction (UX): Conduct user studies or surveys to gather feedback on the naturalness, helpfulness, and ease of use of the conversational interface.
  - Turn-taking and Coherence: Evaluate how well the AI maintains context and provides coherent responses over multiple turns.
- **Overall System:**
  - End-to-End Accuracy: Measure the success rate of users finding the information they need through the conversational interface.
  - Data Freshness: How quickly new data is ingested and reflected in search results.