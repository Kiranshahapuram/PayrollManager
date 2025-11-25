from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import extract
from sqlalchemy.orm import Session
from database import SessionLocal
from models.models import SalaryAdvance
from schemas.schemas import SalaryAdvanceCreate, SalaryAdvanceOut
from sqlalchemy.sql import exists
from datetime import datetime

router = APIRouter(
    prefix="/salaryadvance",
    tags=["Salary Advance"]
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/request", response_model=SalaryAdvanceOut)
def request_salary_advance(request: SalaryAdvanceCreate, db: Session = Depends(get_db)):
    """
    Request a salary advance.  
    The request will be in 'Pending' status by default.
    An employee can only request a new advance if all previous advances are fully paid.
    """
    try:
        formatted_monthyear = datetime.strptime(request.monthyear, "%Y-%m").date().replace(day=1)  # Convert to YYYY-MM-01
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM.")

    # Check for existing unpaid salary advances
    unpaid_advance = db.query(SalaryAdvance).filter(
        SalaryAdvance.employeeid == request.employeeid,
        SalaryAdvance.paid != True  # Not fully paid
    ).first()

    if unpaid_advance:
        raise HTTPException(
            status_code=400, 
            detail="Cannot request new salary advance until previous advance is fully paid."
        )

    # Check if a salary advance already exists for the given month
    existing_advance = db.query(SalaryAdvance).filter(
        SalaryAdvance.employeeid == request.employeeid,
        SalaryAdvance.monthyear == formatted_monthyear
    ).first()

    if existing_advance:
        raise HTTPException(status_code=400, detail="Salary advance already requested for this month.")

    # Create new salary advance request
    new_advance = SalaryAdvance(
        employeeid=request.employeeid,
        monthyear=formatted_monthyear,
        advanceamount=request.advanceamount,
        repaymentmonths=request.repaymentmonths,
        status="Pending",
        paid=None
    )

    db.add(new_advance)
    db.commit()
    db.refresh(new_advance)

    return new_advance


from datetime import datetime

@router.put("/approve/{employeeid}/{monthyear}")
def approve_salary_advance(employeeid: int, monthyear: str, db: Session = Depends(get_db)):
    try:
        formatted_date = datetime.strptime(monthyear, "%Y-%m").date().replace(day=1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM.")

    salary_advance = db.query(SalaryAdvance).filter(
        SalaryAdvance.employeeid == employeeid,
        SalaryAdvance.monthyear == formatted_date
    ).first()

    if not salary_advance:
        raise HTTPException(status_code=404, detail="Salary advance record not found")

    if salary_advance.status != "Pending":
        raise HTTPException(status_code=400, detail="Only pending requests can be approved")

    salary_advance.status = "Approved"
    salary_advance.paid="Unpaid"
    db.commit()
    db.refresh(salary_advance)

    return {"message": "Salary advance approved successfully", "salary_advance": salary_advance}


@router.put("/reject/{employeeid}/{monthyear}")
def reject_salary_advance(employeeid: int, monthyear: str, db: Session = Depends(get_db)):
    try:
        formatted_date = datetime.strptime(monthyear, "%Y-%m").date().replace(day=1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM.")

    salary_advance = db.query(SalaryAdvance).filter(
        SalaryAdvance.employeeid == employeeid,
        SalaryAdvance.monthyear == formatted_date
    ).first()

    if not salary_advance:
        raise HTTPException(status_code=404, detail="Salary advance record not found")

    if salary_advance.status != "Pending":
        raise HTTPException(status_code=400, detail="Only pending requests can be rejected")

    salary_advance.status = "Rejected"
    db.commit()
    db.refresh(salary_advance)

    return {"message": "Salary advance rejected successfully", "salary_advance": salary_advance}



@router.get("/{monthyear}", response_model=list[SalaryAdvanceOut])
def get_salary_advances_for_month(monthyear: str, db: Session = Depends(get_db)):
    """
    Retrieve all salary advance records for a specific month and year (in format YYYYMM).
    """
    # Extract year and month from the 'monthyear' string
    year = int(monthyear[:4])  # First 4 characters represent the year
    month = int(monthyear[4:6])  # Last 2 characters represent the month

    return db.query(SalaryAdvance).filter(
        extract('year', SalaryAdvance.monthyear) == year,
        extract('month', SalaryAdvance.monthyear) == month,
        SalaryAdvance.status == "pending"
    ).all()