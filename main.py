from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import requests
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_API_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}"

headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "mybuddyhq.ai Admin Console API is live"}

@app.post("/function-router")
async def function_router(request: Request):
    body = await request.json()
    function_name = body.get("function_name")
    arguments = body.get("arguments", {})

    if function_name == "add_record":
        return add_record(arguments)
    elif function_name == "update_record":
        return update_record(arguments)
    elif function_name == "delete_record":
        return delete_record(arguments)
    else:
        return JSONResponse(content={"error": f"Function '{function_name}' not supported"}, status_code=400)

def add_record(args):
    table = args.get("table")
    record = args.get("record")
    response = requests.post(f"{AIRTABLE_API_URL}/{table}", json={"fields": record}, headers=headers)
    return JSONResponse(content=response.json(), status_code=response.status_code)

def update_record(args):
    table = args.get("table")
    record_id = args.get("record_id")
    fields = args.get("fields")
    response = requests.patch(f"{AIRTABLE_API_URL}/{table}/{record_id}", json={"fields": fields}, headers=headers)
    return JSONResponse(content=response.json(), status_code=response.status_code)

def delete_record(args):
    table = args.get("table")
    record_id = args.get("record_id")
    response = requests.delete(f"{AIRTABLE_API_URL}/{table}/{record_id}", headers=headers)
    return JSONResponse(content=response.json(), status_code=response.status_code)
