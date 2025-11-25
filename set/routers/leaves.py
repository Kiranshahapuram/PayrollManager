from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models.models import Leaves
from schemas.schemas import LeavesBase,LeavesCreate,LeavesOut

router = APIRouter(prefix="/leaves", tags=["Leaves"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/leaves/", response_model=LeavesOut)
def create_leave(leave: LeavesCreate, db: Session = Depends(get_db)):
    # leave.effectivedate is already a date object from schema validation
    effectivedate = leave.effectivedate

    # Check if leave entry already exists for the employee in the same month
    existing_leave = db.query(Leaves).filter(
        Leaves.employeeid == leave.employeeid,
        Leaves.effectivedate == effectivedate
    ).first()

    if existing_leave:
        raise HTTPException(status_code=400, detail="Leave entry for this month already exists")

    # Create new leave entry
    db_leave = Leaves(
        employeeid=leave.employeeid,
        effectivedate=effectivedate,
        unpaidleaves=leave.unpaidleaves
    )
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)

    return db_leave