from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models.models import Employee, Payroll
from schemas.schemas import PayrollCreate, PayrollOut
from datetime import date
from sqlalchemy import extract, func
from datetime import date, datetime, timedelta
from decimal import Decimal
from models.models import SalaryStructure, Payroll, Tax, SalaryAdvance, Leaves
from schemas.schemas import SalaryStructureCreate, SalaryStructureOut, PayrollOut , LeavesCreate, LeavesOut
from datetime import datetime
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from  models.models import Performance
router = APIRouter(prefix="/payroll", tags=["Payroll"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PayrollOut)
def create_payroll(p: PayrollCreate, db: Session = Depends(get_db)):
    new_payroll = Payroll(**p.dict())
    db.add(new_payroll)
    db.commit()
    db.refresh(new_payroll)
    return new_payroll

@router.get("/getpayroll/{employeeid}", response_model=PayrollOut)
def get_payroll(employeeid: int, db: Session = Depends(get_db)):
    p = db.query(Payroll).filter(Payroll.employeeid == employeeid).order_by(Payroll.monthyear.desc()).first()
    if not p:
        raise HTTPException(status_code=404, detail="Payroll not found")
    return p

@router.post("/process_payroll", response_model=PayrollOut)
def process_payroll(
    employee_id: int = Query(..., description="Employee ID"),
    month_year: date = Query(..., description="Payroll month as the first day of the month"),
    db: Session = Depends(get_db)
):
    # 1. Retrieve the latest salary structure for the employee
    salary_struct = (
        db.query(SalaryStructure)
        .filter(SalaryStructure.employeeid == employee_id)
        .order_by(SalaryStructure.effectivedate.desc())
        .first()
    )
    if not salary_struct:
        raise HTTPException(status_code=404, detail="Salary structure not found for employee")

    # Calculate total salary (BasicPay + HRA + OtherAllowances)
    total_salary = Decimal(salary_struct.basicpay or 0) + Decimal(salary_struct.hra or 0) + Decimal(salary_struct.otherallowances or 0)
    basic = salary_struct.basicpay
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    previous_month = first_day_of_current_month - timedelta(days=1)
    prev_month_num = previous_month.month
    prev_month_year = previous_month.year
    # 2. Retrieve tax deductions for the given month
    tax_record = (
        db.query(Tax)
        .filter(Tax.employeeid == employee_id, Tax.taxmonth == prev_month_num)
        .first()
    )
    if tax_record:
        tax_deductions = Decimal(tax_record.taxamount or 0) \
            + Decimal(tax_record.professionaltaxdeduction or 0) \
            + Decimal(tax_record.providentfunddeduction or 0)
    else:
        tax_deductions = Decimal(0)

    # 3. Retrieve advance deductions from approved & unpaid salary advances
    

    advances = (
    db.query(SalaryAdvance)
    .filter(
        SalaryAdvance.employeeid == employee_id,
        SalaryAdvance.status == 'Approved',
        SalaryAdvance.paid == 'UNPAID'
    )
    .all()
    )

    advance_deductions = Decimal(0)
    current_date = datetime.now().date()  # Convert current datetime to date

    for adv in advances:
        advance_start_date = adv.monthyear  # Assuming this is a datetime.date object
        repayment_end_date = advance_start_date + relativedelta(months=adv.repaymentmonths)

        # Check if current date is within repayment period (inclusive of start and end months)
        if advance_start_date <= current_date <= repayment_end_date:
            monthly_deduction = Decimal(adv.advanceamount) / Decimal(adv.repaymentmonths)
            advance_deductions += monthly_deduction

    # 4. Retrieve unpaid leaves for the previous month
    
    print("\n\n",prev_month_num)
    leaves = (
        db.query(Leaves)
        .filter(Leaves.employeeid == employee_id)
        .filter(func.year(Leaves.effectivedate) == prev_month_year)
        .filter(func.month(Leaves.effectivedate) == prev_month_num)
        .first()
    )
    print("\n\n hiiiii",prev_month_num,prev_month_year)
    leave_deductions = Decimal(0)
    if leaves:
        leave_deductions = Decimal(basic / 30) * Decimal(leaves.unpaidleaves)
    
    # 5. Calculate total deductions
    print("\n\n",advance_deductions,tax_deductions,leave_deductions,"\n\n")
    total_deductions = tax_deductions + advance_deductions + leave_deductions

    # 6. Insert the payroll record (netpayable is computed by the database)
    new_payroll = Payroll(
        employeeid=employee_id,
        monthyear=month_year,
        paymentstatus='Pending',
        paymentdate=None,
        totaldeductions=total_deductions,
        totalpayable=total_salary
    )
    db.add(new_payroll)
    db.commit()
    db.refresh(new_payroll)

    return new_payroll

@router.post("/process_payroll_all")
def process_payroll_all(
    month_year: datetime = Query(..., description="Payroll month as the first day of the month"),
    db: Session = Depends(get_db)
    ):
    employees = db.query(Employee).all()  # Get all employees
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found.")

    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    previous_month = first_day_of_current_month - timedelta(days=1)
    prev_month_num = previous_month.month
    prev_month_year = previous_month.year

    payroll_records = []

    for employee in employees:
        salary_struct = (
            db.query(SalaryStructure)
            .filter(SalaryStructure.employeeid == employee.employeeid)
            .order_by(SalaryStructure.effectivedate.desc())
            .first()
        )

        if not salary_struct:
            print(f"Skipping payroll for Employee {employee.employeeid}: No salary structure found.")
            continue  # Skip processing if no salary structure

        total_salary = Decimal(salary_struct.basicpay or 0) + Decimal(salary_struct.hra or 0) + Decimal(salary_struct.otherallowances or 0)
        basic = salary_struct.basicpay

        # Retrieve tax deductions
        tax_record = (
            db.query(Tax)
            .filter(Tax.employeeid == employee.employeeid, Tax.taxmonth == prev_month_num)
            .first()
        )
        tax_deductions = (
            Decimal(tax_record.taxamount or 0) +
            Decimal(tax_record.professionaltaxdeduction or 0) +
            Decimal(tax_record.providentfunddeduction or 0)
        ) if tax_record else Decimal(0)

        # Retrieve salary advances
        advances = (
            db.query(SalaryAdvance)
            .filter(SalaryAdvance.employeeid == employee.employeeid, SalaryAdvance.status == 'Approved', SalaryAdvance.paid == 'UNPAID')
            .all()
        )
        advance_deductions = sum(Decimal(adv.advanceamount) / Decimal(adv.repaymentmonths) for adv in advances)

        performances=(
            db.query(Performance)
            .filter(Performance.employeeid==employee.employeeid,Performance.rating >=5).first()
        )
        if(performances):
            bonus=basic * Decimal('0.5')
        else:
            bonus=0
        # Retrieve unpaid leaves
        leaves = (
            db.query(Leaves)
            .filter(Leaves.employeeid == employee.employeeid)
            .filter(extract('year', Leaves.effectivedate) == str(prev_month_year))
            .filter(extract('month', Leaves.effectivedate) == str(prev_month_num))
            .first()
        )
        print("\n\n calcs:",prev_month_num,prev_month_year,"\n\n")
        print("basic:",basic)
        leave_deductions = (Decimal(basic / 30) * Decimal(leaves.unpaidleaves)) if leaves else Decimal(0)
        print("\n\n",leave_deductions,tax_deductions,advance_deductions,"\n\n")
        total_deductions = tax_deductions + advance_deductions + leave_deductions

        new_payroll = Payroll(
            employeeid=employee.employeeid,
            monthyear=month_year,
            paymentstatus='Pending',
            paymentdate=None,
            totaldeductions=total_deductions,
            totalpayable=total_salary+bonus
        )
        db.add(new_payroll)
        payroll_records.append(new_payroll)

    db.commit()

    return {"message": f"Payroll processed for {len(payroll_records)} employees", "payroll_records": payroll_records}