from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Contribuinte schemas
class ContribuinteBase(BaseModel):
    dat_proce: date
    cpf_cnpj: str
    cliente: str
    email: Optional[EmailStr] = None
    dat_cadastro: Optional[date] = None

class ContribuinteCreate(ContribuinteBase):
    pass

class ContribuinteUpdate(BaseModel):
    dat_proce: Optional[date] = None
    cpf_cnpj: Optional[str] = None
    cliente: Optional[str] = None
    email: Optional[EmailStr] = None
    dat_cadastro: Optional[date] = None

class Contribuinte(ContribuinteBase):
    ref_id: int
    
    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 