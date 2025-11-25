from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.models import Employee, Performance
from schemas.schemas import EmployeeCreate, EmployeeOut, PerformanceCreate, PerformanceOut

router = APIRouter(prefix="/employees", tags=["Employees"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EmployeeOut)
def create_employee(emp: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(**emp.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.get("/details/{employeeID}", response_model=EmployeeOut)
def get_employee(employeeID: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.employeeid == employeeID).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp
@router.post("/performance", response_model=PerformanceOut)
def create_monthly_performance(
    employeeid: int,
    performance: PerformanceCreate,
    db: Session = Depends(get_db)
):
    """Enter rating for an employee for a specific month and year."""
    
    reviewdate = performance.to_reviewdate()  # Convert year & month to reviewdate
    
    existing_review = (
        db.query(Performance)
        .filter(Performance.employeeid == employeeid)
        .filter(Performance.reviewdate == reviewdate)
        .first()
    )

    if existing_review:
        raise HTTPException(status_code=400, detail="Performance review for this month already exists.")

    new_performance = Performance(
        employeeid=employeeid,
        reviewdate=reviewdate,
        rating=performance.rating,
        comments=performance.comments
    )

    db.add(new_performance)
    db.commit()
    db.refresh(new_performance)

    return new_performance