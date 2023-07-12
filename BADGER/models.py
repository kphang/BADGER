from datetime import datetime
from pydantic import HttpUrl, Json, validator
from sqlmodel import SQLModel, Field, Column, JSON, create_engine
from typing import Literal, List, Dict
from uuid import UUID, uuid4

import json
from apscheduler.schedulers.background import BackgroundScheduler
from aiolimiter import AsyncLimiter
from httpx import Request, Response

import logging 


class BadgerObj(SQLModel):
    
    id: int = Field(default=None, primary_key=True)        
    created_at: datetime = Field(default=datetime.now())
    modified_at: datetime | None = None
    is_deleted: bool = Field(default=False, index=True) # ! how to handle deleted items and archived items
            
    def updateobj(self) -> None:
        self.modified_at = datetime.now()
        return None

    # ? what's the relationshp betwen last run and modified at
    # ? does system updating the limits count as an update?
    # ! this might not be particularly useful model since only jobs really get modified
        # only jobs get deleted directly (everything else is cascaded from the job)

class Job(BadgerObj,table=True):
    
    last_run: datetime | None = None
    next_run: datetime | None = None
    desc: str | None = None
    #status: Literal["draft","active","inactive"] = Field(index=True) # ! sqlmodel issue with Literal (might have to use enum)
    # batch config
    batch_size: int
    #asynclimits: List[AsyncLimiter] | None = None # ! should just be the args of AsyncLimiter?
    n_concur: int = Field(default=5)
    timeout: int = Field(default=60)
    retries: int = Field(default=3)
    reschedule: bool = Field(default=True) # ! need to make sure that period retry happens only once
    # schedule config
    #schedule: BackgroundScheduler # ! schedule items might be better as its own class and related
    start_at: datetime # ?
    repeat: bool = False
    end_date: datetime | None = None
    
    @validator("n_concur")
    def checknconcur(cls,v) ->int:
        return 1 if v < 1 else v # ? should it return error?
    
    @validator("start_at")
    def checkstartat(cls,v) -> datetime: # ? how to validate if the date is very close?
        return v
            
    def run_job(self):
        
        # create a batch by pulling rows based on job config
            # id based on count of existing job batches +1
        
        # update scheduler (if not triggered as now)
        
        # update run info (and config?)
        
        pass
    
    def save_requests(self):
        
        pass


class Batch(BadgerObj,table=True):
    job_id: int = Field(index=True)
    index: int = Field(index=True)
    run_at: datetime
    reqspecs: List[int]           
    
    
    def build_requests() -> list:
        # criteria to pull reqspecs
            # incomplete
        
        # build_request method
        
        pass

    def learn_limits(cls) -> dict:
        # look for max successfully concurrent at any given time
        # identify a safe starting rate
        # return dict of kwargs from the job config
        
                
        
        pass        
                
    def run_batch(cls):        
        
        # receive BatchConfig and apply            
        
        # create client
            # timeout and limits (maxConcur) are provided by Job so they can be added here
            
        # iterate build requests
            
        
        # update runAt
        
        # run async requests (create responses)
            
        # update requests with status                
            # post retry store settings to pass to add to response
        
        
        # save data
        
        # update job to save limits learnt (overwrite settings? store separately and use if exists?)

        
        pass
    
    
class RequestSpec(SQLModel,table=True):
    
    job_id: int = Field(primary_key=True)
    index: int = Field(primary_key=True)
    method: str
    url: HttpUrl    
    params: dict | None = Field(default=None, sa_column=Column(JSON))
    data: dict | None = Field(default=None, sa_column=Column(JSON))
    headers: dict | None = Field(default=None, sa_column=Column(JSON))
    # TODO: files
    # TODO: cookies
    # TODO: auth
    # TODO: proxies
    # TODO: content        
    #status: Literal["Waiting","Retrying Later","Failed","Complete"]
    periodRetried: bool = False
    
    # ? validate that if params included it's not already present in url?
        
    
    # validate by creating an httpx request
    
    
    def build_request(self,client) -> Request:
        
        request = client.build_request(**self)
        
        return request
    
    
    
class BadgerResponse(SQLModel,table=True):
    
    job_id: int = Field(primary_key=True)    
    reqspec_index: int = Field(primary_key=True)    
    index: int = Field(primary_key=True)    
    status_code: int
    delay_applied: int
    sent_at: datetime
    elapsed: float
    headers: dict = Field(sa_column=Column(JSON))
    text: str | None = None
    html: str | None = None
    json: dict | None = Field(default=None, sa_column=Column(JSON))
    
    
    # ? update reqspec if success?

class Notification(BadgerObj,table=True):
    
    # Notifications are associated with Jobs and Batches and are generated upon the end of every batch run or 
    
        
    
    #type: Literal["Job","Batch"]
    relatedId: int = Field(index=True)
    code: str = Field(index=True)
    
    
    def describe(cls) -> str:
        
        # translate code into a string description interpolated with relevant stats
        # Types of notifications                        
            # Batch success        
            # Batch success (some incompletes)            
            # Job completion
            # Job completion (some incompletes)
            # Job could not run on schedule - service was stopped
        
        pass
        
    
    # def send_notification() # send to webhook

engine = create_engine(f"sqlite:///badgerdb.db", echo=True)

def build_db():
    SQLModel.metadata.create_all(engine)

if __name__=="__main__":    
    build_db()