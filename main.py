from fastapi import FastAPI
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks
from database import engine, SessionLocal, Base
from models import Transaction
from schemas import TransactionCreate
from starlette import status
import time

app=FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def process_transaction(transaction_id:str):
    db=SessionLocal()
    try:
        time.sleep(30)

        txn=db.query(Transaction).filter(Transaction.transaction_id==transaction_id).first()
        if not txn:
            raise HTTPException(status_code=404, detail="Transaction not found")
            return
        
        txn.status="PROCESSED"
        txn.processed_at=datetime.utcnow()
        db.commit()  
    except Exception as e:
        print(f"Error processing transaction {transaction_id}: {e}")
    finally:
        db.close()


@app.get("/")
def health():
    return {
        "status": "HEALTHY",
        "current_time": datetime.now().isoformat()
    }

@app.get("/debug/transactions")
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()

@app.get("/v1/transactions/{transaction_id}")
def get_transaction(transaction_id:str, db:Session = Depends(get_db)):
    txn=db.query(Transaction).filter(Transaction.transaction_id==transaction_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return [
        {
        "transaction_id":txn.transaction_id,
        "source_account":txn.source_account,
        "destination_account":txn.destination_account,
        "amount":txn.amount,
        "currency":txn.currency,
        "status":txn.status,
        "created_at":txn.created_at,
        "processed_at":txn.processed_at
        }
    ]



@app.post("/v1/webhooks/transactions")
def create_transaction(transaction:TransactionCreate,background_tasks:BackgroundTasks, db:Session = Depends(get_db)):
    print(transaction)
    exists = db.query(Transaction).filter(Transaction.transaction_id==transaction.transaction_id).first()
    
    if exists:
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Already processed"})
 
    if not exists:
        new_data = Transaction(
            transaction_id=transaction.transaction_id,
            source_account=transaction.source_account,
            destination_account=transaction.destination_account,
            amount=transaction.amount,
            currency=transaction.currency,
            status="PROCESSING"
        )
        db.add(new_data)
        db.commit()

        background_tasks.add_task(process_transaction, transaction.transaction_id)

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Accepted"})
