from pydantic import BaseModel,EmailStr,AnyUrl , Field,field_validator
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    name:str
    age: int
    weight:float
    email: EmailStr
    linkdin_url: AnyUrl
    married:bool
    allergies:List[str]
    contact:Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains=['hdfc.com','icici.com']
        domain_name=value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('not a valid domain')
        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls,name):
        return name.upper()
    
    @field_validator('age',mode='after')
    @classmethod
    def validate_age(cls,value):

        if 0<value<100:
            return value
        else:
            raise ValueError('age is not real')




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