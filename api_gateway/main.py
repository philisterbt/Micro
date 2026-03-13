import os
from fastapi import FastAPI, Request, HTTPException
import requests

app = FastAPI(title="API Gateway")

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
NOTE_SERVICE_URL = os.getenv("NOTE_SERVICE_URL", "http://note-service:8000")

@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def auth_proxy(request: Request, path: str):
    url = f"{AUTH_SERVICE_URL}/{path}"
    return await proxy_request(request, url)

@app.api_route("/notes/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def note_proxy(request: Request, path: str):
    url = f"{NOTE_SERVICE_URL}/{path}"
    return await proxy_request(request, url)

async def proxy_request(request: Request, url: str):
    body = await request.body()
    headers = dict(request.headers)
    method = request.method
    params = request.query_params
    
    try:
        resp = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=body,
            timeout=5
        )
        return resp.json(), resp.status_code
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}
