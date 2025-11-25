from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import employee
from routers import payroll
from routers import salarystructure
from routers import salaryadvance
from routers import routes
from routers import leaves
from routers import users
app = FastAPI()
app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],  # Allow all domains

    allow_credentials=True,

    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)

    allow_headers=["*"],  # Allow all headers

)
# Create tables
Base.metadata.create_all(bind=engine)

# Include Routers
app.include_router(employee.router, prefix="/api")
app.include_router(payroll.router, prefix="/api")
app.include_router(salarystructure.router, prefix="/api")
app.include_router(salaryadvance.router,prefix="/api")
app.include_router(routes.router,prefix="/api")
app.include_router(leaves.router,prefix="/api")
app.include_router(users.router,prefix="/api")
@app.get("/")
def home():
    return {"message": "Payroll Management System API"}
