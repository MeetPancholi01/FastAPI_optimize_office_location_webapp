from database import Base
from sqlalchemy import create_engine, String, Float, Boolean, Integer, Column, Text, text
from sqlalchemy.orm import sessionmaker
class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255),nullable=False)
    address = Column(Text)
    lat = Column(Float,nullable=False)
    long = Column(Float,nullable=False)
    area = Column(String(255),nullable=False)
    def __repr__(self):
        return f"<Employee name> - {self.name} <Employee id> - {self.id}"
    
class Office(Base):
    __tablename__ = 'offices'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(Text)
    lat = Column(Float,nullable=False)
    long = Column(Float,nullable=False)
    area = Column(String(255),nullable=False)
    def __repr__(self):
        return f"<Office address> - {self.address} <Office id> - {self.id}"