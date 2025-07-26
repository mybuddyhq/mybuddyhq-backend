
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import os
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_API_URL = os.getenv("AIRTABLE_API_URL")

headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

app = FastAPI()

@app.post("/function-router")
async def function_router(request: Request):
    body = await request.json()
    function_name = body.get("function")
    args = body.get("arguments", {})

    if function_name == "add_record":
        return add_record(args)
    elif function_name == "update_record":
        return update_record(args)
    elif function_name == "delete_record":
        return delete_record(args)
    elif function_name == "get_records":
        return get_records(args)
    elif function_name == "list_tables":
        return list_tables()
    elif function_name == "create_table":
        return create_table(args)
    elif function_name == "delete_table":
        return delete_table(args)
    elif function_name == "update_table_schema":
        return update_table_schema(args)
    else:
        return JSONResponse(content={"error": "Function not supported"}, status_code=400)

def add_record(args):
    table = args.get("table")
    fields = args.get("fields", {})
    response = requests.post(f"{AIRTABLE_API_URL}/{AIRTABLE_BASE_ID}/{table}", headers=headers, json={"fields": fields})
    return JSONResponse(content=response.json(), status_code=response.status_code)

def update_record(args):
    table = args.get("table")
    record_id = args.get("record_id")
    fields = args.get("fields", {})
    response = requests.patch(f"{AIRTABLE_API_URL}/{AIRTABLE_BASE_ID}/{table}/{record_id}", headers=headers, json={"fields": fields})
    return JSONResponse(content=response.json(), status_code=response.status_code)

def delete_record(args):
    table = args.get("table")
    record_id = args.get("record_id")
    response = requests.delete(f"{AIRTABLE_API_URL}/{AIRTABLE_BASE_ID}/{table}/{record_id}", headers=headers)
    return JSONResponse(content=response.json(), status_code=response.status_code)

def get_records(args):
    table = args.get("table")
    filter_query = args.get("filter", "")
    url = f"{AIRTABLE_API_URL}/{AIRTABLE_BASE_ID}/{table}"
    params = {"filterByFormula": filter_query} if filter_query else {}
    response = requests.get(url, headers=headers, params=params)
    return JSONResponse(content=response.json(), status_code=response.status_code)

def list_tables():
    url = f"https://api.airtable.com/v0/meta/bases/{AIRTABLE_BASE_ID}/tables"
    response = requests.get(url, headers=headers)
    return JSONResponse(content=response.json(), status_code=response.status_code)

def create_table(args):
    table_name = args.get("table_name")
    fields = args.get("fields", [])
    url = f"https://api.airtable.com/v0/meta/bases/{AIRTABLE_BASE_ID}/tables"
    response = requests.post(url, headers=headers, json={"name": table_name, "fields": fields})
    return JSONResponse(content=response.json(), status_code=response.status_code)

def delete_table(args):
    table_id = args.get("table_id")
    url = f"https://api.airtable.com/v0/meta/bases/{AIRTABLE_BASE_ID}/tables/{table_id}"
    response = requests.delete(url, headers=headers)
    return JSONResponse(content=response.json(), status_code=response.status_code)

def update_table_schema(args):
    table_id = args.get("table_id")
    updates = args.get("updates", {})
    url = f"https://api.airtable.com/v0/meta/bases/{AIRTABLE_BASE_ID}/tables/{table_id}"
    response = requests.patch(url, headers=headers, json=updates)
    return JSONResponse(content=response.json(), status_code=response.status_code)
