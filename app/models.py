from sqlalchemy import Column,Integer,String
from app.database import Base
class Anexo5(Base):
    __tablename__="anexo5"
    id=Column(Integer,primary_key=True)
    terminal=Column(String)
    servicio=Column(String)
    tipo_dia=Column(String)
class Voucher(Base):
    __tablename__="vouchers"
    id=Column(Integer,primary_key=True)
    numero=Column(String,unique=True)
    terminal=Column(String)
    servicio=Column(String)
    tipo_dia=Column(String)
