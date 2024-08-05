import asyncio
from typing import List
from sqlalchemy.orm import Session
from app1.utils import fetch_external_data
from app1.crud import create_data
from app1.models import Customer
from concurrent.futures import ThreadPoolExecutor
import uuid
from app1 import crud, schemas
from app1.external_api import fetch_customers

tasks = {}

async def sync_data(source: str, db: Session):
    task_id = f"{source}-{str(uuid.uuid4())}"
    tasks[task_id] = {"status": "running"}



    try:
        if source == "crm":
            data = await fetch_external_data("https://challenge.berrydev.ai/api/crm/customers")
        elif source == "marketing":
            data = await fetch_external_data("https://challenge.berrydev.ai/api/marketing/campaigns")

        for item in data:
            await create_data(db=db, data=item)
        tasks[task_id]["status"] = "completed"
    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)
    
    await asyncio.sleep(1)  # Simulate delay
async def sync_crm_data(db: Session):
    offset = 0
    limit = 10

    while True:
        customers = await fetch_customers(offset=offset, limit=limit)
        if not customers:
            break
        for customer_data in customers:
            customer = schemas.CustomerCreate(**customer_data)
            crud.create_customer(db=db, customer=customer)
        offset += limit

def get_tasks():
    return tasks

async def cancel_task(task_id: str):
    task = tasks.get(task_id)
    if task:
        task["status"] = "cancelled"
        return True
    return False
