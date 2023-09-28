from typing import Literal
from pydantic import BaseModel

class Test(BaseModel):
    t: Literal["a","b"]
    
    