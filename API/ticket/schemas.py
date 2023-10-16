from enum import Enum
from uuid import UUID
from typing import List
from datetime import datetime
from pydantic import BaseModel, EmailStr

from utils.schemas.base_schemas import QueryBase


class TicketStatus(str, Enum):
    open = "open"
    answered = "answered"
    waiting_answer = "waiting_answer"
    closed = "closed"


class TicketQueryBase(QueryBase):
    pass


class TicketBase(BaseModel):
    id: UUID


class TicketBody(BaseModel):
    topic: str
    description: str
    email: EmailStr
    status: TicketStatus


class TicketCreateBody(BaseModel):
    topic: str
    description: str
    email: EmailStr


class TicketExtended(TicketBody):
    created_at: datetime
    updated_at: datetime


class GetOneTicket(TicketBody):
    id: UUID
    created_at: str
    updated_at: str


class GetTicket(TicketExtended):
    id: UUID


class UpdateStatus(BaseModel):
    status: TicketStatus


class PartMultipleTickets(BaseModel):
    id: UUID
    topic: str
    status: TicketStatus


class GetMultipleTickets(BaseModel):
    items: List[PartMultipleTickets]
    page: int
    items_per_page: int
    total_pages: int
