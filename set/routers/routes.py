from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from models.models import Employee, EmployeeHistory, User, SalaryStructure, Tax, SalaryAdvance, Performance, Payroll, Leaves
from schemas.schemas import EmployeeCreate, EmployeeOut, EmployeeHistoryCreate, UserCreate, SalaryStructureCreate, TaxCreate, SalaryAdvanceCreate, PerformanceCreate, PayrollCreate, LeavesCreate

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Employee Routes
@router.post("/employees/", response_model=EmployeeOut)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/employees/{employeeid}", response_model=EmployeeOut)
def get_employee(employeeid: int, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.employeeid == employeeid).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

# Employee History Routes
@router.post("/employeehistory/", response_model=EmployeeHistoryCreate)
def create_employee_history(history: EmployeeHistoryCreate, db: Session = Depends(get_db)):
    db_history = EmployeeHistory(**history.dict())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

# Users Routes
@router.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Salary Structure Routes
@router.post("/salarystructure/", response_model=SalaryStructureCreate)
def create_salary_structure(salary_structure: SalaryStructureCreate, db: Session = Depends(get_db)):
    db_salary_structure = SalaryStructure(**salary_structure.dict())
    db.add(db_salary_structure)
    db.commit()
    db.refresh(db_salary_structure)
    return db_salary_structure

# Tax Routes
@router.post("/tax/", response_model=TaxCreate)
def create_tax(tax: TaxCreate, db: Session = Depends(get_db)):
    db_tax = Tax(**tax.dict())
    db.add(db_tax)
    db.commit()
    db.refresh(db_tax)
    return db_tax

# Salary Advance Routes
@router.post("/salaryadvance/", response_model=SalaryAdvanceCreate)
def create_salary_advance(advance: SalaryAdvanceCreate, db: Session = Depends(get_db)):
    db_advance = SalaryAdvance(**advance.dict())
    db.add(db_advance)
    db.commit()
    db.refresh(db_advance)
    return db_advance

# Performance Routes
@router.post("/performance/", response_model=PerformanceCreate)
def create_performance(performance: PerformanceCreate, db: Session = Depends(get_db)):
    db_performance = Performance(**performance.dict())
    db.add(db_performance)
    db.commit()
    db.refresh(db_performance)
    return db_performance

# Payroll Routes
@router.post("/payroll/", response_model=PayrollCreate)
def create_payroll(payroll: PayrollCreate, db: Session = Depends(get_db)):
    db_payroll = Payroll(**payroll.dict())
    db.add(db_payroll)
    db.commit()
    db.refresh(db_payroll)
    return db_payroll

# Leaves Routes
@router.post("/leaves/", response_model=LeavesCreate)
def create_leave(leave: LeavesCreate, db: Session = Depends(get_db)):
    db_leave = Leaves(**leave.dict())
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave
