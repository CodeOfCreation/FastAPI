from fastapi import FastAPI,Path,Header,HTTPException,Query
import json

app=FastAPI()

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