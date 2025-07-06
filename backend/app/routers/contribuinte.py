from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/contribuinte", tags=["contribuinte"])

@router.post("/", response_model=schemas.Contribuinte)
def create_contribuinte(
    contribuinte: schemas.ContribuinteCreate,
    db: Session = Depends(get_db)
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
    db: Session = Depends(get_db)
):
    contribuintes = db.query(models.Contribuinte).offset(skip).limit(limit).all()
    return contribuintes

@router.get("/by-date/{dat_proce}", response_model=List[schemas.Contribuinte])
def read_contribuintes_by_date(
    dat_proce: str,
    db: Session = Depends(get_db)
):
    """
    Get all contribuintes for a specific process date (dat_proce).
    Date should be in YYYY-MM-DD format.
    """
    try:
        # Convert string to date object for comparison
        from datetime import datetime
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

@router.get("/{ref_id}", response_model=schemas.Contribuinte)
def read_contribuinte(
    ref_id: int,
    db: Session = Depends(get_db)
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
    db: Session = Depends(get_db)
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
    db: Session = Depends(get_db)
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
    db: Session = Depends(get_db)
):
    db_contribuinte = db.query(models.Contribuinte).filter(
        models.Contribuinte.ref_id == ref_id
    ).first()
    if db_contribuinte is None:
        raise HTTPException(status_code=404, detail="Contribuinte not found")
    
    db.delete(db_contribuinte)
    db.commit()
    return {"message": "Contribuinte deleted successfully"} 