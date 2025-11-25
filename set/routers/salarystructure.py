from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal
from models.models import SalaryStructure, Payroll, Tax, SalaryAdvance
from schemas.schemas import SalaryStructureCreate, SalaryStructureOut, PayrollOut 
from database import SessionLocal
from sqlalchemy import extract, func

router = APIRouter(prefix="/salarystructure", tags=["Salary Structure"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Salary Structure Endpoints ----------------
# Create a salary structure entry
@router.post("/", response_model=SalaryStructureOut)
def create_salary_structure(payload: SalaryStructureCreate, db: Session = Depends(get_db)):
    db_salary = SalaryStructure(**payload.dict())
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    return db_salary


# Get all salary structures
@router.get("/", response_model=list[SalaryStructureOut])
def get_salary_structures(db: Session = Depends(get_db)):
    return db.query(SalaryStructure).all()


# Get salary structure by Employee ID and Effective Date
@router.get("/salary/structure/{employeeid}/{effectivedate}", response_model=SalaryStructureOut)
def get_salary_structure(employeeid: int, effectivedate: str, db: Session = Depends(get_db)):
    salary = db.query(SalaryStructure).filter(
        SalaryStructure.employeeid == employeeid,
        func.month(SalaryStructure.effectivedate) == func.month(effectivedate)
    ).first()

    if not salary:
        raise HTTPException(status_code=404, detail="Salary structure not found")
    return salary


# Update salary structure
@router.put("/{employeeid}/{effectivedate}", response_model=SalaryStructureOut)
def update_salary_structure(employeeid: int, effectivedate: str, payload: SalaryStructureCreate, db: Session = Depends(get_db)):
    salary = db.query(SalaryStructure).filter(
        SalaryStructure.employeeid == employeeid,
        SalaryStructure.effectivedate == effectivedate
    ).first()

    if not salary:
        raise HTTPException(status_code=404, detail="Salary structure not found")

    for key, value in payload.dict().items():
        setattr(salary, key, value)

    db.commit()
    db.refresh(salary)
    return salary


