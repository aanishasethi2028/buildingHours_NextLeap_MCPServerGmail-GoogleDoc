import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from docs_tool import append_to_doc
from gmail_tool import create_email_draft

app = FastAPI(title="Google Docs and Gmail MCP Server")


class AppendDocRequest(BaseModel):
    doc_id: str
    content: str


class CreateEmailDraftRequest(BaseModel):
    to: str
    subject: str
    body: str


@app.post("/append_to_doc")
async def append_to_doc_endpoint(req: AppendDocRequest):
    try:
        # Run synchronous function in thread pool to avoid blocking async event loop
        result = await asyncio.to_thread(append_to_doc, req.doc_id, req.content)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/create_email_draft")
async def create_email_draft_endpoint(req: CreateEmailDraftRequest):
    try:
        # Run synchronous function in thread pool to avoid blocking async event loop
        result = await asyncio.to_thread(create_email_draft, req.to, req.subject, req.body)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
