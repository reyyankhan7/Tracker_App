from fastapi import FastAPI
from routers.auth_router import router as auth_router
from routers.expense_router import router as expense_router

app = FastAPI(title="Expense Tracker", version="0.1.0")
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(expense_router, prefix="/expenses", tags=["Expenses"])
