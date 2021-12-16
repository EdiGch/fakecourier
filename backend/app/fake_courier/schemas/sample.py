from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SampleModelSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    id: Optional[UUID]
    name: str
