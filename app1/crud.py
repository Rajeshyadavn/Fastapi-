from sqlalchemy.orm import Session
from app1 import models, schemas
from app1.models import Customer
from app1.schemas import CustomerCreate
from datetime import datetime
from typing import List

async def create_data(db: Session, data: schemas.WebhookPayload):
    db_data = models.Data(source=data.source, content=data.content)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

async def get_data(db: Session, offset: int = 0, limit: int = 10):
    return db.query(models.Data).offset(offset).limit(limit).all()

async def create_customer(db: Session, customer: CustomerCreate):
    db_customer = Customer(
        id=customer.id,
        name=customer.name,
        email=customer.email,
        created_at=datetime()
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

async def get_customers(db: Session, offset: int = 0, limit: int = 10) -> List[Customer]:
    return db.query(Customer).offset(offset).limit(limit).all()
