import uuid

from datetime import datetime
from typing import List
from sqlalchemy.dialects.postgresql import UUID

from utils.db.pagination import sql_paginated
from utils.exceptions import NotFoundException, UnprocessableContent, ForbiddenException

from API import db
from API.ticket.models import Ticket


class TicketComment(db.Model):
    __tablename__ = "ticket_comment"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("ticket.id"), nullable=False
    )
    ticket = db.relationship("Ticket", backref=db.backref("ticket_comment"))
    comment = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, ticket_id: uuid, comment: str, email: str):
        self.ticket_id = ticket_id
        self.comment = comment
        self.email = email

    def __repr__(self):
        return f"<TicketComment {self.id}>"

    @classmethod
    def create(
        cls,
        ticket_id: uuid.UUID,
        comment: str,
        email: str,
    ) -> "TicketComment":
        ticket = Ticket.get_ticket_object(ticket_id)
        if not ticket:
            raise NotFoundException()

        if ticket.status == "closed":
            raise ForbiddenException()

        new_ticket_comment = TicketComment(
            ticket_id=ticket_id, comment=comment, email=email
        )
        db.session.add(new_ticket_comment)
        db.session.commit()
        return new_ticket_comment

    @staticmethod
    def get_all_by_ticket(
        ticket_id: uuid.UUID, page: int, items_per_page: int
    ) -> List["TicketComment"]:
        sql = """

            SELECT
                tc.id,
                tc.comment,
                tc.email,
                tc.created_at
            FROM ticket_comment tc

            WHERE tc.ticket_id = '{ticket_id}'

            ORDER BY tc.created_at DESC

        """.format(
            ticket_id=ticket_id
        )
        return sql_paginated(query=sql, page=page, items_per_page=items_per_page)
