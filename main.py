
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()

class RecordRequest(BaseModel):
    table_name: str
    action: str  # 'add', 'update', 'delete'
    record: dict = None
    record_id: str = None

@app.post("/record")
async def manage_record(req: RecordRequest):
    return {"status": "success", "action": req.action, "table": req.table_name, "record": req.record, "record_id": req.record_id}

@app.get("/")
async def root():
    return {"message": "MyBuddyHQ Admin Console API is live"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
