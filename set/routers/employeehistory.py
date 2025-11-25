from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models.models import EmployeeHistory
from schemas.schemas import EmployeeHistoryBase,EmployeeHistoryCreate

router = APIRouter(prefix="/employeehistory", tags=["EmployeeHistory"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Employee History Routes
@router.post("/employeehistory/", response_model=EmployeeHistoryCreate)
def create_employee_history(history: EmployeeHistoryCreate, db: Session = Depends(get_db)):
    db_history = EmployeeHistory(**history.dict())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history
