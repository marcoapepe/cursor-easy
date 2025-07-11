from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
import csv
import io
from .. import models, schemas
from ..database import get_db, get_db_by_module

router = APIRouter(prefix="/contribuinte", tags=["contribuinte"])

def get_db_session(module: str = Query("A", description="Module to use (A or B)")):
    for db in get_db_by_module(module):
        yield db

@router.post("/", response_model=schemas.Contribuinte)
def create_contribuinte(
    contribuinte: schemas.ContribuinteCreate,
    module: str = Query("A", description="Module to use (A or B)"),
    db: Session = Depends(get_db_session)
):
    # Check if CPF/CNPJ already exists
    existing = db.query(models.Contribuinte).filter(
        models.Contribuinte.cpf_cnpj == contribuinte.cpf_cnpj
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="CPF/CNPJ already registered")
    
    # Check if email already exists (if provided)
    if contribuinte.email:
        existing_email = db.query(models.Contribuinte).filter(
            models.Contribuinte.email == contribuinte.email
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    db_contribuinte = models.Contribuinte(**contribuinte.dict())
    db.add(db_contribuinte)
    db.commit()
    db.refresh(db_contribuinte)
    return db_contribuinte

@router.get("/", response_model=List[schemas.Contribuinte])
def read_contribuintes(
    skip: int = 0,
    limit: int = 100,
    module: str = Query("A", description="Module to use (A or B)"),
    db: Session = Depends(get_db_session)
):
    contribuintes = db.query(models.Contribuinte).offset(skip).limit(limit).all()
    return contribuintes

@router.get("/by-date/{dat_proce}", response_model=List[schemas.Contribuinte])
def read_contribuintes_by_date(
    dat_proce: str,
    module: str = Query("A", description="Module to use (A or B)"),
    db: Session = Depends(get_db_session)
):
    """
    Get all contribuintes for a specific process date (dat_proce).
    Date should be in YYYY-MM-DD format.
    """
    try:
        # Convert string to date object for comparison
        date_obj = datetime.strptime(dat_proce, "%Y-%m-%d").date()
        
        contribuintes = db.query(models.Contribuinte).filter(
            models.Contribuinte.dat_proce == date_obj
        ).all()
        
        return contribuintes
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid date format. Use YYYY-MM-DD format (e.g., 2024-01-15)"
        )

@router.get("/by-client/{client_name}", response_model=List[schemas.Contribuinte])
def read_contribuintes_by_client(
    client_name: str,
    module: str = Query("A", description="Module to use (A or B)"),
    db: Session = Depends(get_db_session)
):
    """
    Get all contribuintes where client name contains the search string.
    Uses case-insensitive LIKE query with wildcards.
    Example: /by-client/Pepe will find clients like "Pepe", "Pepe Company", "My Pepe Store", etc.
    """
    contribuintes = db.query(models.Contribuinte).filter(
        models.Contribuinte.cliente.ilike(f"%{client_name}%")
    ).all()
    
    return contribuintes

@router.get("/{ref_id}", response_model=schemas.Contribuinte)
def read_contribuinte(
    ref_id: int,
    module: str = Query("A", description="Module to use (A or B)"),
    db: Session = Depends(get_db_session)
):
    contribuinte = db.query(models.Contribuinte).filter(
        models.Contribuinte.ref_id == ref_id
    ).first()
    if contribuinte is None:
        raise HTTPException(status_code=404, detail="Contribuinte not found")
    return contribuinte

@router.get("/cpf/{cpf_cnpj}", response_model=schemas.Contribuinte)
def read_contribuinte_by_cpf(
    cpf_cnpj: str,
    module: str = Query("A", description="Module to use (A or B)"),
    db: Session = Depends(get_db_session)
):
    contribuinte = db.query(models.Contribuinte).filter(
        models.Contribuinte.cpf_cnpj == cpf_cnpj
    ).first()
    if contribuinte is None:
        raise HTTPException(status_code=404, detail="Contribuinte not found")
    return contribuinte

@router.put("/{ref_id}", response_model=schemas.Contribuinte)
def update_contribuinte(
    ref_id: int,
    contribuinte_update: schemas.ContribuinteUpdate,
    module: str = Query("A", description="Module to use (A or B)"),
    db: Session = Depends(get_db_session)
):
    db_contribuinte = db.query(models.Contribuinte).filter(
        models.Contribuinte.ref_id == ref_id
    ).first()
    if db_contribuinte is None:
        raise HTTPException(status_code=404, detail="Contribuinte not found")
    
    update_data = contribuinte_update.dict(exclude_unset=True)
    
    # Check for duplicate CPF/CNPJ if being updated
    if "cpf_cnpj" in update_data:
        existing = db.query(models.Contribuinte).filter(
            models.Contribuinte.cpf_cnpj == update_data["cpf_cnpj"],
            models.Contribuinte.ref_id != ref_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="CPF/CNPJ already registered")
    
    # Check for duplicate email if being updated
    if "email" in update_data and update_data["email"]:
        existing_email = db.query(models.Contribuinte).filter(
            models.Contribuinte.email == update_data["email"],
            models.Contribuinte.ref_id != ref_id
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    for field, value in update_data.items():
        setattr(db_contribuinte, field, value)
    
    db.commit()
    db.refresh(db_contribuinte)
    return db_contribuinte

@router.delete("/{ref_id}")
def delete_contribuinte(
    ref_id: int,
    module: str = Query("A", description="Module to use (A or B)"),
    db: Session = Depends(get_db_session)
):
    db_contribuinte = db.query(models.Contribuinte).filter(
        models.Contribuinte.ref_id == ref_id
    ).first()
    if db_contribuinte is None:
        raise HTTPException(status_code=404, detail="Contribuinte not found")
    
    db.delete(db_contribuinte)
    db.commit()
    return {"message": "Contribuinte deleted successfully"}

@router.post("/bulk-upload", response_model=dict)
def bulk_upload_contribuintes(
    file: UploadFile = File(...),
    module: str = Query("A", description="Module to use (A or B)"),
    db: Session = Depends(get_db_session)
):
    """
    Upload a CSV file with contribuinte records.
    Expected format: dat_proce;cpf_cnpj;cliente;email;dat_cadastro
    Date format: YYYY-MM-DD
    """
    if not file.filename or (not file.filename.endswith('.csv') and not file.filename.endswith('.txt')):
        raise HTTPException(
            status_code=400, 
            detail="File must be a CSV or TXT file"
        )
    
    try:
        # Read file content
        content = file.file.read().decode('utf-8')
        file.file.close()
        
        # Parse CSV content
        csv_reader = csv.reader(io.StringIO(content), delimiter=';')
        
        success_count = 0
        error_count = 0
        errors = []
        
        for row_num, row in enumerate(csv_reader, 1):
            if len(row) != 5:
                errors.append(f"Row {row_num}: Expected 5 columns, got {len(row)}")
                error_count += 1
                continue
            
            try:
                # Parse dates
                dat_proce = datetime.strptime(row[0], "%Y-%m-%d").date()
                dat_cadastro = datetime.strptime(row[4], "%Y-%m-%d").date() if row[4] else None
                
                # Check if CPF/CNPJ already exists
                existing = db.query(models.Contribuinte).filter(
                    models.Contribuinte.cpf_cnpj == row[1]
                ).first()
                
                if existing:
                    errors.append(f"Row {row_num}: CPF/CNPJ {row[1]} already exists")
                    error_count += 1
                    continue
                
                # Create new contribuinte record
                contribuinte_data = {
                    "dat_proce": dat_proce,
                    "cpf_cnpj": row[1],
                    "cliente": row[2],
                    "email": row[3] if row[3] else None,
                    "dat_cadastro": dat_cadastro
                }
                
                db_contribuinte = models.Contribuinte(**contribuinte_data)
                db.add(db_contribuinte)
                success_count += 1
                
            except ValueError as e:
                errors.append(f"Row {row_num}: Invalid date format - {str(e)}")
                error_count += 1
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
                error_count += 1
        
        # Commit all successful records
        if success_count > 0:
            db.commit()
        
        return {
            "message": "Bulk upload completed",
            "success_count": success_count,
            "error_count": error_count,
            "errors": errors[:10] if len(errors) > 10 else errors  # Limit error messages
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        ) 