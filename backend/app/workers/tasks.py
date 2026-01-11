import time
import json
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Transaction
from app.workers.redis_conn import redis_client

def process_transaction(transaction_id: int):
    db:Session = SessionLocal()

    try:
        tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        
        if not tx:
            print(f"Transacción {transaction_id} no encontrada")
            return
        
        # Validación defensiva: solo procesar si está pendiente o fallido
        if tx.status not in ["pendiente", "fallido"]:
            print(f"Transacción {transaction_id} ya está en estado '{tx.status}', no se procesará")
            return
        
        #Update status to "pendiente"
        tx.status = "pendiente"
        db.commit()

        redis_client.publish("transactions", json.dumps({
            "id": tx.id,
            "status": "pendiente"
        }))

        # Simulate heavy process
        time.sleep(5)

        tx.status = "procesado"
        db.commit()

        redis_client.publish("transactions", json.dumps({
            "id": tx.id,
            "status": "procesado"
        }))

        print(f"Transacción {tx.id} procesada con éxito")

    except Exception as e:
        print("Error:", e)
        tx.status = "fallido"
        db.commit()

        redis_client.publish("transactions", json.dumps({
            "id": tx.id,
            "status": "fallido"
        }))

    finally:
        db.close()