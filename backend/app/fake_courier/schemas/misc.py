from datetime import datetime
from typing import Optional, Union, Any

from pydantic import BaseModel


class DateQueryParamSchema(BaseModel):
    date: Optional[Union[datetime, Any]]
