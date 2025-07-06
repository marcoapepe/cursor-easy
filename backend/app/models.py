from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Contribuinte(Base):
    __tablename__ = "contribuinte"
    
    ref_id = Column(Integer, primary_key=True, index=True)
    dat_proce = Column(Date, nullable=False)
    cpf_cnpj = Column(String(14), nullable=False)
    cliente = Column(String(80), nullable=False)
    email = Column(String(255), unique=True)
    dat_cadastro = Column(Date) 