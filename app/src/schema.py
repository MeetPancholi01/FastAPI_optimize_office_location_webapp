from pydantic import BaseModel

class Employee(BaseModel):
    name:str
    address:str
    area:str
    class Config:
        orm_mode = True

class Office(BaseModel):
    address:str
    area:str
    class Config:
        orm_mode = True