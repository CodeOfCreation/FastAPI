from pydantic import BaseModel,EmailStr,AnyUrl , Field,model_validator,computed_field
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

    @computed_field
    @property
    def calculate_bmi(self) ->float:
        bmi= round(self.weight/(self.height**2),2)
        return bmi


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.calculate_bmi)
    print("inserted successfully")

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.calculate_bmi)
    print("inserted successfully")

patient_dict = {"name": "Mahadev", "age": 29,'weight':60,'married':True,'allergies':['Pollen','Dust'],'contact':{'email':'mhd@gmail.com','phone':'9999999999'}}

patient1 = Patient(**patient_dict)

insert_patient_data(patient1)   