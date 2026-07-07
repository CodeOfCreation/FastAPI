from pydantic import BaseModel,EmailStr,AnyUrl , Field,model_validator
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    name: str
    age: int
    weight:float
    email: EmailStr
    linkdin_url: AnyUrl
    married:bool
    allergies:Optional[List[str]]= None
    contact:Dict[str,str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls,model):
        if model.age>60 and 'emergency_contact' not in model.contact:
            raise ValueError('patient more than 60 must have a contact')
        


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("inserted successfully")

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("inserted successfully")

patient_dict = {"name": "Mahadev", "age": 29,'weight':60,'married':True,'allergies':['Pollen','Dust'],'contact':{'email':'mhd@gmail.com','phone':'9999999999'}}

patient1 = Patient(**patient_dict)

insert_patient_data(patient1)   