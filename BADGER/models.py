from datetime import datetime
from pydantic import HttpUrl, Json, validator
from sqlmodel import SQLModel, Field, Column, JSON, create_engine, Session, Relationship, ForeignKeyConstraint, Index
from typing import List, Optional
from enum import Enum

import json
from apscheduler.schedulers.background import BackgroundScheduler
from aiolimiter import AsyncLimiter
from httpx import Request, Response

import logging 



class ValidStatuses:
    # SQLModel causes Literal to throw an error, requiring the use of enums
    class JobStatus(str, Enum):
        ACTIVE = "active"
        COMPLETED = "completed"
        CANCELLED = "cancelled"

    class ReqSpecStatus(str, Enum):
        INCOMPLETE = "incomplete"
        COMPLETE = "complete"
        FAILED = "failed"
        RESCHEDULED = "rescheduled"


class Job(SQLModel,table=True):
    
    id: Optional[int] = Field(default=None, primary_key=True)    
    created_at: datetime = Field(default=datetime.now())
    modified_at: Optional[datetime] = None # ? is this useful
    is_deleted: bool = Field(default=False, index=True)
    desc: Optional[str] = None
    status: ValidStatuses.JobStatus = Field(index=True)
    batchconfig: "BatchConfig" = Relationship(back_populates="job")
    #schedule: BackgroundScheduler # TODO: after implementing the scheduler's storage
    start_at: datetime # ? does this exist on the scheduler
    repeat: bool = False    
    end_at: Optional[datetime] = None # ? might not be needed - or only if repeated    
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    reqspecs: Optional["RequestSpec"] = Relationship(back_populates="job")     
    batches: Optional["Batch"] = Relationship(back_populates="job")
    
    
    
    
    
    @validator("start_at")
    def checkstartat(cls,v) -> datetime: # ? how to validate if the date is very close?
        return v

    def __init__(self):
        
        
        pass

    def estimate_enddate(self):
        # estimate end date (none if repeat (without an end date))

        pass

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
    # Need to figure out how it gets overwritten based on experience
    # Need to allow for both experimental and fixed (for cases where rates might be known)
    # Need to handle inputting multiple rates

    job_id: int = Field(foreign_key="job.id", primary_key=True)
    job: Job = Relationship(back_populates="batchconfig")    
    batch_size: int    
    timeout: int = 60
    retries: int = 3
    reschedule: bool = Field(default=True, description="Whether failed requests should be tried again on a later date in addition to regular retries")
    #asynclimits: # TODO: implment after tenacity
    n_concur: int = 5

    @validator("n_concur")
    def checknconcur(cls,v) ->int:
        return 1 if v < 1 else v # ? should it return error?
    
    def create(self) -> None:
        pass

class BatchReqSpec(SQLModel,table=True):
    batch_id: int = Field(primary_key=True, foreign_key="batch.id")
    reqspec_id: int = Field(primary_key=True, foreign_key="requestspec.id")


class Batch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: int = Field(foreign_key="job.id")
    job: Job = Relationship(back_populates="batches")
    index: int # use default_factory? can we create a general function that takes the object and searches for that object?
    run_at: datetime
    reqspecs: List["RequestSpec"] = Relationship(back_populates="batches",link_model=BatchReqSpec)
    Index(
        "job_id", "index", unique=True
    )
    
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
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: int = Field(foreign_key="job.id")
    job: Job = Relationship(back_populates="reqspecs")
    index: int # use default_factory?
    method: str # enumerate
    url: HttpUrl    
    params: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    data: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    headers: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    # TODO: files
    # TODO: cookies
    # TODO: auth
    # TODO: proxies
    # TODO: content        
    status: ValidStatuses.ReqSpecStatus = Field(index=True)
    periodRetried: bool | None = None
    batches: List[Batch] = Relationship(back_populates="reqspecs", link_model=BatchReqSpec)
    responses: List["BadgerResponse"] = Relationship(back_populates="reqspec")
    Index(
        "job_id", "index", unique=True
    )
    
    # ? validate that if params included it's not already present in url?
    # TODO: need to make sure that period retry happens only once        
    
    # validate by creating an httpx request
    def create(self) -> None:
        pass
    
    def build_request(self,client) -> Request:
        
        request = client.build_request(**self)
        
        return request
    
    def get_response(self,final_only=False) -> list:
        
        
        pass

        
    
    
class BadgerResponse(SQLModel,table=True):

    id: int | None = Field(default=None, primary_key=True)    
    reqspec_id: int = Field(foreign_key="requestspec.id")
    reqspec: RequestSpec = Relationship(back_populates="responses")    
    index: int # use default_factory?
    status_code: int
    delay_applied: int
    sent_at: datetime
    elapsed: float
    headers: dict = Field(sa_column=Column(JSON))
    text: Optional[str] = None
    html: Optional[str] = None
    body_json: Optional[dict] = Field(default=None, sa_column=Column(JSON), alias="json")
    Index(
        "reqspec_id", "index", unique=True
    )
    
    def create(self) -> None:
        pass
    
    # def next_index(self) -> int:
        
    #     pass
    # # ? update reqspec if success?

class Notification(SQLModel,table=True):
          
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: int = Field(foreign_key="job.id")    
    batch_id: int = Field(foreign_key="batch.id")    
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

# def next_index(obj,field): # finish typing
#     with Session as session:
#         return session.select(obj).where(obj.field==)


engine = create_engine(f"sqlite:///badgerdb.db", echo=True)


def build_db():
    SQLModel.metadata.create_all(engine)

if __name__=="__main__":    
    build_db()