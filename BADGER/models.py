from datetime import datetime
from pydantic import HttpUrl, Json, validator, BaseModel
from sqlmodel import SQLModel, Field, Column, JSON, create_engine, Session, Relationship
from typing import Literal, List, Dict
from uuid import UUID, uuid4

import json
from apscheduler.schedulers.background import BackgroundScheduler
from aiolimiter import AsyncLimiter
from httpx import Request, Response

import logging 

def BadgerItem(BaseModel):
    id: int = Field(default=None, primary_key=True)

class Job(BadgerItem,table=True):
    
    #id: int = Field(default=None, primary_key=True)        
    created_at: datetime = Field(default=datetime.now())
    modified_at: datetime | None = None
    is_deleted: bool = Field(default=False, index=True)
    desc: str | None = None
    #status: Literal["draft","active","inactive"] = Field(index=True) # ? is this needed? sqlmodel issue with Literal (might have to use enum)    
    #schedule: BackgroundScheduler # TODO: after implementing the scheduler's storage
    start_at: datetime # ?
    repeat: bool = False    
    end_date: datetime | None = None    
    last_run: datetime | None = None
    next_run: datetime | None = None        
    
    
    
    
    @validator("start_at")
    def checkstartat(cls,v) -> datetime: # ? how to validate if the date is very close?
        return v

    def create_reqspecs(self,file) -> None:
        # iterate through file
        
        pass
            
    def run_job(self):
        
        # create a batch by pulling rows based on job config
            # id based on count of existing job batches +1
        
        # update scheduler (if not triggered as now)
        
        # update run info (and config?)
        
        pass
    
    def save_requests(self):
        
        pass

    def updateobj(self) -> None:
        # ? what's the relationshp betwen last run and modified at
        # ? does system updating the limits count as an update?
        self.modified_at = datetime.now()
        return None

class BatchConfig(SQLModel,table=True):
    job_id: int = Field(foreign_key="job.id", primary_key=True)    
    batch_size: int    
    timeout: int = Field(default=60)
    retries: int = Field(default=3)
    reschedule: bool = Field(default=True) # ! need to make sure that period retry happens only once
    #asynclimits: List[AsyncLimiter] | None = None # ! should just be the args of AsyncLimiter?
    n_concur: int = Field(default=5)

    @validator("n_concur")
    def checknconcur(cls,v) ->int:
        return 1 if v < 1 else v # ? should it return error?
    
    def create(self) -> None:
        pass

class Batch(BadgerItem,table=True):
    job_id: int = Field(foreign_key="job.id")
    index: int # use default_factory? can we create a general function that takes the object and searches for that object?
    run_at: datetime
    reqspec_idxs: List["RequestSpec"] = Relationship(back_populates="requestspec.id",link_model="BatchReqSpec")# ! might be better to be a link table so we can use relationships          
    
    
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
    
    job_id: int = Field(foreign_key="job.id")
    index: int # use default_factory?
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
    batches: List[Batch] = Relationship(back_populates="")
    
    # ? validate that if params included it's not already present in url?
        
    
    # validate by creating an httpx request
    def create(self) -> None:
        pass
    
    def build_request(self,client) -> Request:
        
        request = client.build_request(**self)
        
        return request
    
    def get_response(self,final_only=False) -> list:
        
        
        pass

        
class BatchReqSpec(SQLModel,table=True):
    batch_id: int = Field(primary_key=True, foreign_key="batch.id")
    reqspec_id: int = Field(primary_key=True, foreign_key="requestspec.id")
    
class BadgerResponse(BadgerItem,table=True):
    
    reqspec_id: int = Field(foreign_key="requestspec.id")    
    job_id: int = Field(foreign_key="job.id")
    reqspec_index: int = Field(foreign_key="requestspec.index")        
    batch_index: int = Field(foreign_key="batch.index")
    index: int = Field(primary_key=True) # use default_factory?
    status_code: int
    delay_applied: int
    sent_at: datetime
    elapsed: float
    headers: dict = Field(sa_column=Column(JSON))
    text: str | None = None
    html: str | None = None
    body_json: dict | None = Field(default=None, sa_column=Column(JSON), alias="json")
    
    def create(self) -> None:
        pass
    
    def next_index(self) -> int:
        
        pass
    # ? update reqspec if success?

class Notification(SQLModel,table=True):
    
    # Notifications are associated with Jobs and Batches and are generated upon the end of every batch run or 
    test: str = Field()
        
    id: int | None = Field(primary_key=True)
    job_id: int = Field(foreign_key="job.id")
    batch_index: int | None = Field(foreign_key="batch.index", default=None)        
    flag: int = Field(index=True)
    code: str
    
    # Types of notifications                        
            # Job finished
            # Job finished (some incompletes)
            # Job could not run on schedule - service was stopped            
            # Batch finished
            # Batch finished (some incompletes)            
            
    def create(self) -> None:
        pass
    
    def describe(cls) -> str:
        
        
        # translate code into a string description interpolated with relevant stats
        
        
        pass
        
    
    # def send_notification() # send to webhook

def next_index(obj,field): # finish typing
    with Session as session:
        return session.select(obj).where(obj.field==)


engine = create_engine(f"sqlite:///badgerdb.db", echo=True)


def build_db():
    SQLModel.metadata.create_all(engine)

if __name__=="__main__":    
    build_db()