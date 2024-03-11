import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import json
# from src.main import app
import sys
import os
current_directory = os.path.dirname(__file__)
parent_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(parent_directory)
from src.main import app
from src.endpoints import delete_employee, Valuenotfound
from src.endpoints import get_all_employees,get_an_employee,create_an_employee,update_employee
from src.endpoints import get_Offices,get_an_office,create_an_office, update_office, delete_office
from src.schema import Employee
from src import models

@pytest.fixture
def client():
    return TestClient(app)

# @pytest.fixture(scope="function")
# def db_session():
#     """
#     Fixture to provide a test database session.
#     """
#     # Here you could create a temporary test database if needed
#     # In this example, we'll simply create a session
#     session = create_session()
#     yield session
#     session.close()

def test_get_all_employee(monkeypatch):
    mock_session = MagicMock(spec=Session)
    mock_employee = {"name":"Meet","address":"Bodakdev Ahmedabad"}
    mock_session.query().all.return_value = [mock_employee]
    monkeypatch.setattr("src.endpoints.create_session", lambda: mock_session)
    res = get_all_employees()
    assert res == [mock_employee]

def test_get_an_employee(monkeypatch):
    mock_session = MagicMock(spec=Session)
    mock_employee = {"name":"Meet","address":"Bodakdev Ahmedabad"}
    mock_session.query().filter().first.return_value = mock_employee
    monkeypatch.setattr("src.endpoints.create_session", lambda: mock_session)
    id = 1
    res = get_an_employee(id)
    assert res == mock_employee

@patch("src.endpoints.func")
@patch("src.endpoints.create_session")
def test_create_an_employee_no_address(mock_session_details, mock_function):
    # def test_create_an_employee_no_address(monkeypatch):
    mock_session = MagicMock(spec=Session)
    # mock_function = MagicMock(return_value=[None,None])
    mock_employee = models.Employee
    mock_employee.name = "Meet"
    mock_employee.address = "Bodakdev Ahmedabad"
    mock_employee.area = "Nahi Pata"
    mock_function.return_value = [None,None]
    mock_session_details.return_value = mock_session
    # create_an_employee.func = MagicMock(return_value = [None,None])
    x = mock_employee.address
    # monkeypatch.setattr('src.endpoints.func', mock_function)
    # monkeypatch.setattr("src.endpoints.create_session", mock_session)
    with pytest.raises(HTTPException) as err:
        create_an_employee(mock_employee)
    # import pdb; pdb.set_trace()
    assert err.value.detail == "Address could not be found"
    assert err.value.status_code == 400

@patch("src.endpoints.existing_employee")
@patch("src.endpoints.func")
@patch("src.endpoints.create_session")
def test_create_an_employee_existing_employee(mock_session_detail,mock_function,mock_existing_employee):
    mock_session = MagicMock(spec=Session)
    mock_employee = models.Employee
    mock_employee.name = "Meet Pancholi"
    mock_employee.address = "Bodakdev Ahmedabad"
    mock_employee.area = "Bodakdev"
    mock_existing_employee.return_value = True
    mock_session_detail.return_value = mock_session
    mock_function.return_value = [23.11,72.09]
    with pytest.raises(HTTPException) as err:
        create_an_employee(mock_employee)
    assert err.value.detail == "Employee already exist"
    assert err.value.status_code == 400

@patch("src.endpoints.existing_employee")
@patch("src.endpoints.func")
@patch("src.endpoints.create_session")
def test_create_an_employee_existing_employee(mock_session_detail,mock_function,mock_existing_employee):
    mock_session = MagicMock(spec=Session)
    mock_employee = models.Employee
    mock_employee.name = "Meet Pancholi"
    mock_employee.address = "Bodakdev Ahmedabad"
    mock_employee.area = "Bodakdev"
    mock_existing_employee.return_value = False
    mock_session_detail.return_value = mock_session
    mock_session_detail.add.return_value = None
    mock_session_detail.commit.return_value = None
    mock_session_detail.refresh.return_value = None
    mock_function.return_value = [23.11,72.09]
    res = create_an_employee(mock_employee)
    # print(f"==================>{dir(res)}")
    assert res.status_code == 201

@patch("src.endpoints.existing_employee_id")
@patch("src.endpoints.create_session")
def test_update_employee_no_employee(mock_session_detail,mock_existing_employee_id):
    mock_session = MagicMock(spec=Session)
    id = 4
    mock_employee = models.Employee
    mock_employee.name = "Rohit Deshmukh"
    mock_employee.address = "Prerna viraj-2 jodhpur gam aagan party plot satellite ahmedabad"
    mock_employee.area = "Satellite"
    mock_session_detail.return_value = mock_session
    mock_existing_employee_id.return_value = None
    with pytest.raises(Valuenotfound) as err:
        update_employee(id,mock_employee)
    assert err.value.message == "Resource not Found"
    assert err.value.code == 404  

@patch("src.endpoints.func")
@patch("src.endpoints.existing_employee_id")
@patch("src.endpoints.create_session")
def test_update_employee_overall(mock_session_detail,mock_existing_employee_id,mock_function):
    mock_session = MagicMock(spec=Session)
    id=4
    mock_employee = models.Employee
    mock_employee.name = "Rohit Deshmukh"
    mock_employee.address = "Prerna viraj-2 jodhpur gam aagan party plot satellite ahmedabad"
    mock_employee.area = "Bodakdev"
    mock_session_detail.return_value = mock_session
    mock_existing_employee_id.return_value = mock_employee
    mock_function.return_value = [23.11,72.09]
    mock_session_detail.commit.return_value = None
    res = update_employee(id,mock_employee)
    assert res.status_code == 200


# @patch('endpoints.create_session')
def test_delete_employee_no_employee(monkeypatch):
    mock_session = MagicMock(spec=Session)
    mock_session.query().filter().first.return_value = None
    id = 35
    monkeypatch.setattr("src.endpoints.create_session", lambda: mock_session)
    # delete_employee(id).existing_employee_id = MagicMock(return_value=None)
    with pytest.raises(Valuenotfound) as err:
        delete_employee(id)
    assert err.value.message == "Resource not Found"
    assert err.value.code == 404  
    
def test_delete_employee_yes_employee(monkeypatch):
    mock_session = MagicMock(spec=Session)
    mock_employee = {"name":"xyz","address":"Bodakdev Ahmedabad"}
    mock_employee = json.dumps(mock_employee)
    mock_session.query().filter().first.return_value = mock_employee
    delete_employee.existing_employee_id = MagicMock(return_value=mock_employee)
    mock_session.delete.return_value = None
    mock_session.commit.return_value=None
    id = 34
    monkeypatch.setattr("src.endpoints.create_session", lambda: mock_session)
    delete_employee(id)
    assert True

# -------- FOR OFFICES APIs
@patch("src.endpoints.create_session")
def test_get_offices(mock_session_details):
    mock_session = MagicMock(spec=Session)
    mock_session_details.return_value = mock_session
    # mock_session.query().all.return_value = None
    mock_session_details.query.return_value = mock_session.query()
    mock_session_details.query.return_value.all.return_value = None
    res = get_Offices()
    assert res['results'] == None

@patch("src.endpoints.create_session")
def test_get_an_office(mock_session_details):
    mock_session = MagicMock(spec = Session)
    mock_session_details.return_value = mock_session
    mock_session.query().filter().first.return_value = None
    id=1
    res = get_an_office(id)
    return res == None

@patch("src.endpoints.func")
@patch("src.endpoints.create_session")
def test_create_an_office_no_address(mock_session_details,mock_function):
    mock_session = MagicMock(spec = Session)
    mock_session_details.return_value = mock_session
    mock_function.return_value = [None,23]
    mock_office = models.Office
    mock_office.address = "IIM Road Ahmedabad"
    mock_office.area = "IIM Road"
    with pytest.raises(HTTPException) as err:
        create_an_office(mock_office)
    assert err.value.detail == "Address could not be found"
    assert err.value.status_code == 400

@patch("src.endpoints.func")
@patch("src.endpoints.create_session")
def test_create_an_office_existing_office(mock_session_details,mock_function):
    mock_session = MagicMock(spec = Session)
    mock_session_details.return_value = mock_session
    mock_function.return_value = [23,72]
    mock_office = models.Office
    mock_office.address = "IIM Road Ahmedabad"
    mock_office.area = "IIM Road"
    mock_session_details.query.return_value = mock_session.query()
    mock_session_details.query.filter.return_value = mock_session.query().filter()
    mock_session_details.query.filter.first.return_value = 1
    with pytest.raises(HTTPException) as err:
        create_an_office(mock_office)
    assert err.value.detail == "Office already exist"
    assert err.value.status_code == 400

@patch("src.endpoints.func")
@patch("src.endpoints.create_session")
def test_create_an_office_overall(mock_session_details,mock_function):
    mock_session = MagicMock(spec = Session)
    mock_session_details.return_value = mock_session
    mock_function.return_value = [23,72]
    mock_office = models.Office
    mock_office.address = "IIM Road Ahmedabad"
    mock_office.area = "IIM Road"
    # mock_session_details.query.return_value = mock_session.query()
    # mock_session_details.query.filter.return_value = mock_session.query.filter()
    # mock_session_details.query.return_value = None
    # mock_session_details.query.filter.return_value = None
    # mock_session_details.query.filter.first.return_value = None
    mock_session.query().filter().first.return_value = None
    # mock_session_details.add.return_value = None
    mock_session.add.return_value = None
    # mock_session_details.commit.return_value = None
    mock_session.commit.return_value = None
    # mock_session_details.refresh.return_value = None
    mock_session.refresh.return_value = None
    res = create_an_office(mock_office)
    assert res.status_code == 201


#  1ST METHOD TO MOCK
# @patch("src.endpoints.func")
# @patch("src.endpoints.create_session")
# def test_create_an_office_overall(mock_session_details,mock_function):
#     mock_session = MagicMock(spec = Session)
#     mock_session_details.return_value = mock_session
#     mock_function.return_value = [23,72]
#     mock_office = models.Office
#     mock_office.address = "IIM Road Ahmedabad"
#     mock_office.area = "IIM Road"
#     mock_session.query().filter().first.return_value = None
#     mock_session.add.return_value = None
#     mock_session.commit.return_value = None
#     mock_session.refresh.return_value = None
#     res = create_an_office(mock_office)
#     assert res.status_code == 201


# 2ND METHOD to MOCK
@patch("src.endpoints.func")
@patch("src.endpoints.create_session")
def test_create_an_office_overall(mock_session_details,mock_function):
    mock_session = MagicMock(spec = Session)
    mock_session_details.return_value = mock_session
    mock_function.return_value = [23,72]
    mock_office = models.Office
    mock_office.address = "IIM Road Ahmedabad"
    mock_office.area = "IIM Road"
    mck_query = mock_session.query.return_value
    mck_filter = mck_query.filter.return_value
    mck_filter.first.return_value = None
    # mock_session.query().filter().first.return_value = None
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None
    res = create_an_office(mock_office)
    assert res.status_code == 201



# 3RD METHOD TO MOCK
# @patch("src.endpoints.func")
# @patch("src.endpoints.create_session")
# def test_create_an_office_overall(mock_session_details, mock_function):
#     # Mocking the create_session function to return a MagicMock object
#     mock_session = mock_session_details.return_value
#     # Patching the return value of func() with a list [23, 72]
#     mock_function.return_value = [23, 72]
#     # Creating a MagicMock object to simulate an instance of the Office model
#     mock_office = models.Office
#     # Setting attributes for the mock office object
#     mock_office.address = "IIM Road Ahmedabad"
#     mock_office.area = "IIM Road"
#     # Mocking the query() method of the session object
#     mock_query = mock_session.query.return_value
#     # Mocking the filter() method of the query object
#     mock_filter = mock_query.filter.return_value
#     # Mocking the first() method of the filter object to return None
#     mock_filter.first.return_value = None
#     # Mocking the add(), commit(), and refresh() methods of the session object to return None
#     mock_session.add.return_value = None
#     mock_session.commit.return_value = None
#     mock_session.refresh.return_value = None
#     # Calling the function create_an_office() with the mock office object
#     res = create_an_office(mock_office)
#     # Asserting that the status code of the response is 201
#     assert res.status_code == 201

@patch("src.endpoints.func")
@patch("src.endpoints.create_session")
def test_update_office_no_office(mock_session_details,mock_function):
    mock_session = MagicMock(spec=Session)
    mock_session_details.return_value = mock_session
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None
    mock_function.return_value = [23,72]
    mock_office = models.Office
    mock_office.address = "IIM Road Ahmedabad"
    mock_office.area = "IIM Road"
    id = 2
    with pytest.raises(HTTPException) as err:
        update_office(id,mock_office)
    assert err.value.detail == "Office Not Found"
    assert err.value.status_code == 404

@patch("src.endpoints.func")
@patch("src.endpoints.create_session")
def test_update_office_overall(mock_session_details,mock_function):
    mock_session = MagicMock(spec=Session)
    mock_session_details.return_value = mock_session
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_function.return_value = [23,72]
    mock_office = models.Office
    mock_office.address = "IIM Road Ahmedabad"
    mock_office.area = "IIM Road"
    mock_filter.first.return_value = mock_office
    mock_session.commit.return_value = None
    id = 2
    res = update_office(id,mock_office)
    assert res.status_code == 200

@patch("src.endpoints.create_session")
def test_delete_office_no_office(mock_session_details):
    mock_session = MagicMock(spec=Session)
    mock_session_details.return_value = mock_session
    mock_session.query().filter().first.return_value = None
    id = 3
    with pytest.raises(HTTPException) as err:
        delete_office(id)
    assert err.value.detail == "Resource not Found"
    assert err.value.status_code == 404

@patch("src.endpoints.create_session")
def test_delete_office_overall(mock_session_details):
    mock_session = MagicMock(spec=Session)
    mock_session_details.return_value = mock_session
    mock_office = models.Office
    mock_office.address = "IIM Road Ahmedabad"
    mock_office.area = "IIM Road"
    mock_session.query().filter().first.return_value = mock_office
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None
    id = 2
    res = delete_office(id)
    assert res.status_code == 200
















    
    
    
    


    

    
        

    
    
    
    
    

