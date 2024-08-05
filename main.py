from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app1 import crud, models, schemas, tasks, database
from app1.utils import get_api_key, rate_limiter
from typing import List
from app1.database import connect_to_db, get_db
import asyncio
from contextlib import asynccontextmanager
from app1.tasks import sync_crm_data


app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect_to_db()
    yield
    # Shutdown
    await database.disconnect_from_db()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook", response_model=schemas.WebhookResponse)
async def handle_webhook(payload: schemas.WebhookPayload, db: Session = Depends(database.get_db)):
    data = await crud.create_data(db=db, data=payload)
    return {"message": "Webhook data stored successfully"}

@app.get("/data", response_model=List[schemas.Customer])
async def get_data(offset: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    data = await crud.get_data(db=db, offset=offset, limit=limit)
    return data

@app.get("/sync/crm")
async def sync_crm(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(sync_crm_data, db)
    return {"message": "CRM data synchronization started"}
@app.get("/tasks")
async def list_tasks():
    tasks = tasks.get_tasks()
    return tasks

@app.post("/tasks/cancel")
async def cancel_task(task_id: str):
    result = await tasks.cancel_task(task_id)
    if result:
        return {"message": "Task cancelled successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.middleware("http")
async def add_api_key_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-API-Key"] = get_api_key()
    return response

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    await rate_limiter(request)
    response = await call_next(request)
    return response
 

