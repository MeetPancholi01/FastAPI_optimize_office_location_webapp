from database import SessionLocal
import models
from schema import Employee, Office
from fastapi import HTTPException,status,APIRouter
from math import radians, cos, sin, asin, sqrt
from geopy.geocoders import Nominatim
import requests
from fastapi.responses import JSONResponse
from sklearn.cluster import KMeans
import numpy as np
from sqlalchemy.orm import Session
import json

router = APIRouter()

class Valuenotfound(Exception):
    def __init__(self):
        self.code=404
        self.message = "Resource not Found"   
        super().__init__(self.message)

def create_session():
    # print("---------------------------------not mocked")
    db = SessionLocal()
    print("xyz")
    return db

db = create_session()
def existing_employee(employee:Employee):
    db = create_session()
    db_employee = db.query(models.Employee).filter(models.Employee.name == employee.name).first()
    if(db_employee is None):
        return False
    else:
        return True

def existing_employee_id(db,id):
    emp = db.query(models.Employee).filter(models.Employee.id == id).first()
    return emp
    

def func(srt:str):
    lt = srt.split()
    req_body = "https://api.geoapify.com/v1/geocode/search?text="
    for i in range(len(lt)):
        if(i == len(lt)-1):
            req_body += lt[i]
        else:
            req_body += lt[i]
            req_body += "%20"
    dr = "&format=json&apiKey=d548c5ed24604be6a9dd0d989631f783"
    req_body += dr
    response = requests.get(req_body)
    if(response.status_code == 200):
        data = response.json()
        if(len(data['results']) == 0):
            return [None,None]
        else:
            lat_ = data['results'][0]['lat']
            long_ = data['results'][0]['lon']
            return [lat_,long_]
    else:
        raise HTTPException(status_code=404,detail="Couldn't fetch latitude and longitude for the given address")

def getdistance(lat1, lat2, lon1, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2) 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
    return(c * r)

@router.get('/employees',status_code=status.HTTP_200_OK)
# @router.get('/employees',status_code=200)
def get_all_employees():
    db = create_session()
    employees = db.query(models.Employee).all()
    return employees

@router.get('/employees/{id}',status_code = status.HTTP_200_OK)
# @router.get('/employees/{id}',status_code = status.HTTP_200_OK)
def get_an_employee(id:int):
    db = create_session()
    employee = db.query(models.Employee).filter(models.Employee.id == id).first()
    return employee


@router.post('/employees',status_code = status.HTTP_201_CREATED)
def create_an_employee(employee:Employee):
    # import pdb; pdb.set_trace()
    db = create_session()
    [lat_,long_] = func(employee.address)
    if(lat_ == None or long_ == None):
        raise HTTPException(status_code=400,detail="Address could not be found")
    else:
        new_employee = models.Employee(
            name = employee.name,
            lat = lat_,
            long = long_,
            address = employee.address,
            area = employee.area
        )
    is_current_employee = existing_employee(employee)
    if is_current_employee:
        raise HTTPException(status_code=400,detail = "Employee already exist")
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return JSONResponse(content={"name": new_employee.name, "address": new_employee.address}, status_code=status.HTTP_201_CREATED)

@router.put('/employees/{id}')
def update_employee(id:int,employee:Employee):
    db = create_session()
    employee_to_update = existing_employee_id(id)
    if(employee_to_update is None):
        raise Valuenotfound
    else:
        employee_to_update.name = employee.name
        employee_to_update.address = employee.address
        [lat,long] = func(employee.address)
        employee_to_update.lat = lat
        employee_to_update.long = long
        employee_to_update.area = employee.area
        db.commit()
    # return employee_to_update
        return JSONResponse(content={"name": employee_to_update.name, "address":employee_to_update.address},status_code=status.HTTP_200_OK)

    

@router.delete('/employees/{id}')
def delete_employee(id:int):
    db = create_session()
    emp = existing_employee_id(db,id)
    if emp is None:
        raise Valuenotfound
    db.delete(emp)
    db.commit()
    empl = json.dumps(emp)
    return JSONResponse(content={"id":id})

# Offices endpoints-------------------------------------------------------------->

@router.get('/offices',status_code=200)
def get_Offices():
    db = create_session()
    offices = db.query(models.Office).all()
    return {"results":offices}

@router.get('/office/{id}',status_code = status.HTTP_200_OK)
def get_an_office(id:int):
    db = create_session()
    office= db.query(models.Office).filter(models.Office.id == id).first()
    return office

@router.post('/offices',status_code = status.HTTP_201_CREATED)
def create_an_office(office:Office):
    db = create_session()
    [lat_,long_] = func(office.address)
    if(lat_ == None or long_ == None):
        raise HTTPException(status_code=400,detail="Address could not be found")
    else:
        new_office = models.Office(
            lat = lat_,
            long = long_,
            address = office.address,
            area = office.area
        )
    # import pdb; pdb.set_trace()
    db_office = db.query(models.Office).filter(models.Office.address == office.address).first()
    if db_office != None:
        raise HTTPException(status_code=400,detail = "Office already exist")
    db.add(new_office)
    db.commit()
    db.refresh(new_office)
    return JSONResponse(content={"address":new_office.address,"area":new_office.area},status_code=status.HTTP_201_CREATED)

@router.put('/offices/{id}')
def update_office(id:int,office:Office):
    db = create_session()
    office_to_update = db.query(models.Office).filter(models.Office.id == id).first()
    if(office_to_update is None):
        raise HTTPException(status_code=404,detail="Office Not Found")
    office_to_update.address = office.address
    [lat,long] = func(office.address)
    office_to_update.area = office.area
    office_to_update.lat = lat
    office_to_update.long = long
    db.commit()
    return JSONResponse(content={"address":office_to_update.address,"area":office_to_update.area},status_code=status.HTTP_200_OK)

@router.delete('/offices/{id}')
def delete_office(id:int):
    db = create_session()
    office = db.query(models.Office).filter(models.Office.id == id).first()
    if office is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "Resource not Found")
    db.delete(office)
    db.commit()
    return JSONResponse(content={"address":office.address,"area":office.area},status_code=status.HTTP_200_OK)

@router.get('/office-employee-distance/{office_id}/{employee_id}')
def get_distance(office_id:int,employee_id:int):
    db = create_session()
    office_lat = db.query(models.Office).filter(models.Office.id == office_id).first().lat
    office_long = db.query(models.Office).filter(models.Office.id == office_id).first().long
    employee_lat = db.query(models.Employee).filter(models.Employee.id == employee_id).first().lat
    employee_long = db.query(models.Employee).filter(models.Employee.id == employee_id).first().long
    employee_name = db.query(models.Employee).filter(models.Employee.id == employee_id).first().name
    distance = getdistance(office_lat,employee_lat,office_long,employee_long)
    dist = round(distance,2)
    return JSONResponse(content={"Office id":office_id,"Employee name":employee_name,"Distance in Km":dist})


@router.get('/better_locations/{office_id1}/{office_id2}')
def get_better_location(office_id1:int,office_id2:int):
    d1 = 0 # For office 1
    d2 = 0 # For office 2
    employees = requests.get('http://127.0.0.1:8000/employees')
    office1 = requests.get(f'http://127.0.0.1:8000/office/{office_id1}')
    office2 = requests.get(f"http://127.0.0.1:8000/office/{office_id2}")
    if(office1.status_code == 200 and office2.status_code == 200):
        office1 = office1.json()
        office2 = office2.json()
        lat1 = office1['lat']
        long1 = office1['long']
        lat2 = office2['lat']
        long2 = office2['long']
        pass
    else:
        raise HTTPException(status_code=404,detail="One or Both the office id doesn't exist")
    if(employees.status_code == 200):
        employee_list = employees.json()
        for object in employee_list:
            lat = object['lat'] 
            long = object['long']
            d1 += getdistance(lat,lat1,long,long1)
            d2 += getdistance(lat,lat2,long,long2)
        if(d1 > d2):
            return JSONResponse(content={"Office_id":office_id2,"Verdict":f"Office with id {office_id2} is better"})
        elif(d2 > d1):
            return JSONResponse(content={"Office_id":office_id1,"Verdict":f"Office with id {office_id1} is better"})
        else:
            return JSONResponse(content={"Verdict":"Both offices are equally optimal"})
    else:
        raise HTTPException(status_code=employees.status_code,detail="Couldn't make request")
    
@router.get('/employees/clusters/{no_of_clusters}')
def get_clusters(no_of_clusters:int):
    employees = requests.get('http://127.0.0.1:8000/employees')
    if(employees.status_code == 200):
        employees = employees.json()
        coords = []
        for employee in employees:
            coords.append([employee['lat'],employee['long']])
        arr = np.array(coords)
        clus = no_of_clusters
        kmeans = KMeans(n_clusters=clus)
        kmeans.fit(arr)
        labels = kmeans.labels_
        dic = {}
        lbls = labels.tolist()
        ln = len(employees)
        for i in range(ln):
            dic[employees[i]['id']] = lbls[i]
        res = []
        for i in dic:
            obj = {}
            obj['Employee Id']=i
            obj['Cluster'] = f'C{dic[i]}'
            emp_name = requests.get(f'http://127.0.0.1:8000/employees/{i}')
            if(emp_name.status_code == 200):
                emp_name = emp_name.json()
                emp_name = emp_name['name']
                obj['Employee Name'] = emp_name
                res.append(obj)
            else:
                raise HTTPException(status_code = 200,detail="Could not be found")
        return JSONResponse(content={"result":res})   
    else:
        raise HTTPException(status_code=400,detail="Couldn't make requests")
    