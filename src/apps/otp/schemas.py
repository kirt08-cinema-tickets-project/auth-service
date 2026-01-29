from fastapi import Query
from pydantic import BaseModel

class OtpRequest(BaseModel):
    identifier : str
    type : str