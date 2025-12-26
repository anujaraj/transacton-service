from pydantic import BaseModel

class TransactionCreate(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: float
    currency: str
