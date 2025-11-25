from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:1234@127.0.0.1:3306/payroll"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("✅ Database connected successfully!")
except Exception as e:
    print("❌ Database connection error:", e)

    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
