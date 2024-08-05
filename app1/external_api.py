import httpx
from typing import List, Dict

BASE_URL = "https://challenge.berrydev.ai/api/crm/customers"
API_KEY = "your_github_username"  # Replace with your GitHub username

async def fetch_customers(offset: int = 0, limit: int = 10) -> List[Dict]:
    headers = {"X-API-Key": API_KEY}
    params = {"offset": offset, "limit": limit}
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get("customers", [])
