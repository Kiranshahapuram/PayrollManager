from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.models import Employee
from schemas.schemas import EmployeeOut
from models.models import User
from schemas.schemas import UserOut
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

# Dummy password check (replace with hashed password check in real implementation)
class LoginRequest(BaseModel):
    employeeId: int
    password: str
    role: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    db_employee = db.query(User).filter(User.employeeid == request.employeeId).first()
    if not db_employee:
        print('here1')
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Replace this with real password verification
    print("\n",request.password,"\n")
    if request.password != db_employee.passwordhash:  
        print('here 2')
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if request.role.lower() !=db_employee.role.lower():
        raise HTTPException(status_code=401,detail="Invalid Credentials")

    return {"success": True, "role": request.role}
