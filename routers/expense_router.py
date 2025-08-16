from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import Base, engine
from models import Expense
from schemas import ExpenseCreate, ExpenseOut, ExpenseListResponse, TotalsPerCategory
from auth_utils import get_db, get_current_user
from crud import create_expense, list_expenses, totals_per_category
from typing import List
from fastapi.responses import JSONResponse

Base.metadata.create_all(bind=engine)
router = APIRouter()

@router.post("/", response_model=ExpenseOut)
def add_expense(body: ExpenseCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    exp = create_expense(db, user_id=user.id, amount=body.amount, category=body.category, date=body.date, note=body.note)
    return exp

@router.get("/", response_model=ExpenseListResponse)
def get_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user=Depends(get_current_user)):
    total, items = list_expenses(db, user_id=user.id, skip=skip, limit=limit)
    return {"total": total, "items": items}

@router.get("/totals", response_model=TotalsPerCategory)
def get_totals(db: Session = Depends(get_db), user=Depends(get_current_user)):
    totals = totals_per_category(db, user_id=user.id)
    return {"totals": totals}

@router.get("/export")
def export_json(db: Session = Depends(get_db), user=Depends(get_current_user)):
    total, items = list_expenses(db, user_id=user.id, skip=0, limit=100000)
    data = [
        {"id": e.id, "amount": e.amount, "category": e.category, "date": e.date.isoformat(), "note": e.note}
        for e in items
    ]
    return JSONResponse(content={"user": {"id": user.id, "name": user.name, "email": user.email}, "expenses": data})
