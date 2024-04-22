from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class BaseEntity(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DateCreatedUpdateEntity(BaseEntity):
    date_created: Annotated[datetime, Field(title="Date Created")]
    date_updated: Annotated[datetime, Field(title="Date Updated")]
