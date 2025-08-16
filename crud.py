from typing import Dict, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import User, Expense
from auth_utils import hash_password, verify_password

def create_user(db: Session, name: str, email: str, password: str) -> User:
    user = User(name=name, email=email, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_expense(db: Session, user_id: int, amount: float, category: str, date, note: str = None) -> Expense:
    exp = Expense(user_id=user_id, amount=amount, category=category, date=date, note=note)
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

def list_expenses(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> Tuple[int, List[Expense]]:
    q = db.query(Expense).filter(Expense.user_id == user_id).order_by(Expense.date.desc(), Expense.id.desc())
    total = q.count()
    items = q.offset(skip).limit(limit).all()
    return total, items

def totals_per_category(db: Session, user_id: int) -> Dict[str, float]:
    rows = (
        db.query(Expense.category, func.coalesce(func.sum(Expense.amount), 0.0))
        .filter(Expense.user_id == user_id)
        .group_by(Expense.category)
        .all()
    )
    return {cat: float(total) for cat, total in rows}
