import uuid

from typing import List
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID

from API import db
from utils.db.pagination import sql_paginated
from utils.exceptions import UnprocessableContent, NotFoundException


class Ticket(db.Model):
    __tablename__ = "ticket"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    status = db.Column(
        db.Enum("open", "answered", "waiting_answer", "closed", name="ticket_status"),
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )

    def __init__(self, topic: str, description: str, email: str, status: int):
        self.topic = topic
        self.description = description
        self.email = email
        self.status = status

    def __repr__(self):
        return f"<Ticket {self.id}>"

    @classmethod
    def get_ticket_object(cls, ticket_id: uuid.UUID) -> "Ticket":
        ticket = cls.query.filter_by(id=ticket_id).first()
        if not ticket:
            raise NotFoundException
        return ticket

    @staticmethod
    def get_all(page: int, items_per_page: int) -> List["Ticket"]:
        sql = """

            SELECT 
                t.id::text,
                t.topic,
                t.status
            FROM ticket t

            ORDER by t.created_at DESC

        """

        return sql_paginated(
            query=sql,
            page=page,
            items_per_page=items_per_page,
        )

    @classmethod
    def create(
        cls,
        topic: str,
        description: str,
        email: str,
    ) -> "Ticket":
        new_ticket = cls(
            topic=topic, description=description, email=email, status="open"
        )
        db.session.add(new_ticket)
        db.session.commit()
        return new_ticket

    @classmethod
    def update_status(cls, ticket_id: uuid.UUID, status: str) -> "Ticket":
        allowed_to_change = {
            "open": {"answered", "closed"},
            "answered": {"waiting_answer", "closed"},
            "waiting_answer": {"answered"},
            "closed": {},
        }

        ticket = cls.get_ticket_object(ticket_id)
        if not ticket:
            raise NotFoundException()
        if status.value not in allowed_to_change.get(ticket.status):
            raise UnprocessableContent()

        ticket.status = status.value
        db.session.merge(ticket)
        db.session.commit()
        return ticket
