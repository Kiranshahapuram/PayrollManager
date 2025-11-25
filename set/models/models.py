from sqlalchemy import Column, Computed, Integer, Numeric, String, Date, Enum, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Employees Table
class Employee(Base):
    __tablename__ = "employees"

    employeeid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(Enum('Male', 'Female', 'Other', name="gender_enum"), nullable=False)
    address = Column(String)
    phone = Column(String(15))
    email = Column(String(100), unique=True)
    ifsc = Column(String(11), unique=True)
    bankaccountnumber = Column(String(18), unique=True)
    hiredate = Column(Date, nullable=False)

# EmployeeHistory Table
class EmployeeHistory(Base):
    __tablename__ = "employeehistory"

    employeeid = Column(Integer, ForeignKey("employees.employeeid"), primary_key=True)
    designationname = Column(String(100), nullable=False, unique=True)
    effectivedate = Column(Date, primary_key=True)
    salary = Column(DECIMAL(10,2))

# Users Table
class User(Base):
    __tablename__ = "users"

    employeeid = Column(Integer, primary_key=True)
    passwordhash = Column(String(255), nullable=False)
    role = Column(Enum('Admin', 'HR', 'Employee', name="role_enum"), nullable=False)
    

# SalaryStructure Table
class SalaryStructure(Base):
    __tablename__ = "salarystructure"

    employeeid = Column(Integer, ForeignKey("employees.employeeid"), primary_key=True)
    effectivedate = Column(Date, primary_key=True)
    basicpay = Column(DECIMAL(10,2), nullable=False)
    hra = Column(DECIMAL(10,2))
    otherallowances = Column(DECIMAL(10,2))
    totalsalary = Column(DECIMAL(10,2), Computed("basicpay + hra + otherallowances", persisted=True))

# Tax Table
class Tax(Base):
    __tablename__ = "tax"

    employeeid = Column(Integer, ForeignKey("employees.employeeid"), primary_key=True)
    taxmonth = Column(Integer, primary_key=True)
    taxamount = Column(DECIMAL(10,2), nullable=False)
    professionaltaxdeduction = Column(DECIMAL(10,2))
    providentfunddeduction = Column(DECIMAL(10,2), nullable=False)

# SalaryAdvance Table
class SalaryAdvance(Base):
    __tablename__ = "salaryadvance"

    employeeid = Column(Integer, ForeignKey("employees.employeeid"), primary_key=True)
    monthyear = Column(Date, primary_key=True)
    advanceamount = Column(DECIMAL(10,2), nullable=False)
    repaymentmonths = Column(Integer, nullable=False)
    status = Column(Enum('Pending', 'Approved', 'Rejected', name="status_enum"), default='Pending')
    paid = Column(Enum('PAID', 'UNPAID', name="paid_enum"))

# Performance Table
class Performance(Base):
    __tablename__ = "performance"

    performanceid = Column(Integer, primary_key=True, autoincrement=True)
    employeeid = Column(Integer, ForeignKey("employees.employeeid"), nullable=False)
    reviewdate = Column(Date, nullable=False)
    rating = Column(Integer, nullable=False)
    comments = Column(String)

# Payroll Table
class Payroll(Base):
    __tablename__ = "payroll"

    employeeid = Column(Integer, ForeignKey("employees.employeeid"), primary_key=True)
    monthyear = Column(Date, primary_key=True)
    paymentstatus = Column(Enum('Pending', 'Paid', name="paymentstatus_enum"), default='Pending')
    paymentdate = Column(Date)
    totaldeductions = Column(DECIMAL(10,2), nullable=False)
    totalpayable = Column(DECIMAL(10,2), nullable=False)
    netpayable = Column(DECIMAL(10,2), Computed("totalpayable - totaldeductions", persisted=True))

# Leaves Table
class Leaves(Base):
    __tablename__ = "leaves"

    employeeid = Column(Integer, ForeignKey("employees.employeeid"), primary_key=True)
    effectivedate = Column(Date, primary_key=True)
    unpaidleaves = Column(Integer, nullable=False)
