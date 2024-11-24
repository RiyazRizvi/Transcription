from fastapi import FastAPI,UploadFile,File
import shutil
from pathlib import Path

app=FastAPI()

@app.post('/UploadFile/')
async def file(file:UploadFile=File(...)):
    #for create temporar  file path
    video_path=f"temp_{file.filename}"

    #for saving file temporary
    with open(video_path,'wb') as buffer:
        shutil.copyfileobj(file.file,buffer)
        

    


