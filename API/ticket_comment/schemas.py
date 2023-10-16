from typing import Optional, List
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from utils.schemas.base_schemas import QueryBase


class TicketCommentQueryBase(QueryBase):
    pass


class TicketCommentBase(BaseModel):
    id: UUID


class TicketCommentBody(BaseModel):
    comment: str
    email: str


class TicketCommentExtended(TicketCommentBody):
    created_at: datetime


class GetTicketComment(TicketCommentExtended):
    id: UUID


class GetMultipleTicketComment(BaseModel):
    items: list[GetTicketComment]
    page: int
    items_per_page: int
    total_pages: int
