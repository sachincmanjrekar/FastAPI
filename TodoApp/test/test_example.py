import pytest


def test_equal_or_not_equal():
    assert 3!=2

def teste_is_instance():
    assert isinstance('this is a string',str)
    assert not isinstance('10',int)



def test_booean():
    validated = True
    assert validated == True
    assert ('hello' == 'world') is False


def test_type():
    assert type('He' is str)
    assert type('He' is not int)


class Student:
    def __init__(self,first_name:str,last_name:str, major:str, years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Student('Sachin', 'M', 'CS', 3)


def test_person_initialization(default_employee):
    assert default_employee.first_name == 'Sachin', 'First name should be Sachin'
    assert default_employee.last_name == 'M', "Last name should be M"
    assert default_employee.major == 'CS'
    assert default_employee.years == 3
