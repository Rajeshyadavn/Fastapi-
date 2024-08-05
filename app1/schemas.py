from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class WebhookPayload(BaseModel):
    source: str
    content: str

class WebhookResponse(BaseModel):
    message: str
class CustomerBase(BaseModel):
    name: str
    email: str
class CustomerCreate(CustomerBase):
    pass

class Customer(BaseModel):  
    id: int    
    created_at: datetime

    

    class Config:
        orm_mode = True
