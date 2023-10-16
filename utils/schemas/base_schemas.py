from typing import Optional
from pydantic import BaseModel


class QueryBase(BaseModel):
    page: Optional[int] = 1
    items_per_page: Optional[int] = 10
