from pydantic import BaseModel, Field, field_validator, validator
from typing import Optional
from datetime import date


# Employee Schema
class EmployeeBase(BaseModel):
    firstname: str
    lastname: str
    dob: date
    gender: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    ifsc: Optional[str] = None
    bankaccountnumber: Optional[str] = None
    hiredate: date


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeOut(EmployeeBase):
    employeeid: int

    class Config:
        from_attributes = True


# Employee History Schema
class EmployeeHistoryBase(BaseModel):
    designationname: str
    effectivedate: date
    salary: Optional[float] = None


class EmployeeHistoryCreate(EmployeeHistoryBase):
    pass


class EmployeeHistoryOut(EmployeeHistoryBase):
    employeeid: int

    class Config:
        from_attributes = True


# User Schema
class UserBase(BaseModel):
    username: str
    role: str
    employeeid: Optional[int] = None


class UserCreate(UserBase):
    passwordhash: str


class UserOut(UserBase):
    userid: int

    class Config:
        from_attributes = True


# Salary Structure Schema
class SalaryStructureBase(BaseModel):
    employeeid : int
    effectivedate: date
    basicpay: float
    hra: Optional[float] = None
    otherallowances: Optional[float] = None


class SalaryStructureCreate(SalaryStructureBase):
    pass


class SalaryStructureOut(SalaryStructureBase):
    employeeid: int
    totalsalary: Optional[float] = None

    class Config:
        from_attributes = True


# Tax Schema
class TaxBase(BaseModel):
    taxmonth: int
    taxamount: float
    professionaltaxdeduction: Optional[float] = None
    providentfunddeduction: float


class TaxCreate(TaxBase):
    pass


class TaxOut(TaxBase):
    employeeid: int

    class Config:
        from_attributes = True


# Salary Advance Schema
class SalaryAdvanceBase(BaseModel):
    employeeid: int
    monthyear: str  # Ensure it's a string
    advanceamount: float
    repaymentmonths: int
    status: str = "Pending"
    paid: Optional[str] = None

class SalaryAdvanceCreate(SalaryAdvanceBase):
    pass

class SalaryAdvanceOut(SalaryAdvanceBase):
    employeeid: int

    # Convert monthyear to string before returning response
    @field_validator("monthyear", mode="before")
    def convert_monthyear(cls, v):
        if isinstance(v, date):  # Convert datetime.date to string
            return v.strftime("%Y-%m")
        return v  # Already a string

    class Config:
        from_attributes = True


class PerformanceBase(BaseModel):
    year: int = Field(..., ge=1900, le=2100)  # Ensure valid year
    month: int = Field(..., ge=1, le=12)  # Ensure valid month
    rating: int
    comments: Optional[str] = None

    def to_reviewdate(self) -> date:
        """Convert year and month to a valid reviewdate (1st of the month)."""
        return date(self.year, self.month, 1)

class PerformanceCreate(PerformanceBase):
    pass

class PerformanceOut(BaseModel):
    performanceid: int
    employeeid: int
    reviewdate: date  # Will store the 1st day of the month
    rating: int
    comments: Optional[str] = None

    class Config:
        from_attributes = True

# Payroll Schema
class PayrollBase(BaseModel):
    monthyear: date
    paymentstatus: str = "Pending"
    paymentdate: Optional[date] = None
    totaldeductions: float
    totalpayable: float


class PayrollCreate(PayrollBase):
    pass


class PayrollOut(PayrollBase):
    employeeid: int
    netpayable: Optional[float] = None

    class Config:
        from_attributes = True



class LeavesBase(BaseModel):
    employeeid: int
    effectivedate: str  # MMYYYY format
    unpaidleaves: int  

    @validator("effectivedate")
    def validate_effectivedate(cls, value):
        """Convert MMYYYY to YYYY-MM-01 format"""
        if len(value) != 6 or not value.isdigit():
            raise ValueError("effectivedate must be in MMYYYY format")
        month = int(value[:2])
        year = int(value[2:])
        if month < 1 or month > 12:
            raise ValueError("Invalid month in effectivedate")
        return date(year, month, 1)  # Store as YYYY-MM-01

class LeavesCreate(LeavesBase):
    pass

class LeavesOut(BaseModel):
    employeeid: int
    effectivedate: date  # Will store as YYYY-MM-01 in DB
    unpaidleaves: int

    class Config:
        from_attributes = True  # Enable ORM conversion