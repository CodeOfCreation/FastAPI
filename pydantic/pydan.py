from pydantic import BaseModel,EmailStr,AnyUrl , Field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    name: Annotated[str,Field(max_length=50,title='Name of the patient',description='give the name of the patient under the 50 characters')]
    age: int
    weight:float = Field(gt=0,lt=120)
    email: EmailStr
    linkdin_url: AnyUrl
    married:bool=False
    allergies:Optional[List[str]]= None
    contact:Dict[str,str]


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