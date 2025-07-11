from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create database engines for different modules
engine_a = create_engine(settings.DATABASE_URL_A)
engine_b = create_engine(settings.DATABASE_URL_B)

# Create SessionLocal classes for different modules
SessionLocalA = sessionmaker(autocommit=False, autoflush=False, bind=engine_a)
SessionLocalB = sessionmaker(autocommit=False, autoflush=False, bind=engine_b)

# Legacy support for backward compatibility
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session based on module
def get_db_by_module(module: str):
    if module.upper() == "A":
        db = SessionLocalA()
    elif module.upper() == "B":
        db = SessionLocalB()
    else:
        # Default to legacy database for backward compatibility
        db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()

# Legacy dependency for backward compatibility
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 