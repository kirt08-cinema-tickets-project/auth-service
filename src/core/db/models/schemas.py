import datetime 
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

from src.core.db.models.utils import Roles, Type

class UserRequest(BaseModel):
    phone : Annotated[str | None, Field(default=None)]
    email : Annotated[str | None, Field(default=None)]

class UserResponse(UserRequest):
    model_config = ConfigDict(
        from_attributes=True
    )

    id : int
    is_phone_verified : bool
    is_email_verified : bool
    role : Roles

    created_at : datetime.datetime
    updated_at : datetime.datetime

class PendingContactChangesRequest(BaseModel):
    type : Type
    value : str
    codeHash : str
    expiresAt : int

class PendingContactChangesResponse(PendingContactChangesRequest):
    model_config = ConfigDict(
        from_attributes=True
    )
    id : int
    account_id : int
    # account : UserResponse
    created_at : datetime.datetime
    updated_at : datetime.datetime