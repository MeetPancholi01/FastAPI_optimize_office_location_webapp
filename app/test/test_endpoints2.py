# Test cases for Employee endpoints
# def test_get_all_employees(client):
#     response = client.get('/employees')
#     assert response.status_code == 200

# def test_get_an_employee(client):
#     mock_employee={
#         "name": "Meet",
#         "address": "Agrawal Appt",
#         "area": "Satellite"
#     }
    
    
#     # response = client.get('/employees/1')  # Assuming there is an employee with ID 1
#     assert response.status_code == 200
    

# @patch('endpoints.create_session')
# def test_create_an_employee(mock_create_session, client):
#     # Mock the behavior of create_session to return a mock session
#     mock_session = MagicMock()
#     mock_create_session = MagicMock(return_value=mock_session)
    
#     # Define the data to be sent in the request
#     employee_data = {"name": "abcdefg", "address": "Bodakdev Ahmedabad", "area": "Bodakdev"}
    
#     # Mock the response JSON data
#     mock_response_json = {"name": "abcdefg", "address": "Bodakdev Ahmedabad"}
    
#     # Configure the mock session to return the mock response JSON
#     mock_session.post().json = MagicMock(return_value=mock_response_json)
    
#     # Call the endpoint to create an employee
#     response = client.post('/employees', json=employee_data)
    
#     # Check if the response status code is 201
#     assert response.status_code == 201
    
#     # Check if the response JSON contains the expected data
#     response_json = response.json()
#     assert "name" in response_json
#     assert "address" in response_json
#     # emp = db.query(models.Employee).filter(models.Employee.name == "abcdefg").first()
#     # db.delete(emp)
#     # db.commit()
    
   
# @patch('endpoints.create_session') 
# def test_update_an_employee(mock_create_session,client):
#     mock_session = MagicMock()
#     mock_create_session = MagicMock(return_value=mock_session)
#     employee_data = {"name": "xyz", "address": "GIFT City Gandhinagar Gujarat", "area": "Gandhinagar"}
#     mock_json = {"name":"xyz","address": "GIFT City Gandhinagar Gujarat"}
#     mock_session.put().json = MagicMock(return_value = mock_json)
#     id = 63
#     response = client.put(f'/employees/{id}',json=employee_data)
#     assert response.status_code == 200
#     response_json = response.json()
#     assert  "name" in response_json
#     assert "address" in response_json

# def test_update_employee():
#     mock_json = {"name":"xyz","address":"Bodakdev Ahmedabad"}
#     mock_employee = {
#         "name":"xyz",
#         "address":"Bodakdev Ahmedabad",
#         "area":"Bodakdev"
#     }
#     update_employee = MagicMock(return_value = mock_json)
#     result = update_employee(2,mock_employee)
#     assert result == mock_json

# def test_update_employee_no_employee():
#     update_employee.existing_employee_id = MagicMock(return_value=None)
#     mock_employee = {
#         "name":"xyz",
#         "address":"Bodakdev Ahmedabad",
#         "area":"Bodakdev"
#     }
#     with pytest.raises(Valuenotfound) as err:
#         update_employee(1,mock_employee)
#     assert err.value.message == "Resource not Found"
#     assert err.value.code == 404  

# @patch('endpoints.create_session')
# def test_delete_employee():
#     mock_json = {"id":1,"name":"John Doe"}
#     delete_employee = MagicMock(
#         return_value=mock_json
#     )
#     result = delete_employee(1)
#     assert result == mock_json