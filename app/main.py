from fastapi import FastAPI, Request, HTTPException
import httpx
import os
import time

app = FastAPI()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")

token_cache = {"access_token": None, "expires_at": 0}

async def get_token():
    if token_cache["expires_at"] > time.time():
        return token_cache["access_token"]

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "scope": "https://cognitiveservices.azure.com/.default",
                "grant_type": "client_credentials",
            },
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Token request failed")

        token_data = response.json()

        token_cache["access_token"] = token_data["access_token"]
        token_cache["expires_at"] = time.time() + token_data["expires_in"] - 60

        return token_cache["access_token"]

@app.post("/v1/chat/completions")
async def proxy_chat(request: Request):
    body = await request.json()
    token = await get_token()
    print(token)

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version=2024-02-01",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json=body,
        )

    return response.json()

@app.get("/")
async def root():
    return {"message": "open-webui-proxy is ready to serve!"}
