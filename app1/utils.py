import httpx
from fastapi import HTTPException, Request
from functools import wraps
import time
import os

API_KEY = os.getenv("GITHUB_USERNAME", "default_api_key")

async def fetch_external_data(url: str):
    headers = {"X-API-Key": API_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")

def get_api_key():
    return API_KEY

async def rate_limiter(request: Request):
    # Implement a simple rate limiter
    time.sleep(1)  # Simulate rate limiting
