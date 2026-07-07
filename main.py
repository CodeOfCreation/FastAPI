from fastapi import FastAPI,Path,Header,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal


app=FastAPI()

class Patient(BaseModel):
    
    id:Annotated[str,Field(...,description='Id of the patient',examples=['P001'])]
    name:Annotated[str,Field(...,description='name of the patient')]
    city:Annotated[str,Field(...,description='city of the patient')]
    age:Annotated[int,Field(...,gt=0,lt=120,description='age of the patient')]
    gender:Annotated[Literal['Male','Female','others'],Field(...,description='gender of the patient')]
    height:Annotated[float,Field(...,gt=0,description='height of the patient')]
    weight:Annotated[float,Field(...,gt=0,description='weight of the patient')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height*self.height),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi<18.5:
            return 'underweight'
        elif self.bmi>25:
            return 'normal'
        else:
            return 'obese'

@app.get("/")
def hello():
    return {'message':"hello world"} 

@app.get("/about")
def about():
    return {'message':'deva d xebec'}

def load_data():
    with open('patients.json','r') as f:
       data = json.load(f)
    return data

def save_data(data):
    with open("patients.json",'w') as f:
        json.dump(data,f)

@app.get('/view')
def view():
    data= load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id:str = Path(...,description='ID Of the patient in database',example='P003')):
    data=load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='patient not found in database')



@app.get('/sort')
def sort_patients(sort_by:str = Query(...,description='sort on the basis of height and weight or bmi'),order:str=Query('asc',description='sorted on asceding or descending order')):
   valid_fields=['height','weight','bmi']
   if sort_by not in valid_fields:
       raise HTTPException(status_code=400,detail=f'invalid fields select from {valid_fields}')
   
   if order not in ['asc','desc']:
       raise HTTPException(status_code=400,detail=f'invalid order please select asc or desc')
   
   sort_order= True if order=='desc' else False

   data=load_data()
   sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)

@app.post('/create')
def create_patient(patient:Patient):
    # load existing data
    data=load_data()

    # check patient is already in DB
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')

    # if not then add new patient
    data[patient.id]=patient.model_dump(exclude=['id'])

    # save data in DB
    save_data(data)

    # send response to the client
    return JSONResponse(status_code=201,content={'message':'patient created'})