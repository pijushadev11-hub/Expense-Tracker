from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, transactions, test_auth
from .database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(test_auth.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Expense Tracker API"}