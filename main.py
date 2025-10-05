from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
import numpy as np
import re
import ast

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the golden records dataset
golden_records_df = pd.read_csv("golden_records.csv")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question", "").lower()

    imo = None
    mmsi = None
    name = None

    # Simple keyword matching to simulate LLM. 
    imo_match = re.search(r"imo (\d+)", question)
    if imo_match:
        imo = int(imo_match.group(1))

    mmsi_match = re.search(r"mmsi (\d+)", question)
    if mmsi_match:
        mmsi = int(mmsi_match.group(1))

    name_match = re.search(r"name (\w+)", question)
    if name_match:
        name = name_match.group(1)

    search_results = search_vessels(imo=imo, mmsi=mmsi, name=name)

    if not search_results["results"]:
        return {"answer": "I could not find a vessel matching your query."}

    vessel_data = search_results["results"][0]

    # Clean up the list-like strings
    for col in ['mmsi', 'name', 'callsign']:
        if isinstance(vessel_data[col], str):
            try:
                vessel_data[col] = ast.literal_eval(vessel_data[col])
            except (ValueError, SyntaxError):
                # If it's not a valid literal, just keep it as a string
                pass

    # Intent detection
    if "position" in question or "location" in question or "where" in question:
        answer = f"The vessel with IMO {vessel_data['imo']} is at latitude {vessel_data['last_position_latitude']} and longitude {vessel_data['last_position_longitude']}."
    elif "name" in question:
        answer = f"The vessel with IMO {vessel_data['imo']} is named {vessel_data['name']}."
    else:
        answer = "I found a vessel with the following information:\n"
        for key, value in vessel_data.items():
            answer += f"- {key}: {value}\n"

    return {"answer": answer}


@app.get("/search")
def search_vessels(imo: int = None, mmsi: int = None, name: str = None):
    """
    Search for vessels by IMO, MMSI, or name.
    """
    results = golden_records_df

    if imo:
        results = results[results["imo"] == imo]
    
    if mmsi:
        # The mmsi column contains lists of MMSIs as strings, so we search for the substring
        results = results[results["mmsi"].str.contains(str(mmsi), na=False)]

    if name:
        # The name column contains lists of names as strings, so we search for the substring
        results = results[results["name"].str.contains(name, case=False, na=False)]

    # Replace NaN with None for JSON compatibility
    results = results.replace({np.nan: None})

    return {"results": results.to_dict(orient="records")}
