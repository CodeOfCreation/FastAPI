from fastapi import FastAPI,Path,Header,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional

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


class Patient_update(BaseModel):
    name:Annotated[Optional[str],Field(description='name of the patient')]
    city:Annotated[Optional[str],Field(description='city of the patient')]
    age:Annotated[Optional[int],Field(gt=0,lt=120,description='age of the patient')]
    gender:Annotated[Optional[str],Field(description='gender of the patient')]
    height:Annotated[Optional[float],Field(gt=0,description='height of the patient')]
    weight:Annotated[Optional[float],Field(gt=0,description='weight of the patient')]
    




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

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: Patient_update):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id):
    data=load_data()
    if Patient_update not in data:
        raise HTTPException(status_code=404,detail='patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient deleted successfully'})
