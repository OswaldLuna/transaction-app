from pydantic import BaseModel

class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    type: str

class TransactionOut(BaseModel):
    id: int
    user_id: int
    amount: float
    type: str
    status: str

    class Config:
        orm_mode = True

class AsyncProcessRequest(BaseModel):
    transaction_id: int

class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str

    class Config:
        orm_mode = True
