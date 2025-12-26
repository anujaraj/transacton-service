# Transaction Processing Service

A backend service built with FastAPI that receives transaction webhooks, responds immediately, and processes transactions asynchronously with idempotency and persistent storage.
This service simulates real-world payment processor behavior (e.g., Razorpay webhooks) by acknowledging requests quickly and completing processing in the background.

---

## Tech Stack

- **Python 3.10+**
- **FastAPI** – Web framework
- **SQLAlchemy** – ORM
- **PostgreSQL** (Render-managed) – Persistent storage
- **Uvicorn** – ASGI server
- **Render** – Cloud deployment

---

## Features

- Immediate webhook acknowledgment (`202 Accepted`)
- Background transaction processing with 30-second delay
- Idempotent webhook handling (no duplicate processing)
- Persistent transaction state storage
- Transaction status query endpoint
- Health check endpoint

---

## Technical Design Decisions

- FastAPI BackgroundTasks are used to ensure webhook responses return immediately without blocking

---

## API endpoint

### Health Check: 
- GET \
- Response :  
```json
{
  "status": "HEALTHY",
  "current_time": "2024-01-15T10:30:00Z"
}
```

 
## Transaction Webhook: 
- POST /v1/webhooks/transactions
- Request body:
```json
{
  "transaction_id": "txn_abc123newid236",
  "source_account": "acc_user_789",
  "destination_account": "acc_merchant_456",
  "amount": 1600,
  "currency": "INR"

}
```

- Response:
  ```json
  202 Accepted
  ```

## Get Transaction Status
- GET /v1/transactions/{transaction_id}
- Response
  ```json
  {
    "transaction_id": "txn_abc123def456",
    "source_account": "acc_user_789",
    "destination_account": "acc_merchant_456",
    "amount": 1500,
    "currency": "INR",
    "status": "PROCESSED",
    "created_at": "2024-01-15T10:30:00Z",
    "processed_at": "2024-01-15T10:30:30Z"
  }
  ```

---

## Instructions to Run the Service

### 1. Clone the repository

git clone https://github.com/<your-username>/transaction-processing-service.git
cd transaction-processing-service

### 2. Create Virtual Environment

python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Create a .env file

DATABASE_URL=postgresql://user:password@localhost:5432/transactions_db

### 5. Run the application

uvicorn main:app --reload
The service will start at : http://127.0.0.1:8000

### 6 Testing 

Send a webhook request
Immediately query the transaction status
Status will initially be PROCESSING
After ~30 seconds, status changes to PROCESSED
Sending the same webhook again will not create a duplicate transaction

## Deployment
The service is deployed on Render using a GitHub-connected workflow.
Database credentials are configured via Render environment variables.

## Author
Built as part of a backend development assessment.



