from fastapi import APIRouter, Depends, WebSocket, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas
import hashlib
from rq import Queue
from app.workers.tasks import process_transaction
from app.workers.redis_conn import redis_client
import asyncio


router = APIRouter()

@router.post("/create", response_model=schemas.TransactionOut)
def create_transaction(payload: schemas.TransactionCreate, db: Session = Depends(get_db)):
    hash_input = f"{payload.user_id}-{payload.amount}-{payload.type}"
    tx_hash = hashlib.sha256(hash_input.encode()).hexdigest()

    existing = db.query(models.Transaction).filter_by(hash=tx_hash).first()
    if existing:
        return existing
    
    tx= models.Transaction(
        user_id=payload.user_id,
        amount=payload.amount,
        type=payload.type,
        hash=tx_hash
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    return tx

queue = Queue('transq', connection=redis_client)

@router.post("/async-process")
def async_process(payload: schemas.AsyncProcessRequest):
    job = queue.enqueue(process_transaction, payload.transaction_id)
    return {"job_id": job.id, "transaction_id": payload.transaction_id}

@router.websocket("/stream")
async def transaction_stream(websocket: WebSocket):
    await websocket.accept()

    pubsub = redis_client.pubsub()
    pubsub.subscribe("transactions")

    try:
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)

            if message:
                data = message["data"]
                await websocket.send_text(data)

            await asyncio.sleep(0.01)

    except Exception as e:
        print("WebSocket desconectado:", e)

    finally:
        pubsub.close()