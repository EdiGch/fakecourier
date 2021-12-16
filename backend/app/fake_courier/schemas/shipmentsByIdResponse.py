from typing import List, Optional, Dict, Union
from pydantic import BaseModel


class ShipmentsByIdResponse(BaseModel):
    class Config:
        orm_mode = False
        allow_population_by_field_name = True

    ShipmentID: Optional[str]
    Ref1: Optional[str]
    Ref2: Optional[str]
    Events: Optional[Union[List, Dict]] = None


class ShipmentsByIdDataResponse(BaseModel):
    class Config:
        orm_mode = False
        allow_population_by_field_name = True

    data: Optional[Union[List, Dict]]
    status: Optional[int]
    validations: Optional[List]


class ShipmentsEvents(BaseModel):
    class Config:
        orm_mode = False
        allow_population_by_field_name = True

    StatusID: Optional[int]
    StatusName: Optional[str]
    StatusDescription: Optional[str]
