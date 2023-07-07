from datetime import datetime
from pydantic import BaseModel, validators, dataclasses
from typing import Literal
from uuid import UUID, uuid4

import json
from apscheduler.schedulers.background import BackgroundScheduler
from aiolimiter import AsyncLimiter
from httpx import Request, Response

class BadgerObj(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    id: UUID = uuid4()
    createdAt: datetime = datetime.now()
    modifiedAt: datetime | None
    isDeleted: bool = False # ! how to handle deleted items and archived items
    
    def update_moddat(self) -> None:
        self.modifiedAt = datetime.now()
        return None

# class RateLimit(BaseModel):    
#     amount: int # amount for rate # ! 
#     period: Literal["second","minute","hour","day","month","year"] # period for rate    

class BatchConfig(BaseModel):
    """The BatchConfig is set on job creation and defines the rules by which batches
    are generated and its requests are run.
    """            
    batchSize: int | None = None
    asynclimits: tuple[AsyncLimiter,...] | None = None # ! use limits library instead?
    maxConcur: int = 5    
    timeout: int = 60
    maxRetries: int = 3
    reschedule: bool = True # ! need to make sure that period retry happens only once
    

    @validators("maxConcur")
    def checkmaxconcur(cls,v) ->int:
        return 1 if v < 1 else v # ? should it return error?
        

class Job(BadgerObj):
    
    lastRunAt: datetime
    nextRunAt: datetime
    title: str | None
    status: Literal["draft","active","inactive"] # TODO    
    batchConfig: BatchConfig
    schedule: BackgroundScheduler # ! APScheduler
    scheduleStartDate: datetime # ?
    repeat: bool = False
    endDate: datetime | None = None
    
    @validators("startDate")
    def checkstartdate(cls,v) -> datetime: # ? how to validate if the date is very close?
        return 
            
    def run_job(cls):
        
        # create a batch by pulling rows based on job config
        
        # update scheduler (if not triggered as now)
        
        # update run info (and config?)
        
        pass
    
    def save_requests(cls):
    
class Batch(BadgerObj):
    runAt: datetime
    jobId: UUID
    requests = tuple[Request, ...]
                
    def run_batch(cls):        
        
        # receive BatchConfig and apply
        
        # update runAt
        
        # run async requests
        
        # update requests with status                
        
        # save data
        
        # update BatchConfig to save limits learnt (overwrite settings? store separately and use if exists?)
        
        pass
    
        # ! Should Batch be a list of objects associated to the Job?
            # wouldn't need a uuid, it's just indexed by tuple of job batches?
                # but then how does it get stored in sqlite?

class APIRequest(BadgerObj):
    
    jobId: UUID
    index: int
    request: Request
    response: Response | None
    attemptnotes: dict | None
    status: Literal["Waiting","Retrying Later","Failed","Complete"]
    
    
class BadgerRequest(BadgerObj,Request):
    
    jobId: UUID
    index: int
    request: Request    
    attemptNotes: dict | None
    status: Literal["Waiting","Retrying Later","Failed","Complete"]
    periodRetried: bool = False
    
class BadgerResponse(BadgerObj,Response):
    
    requestId: UUID    
    response: Response    
    attemptnotes: dict | None
    status: Literal["Waiting","Retrying Later","Failed","Complete"]


class Notification(BadgerObj):
    
    # Notifications are associated with Jobs and Batches and are generated upon the end of every batch run or 
    
        
    
    type: Literal["Job","Batch"]
    relatedId: UUID
    code: str
    
    
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
    