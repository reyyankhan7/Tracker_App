from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import date

class UserRegister(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenPayload(BaseModel):
    sub: str
    name: str
    exp: int

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    date: date
    note: Optional[str] = None

class ExpenseOut(BaseModel):
    id: int
    amount: float
    category: str
    date: date
    note: Optional[str] = None

    class Config:
        from_attributes = True

class ExpenseListResponse(BaseModel):
    total: int
    items: List[ExpenseOut]

class TotalsPerCategory(BaseModel):
    totals: Dict[str, float]
