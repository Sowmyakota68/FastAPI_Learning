import pytest

class Student:
    def __init__(self, first_name:str,last_name:str, major:str,years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years
        
@pytest.fixture()
def default_employee():
    return Student("sowmya","kota","EEE",4)

def test_student_details(default_employee):
    assert default_employee.first_name == "sowmya"
    assert default_employee.last_name =="kota"
    assert default_employee.major == "EEE"
    assert default_employee.years == 4



