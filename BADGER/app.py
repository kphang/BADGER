#from .models import engine
import functions

import uvicorn
from fastapi import FastAPI, File, Form, UploadFile, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import pandas as pd
from itables import to_html_datatable

import logging
import sys



app = FastAPI(title="BADGER")
app.mount("/static", StaticFiles(directory="BADGER/static"), name="static")
templates = Jinja2Templates(directory="BADGER/templates")

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s]: %(asctime)s - %(message)s"
)


@app.get("/", response_class=HTMLResponse)
async def index(request:Request):
    # homepage shows notifications and status of active jobs
    # use index.html
    
    testdf1 = pd.DataFrame({"a":[1,2],"b":[3,4]})#.to_html()
    testdf2 = pd.DataFrame({"a":[3,1],"b":[4,1]})
    test = to_html_datatable(testdf1)
    test2 = to_html_datatable(testdf2)
    return templates.TemplateResponse("index.html", {"request":request, "test":test, "test2":test2})

@app.get("/jobs", response_class=HTMLResponse)
async def jobs(request:Request):
    
    
    return templates.TemplateResponse("jobs.html", {"request":request})

@app.get("/job/{job_id}", response_class=HTMLResponse)
async def job_details(request:Request,job_id:int):
    
    
    return templates.TemplateResponse("job.html", {"request":request, "job_id":job_id})

@app.get("/job/{job_id}/batch/{batch_index}", response_class=HTMLResponse)
async def batch_details(request:Request,job_id:int,batch_index:int):
    
    
    return templates.TemplateResponse("batch.html", 
                                      {"request":request, "job_id":job_id, "batch_index":batch_index})


@app.get("/job/{job_id}/req-spec/{reqspec_index}")
async def req_spec_details(request:Request,job_id:int,reqspec_index:int):
    
    
    return templates.TemplateResponse("reqspec.html", 
                                      {"request":request, "job_id":job_id, "reqspec_index":reqspec_index})


@app.get("/create-job", response_class=HTMLResponse)
@app.post("/create-job", response_class=HTMLResponse)
async def create_job(request:Request):
    
    if request.method=="GET":
        return templates.TemplateResponse("create-job.html", {"request":request})    
    elif request.method=="POST":
        
        pass
    

if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
    # use custom port? 8_69