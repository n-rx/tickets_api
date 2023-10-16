import pytest

from faker import Faker
from uuid import UUID

from API.ticket_comment.models import TicketComment
from utils.exceptions import ForbiddenException
from tests.unit.ticket.utils import change_status_tmp_ticket, create_tmp_ticket

fake = Faker()


def test_create_open_ticket_comment(client):
    ticket = create_tmp_ticket()
    comment = fake.text()
    email = fake.email()
    new_ticket_comment = TicketComment.create(
        ticket_id=ticket.id, comment=comment, email=email
    )
    assert new_ticket_comment.comment == comment
    assert new_ticket_comment.email == email


def test_create_answered_ticket_comment(client):
    ticket = create_tmp_ticket()
    answered_ticket = change_status_tmp_ticket(ticket.id, "answered")
    comment = fake.text()
    email = fake.email()
    new_ticket_comment = TicketComment.create(
        ticket_id=answered_ticket.id, comment=comment, email=email
    )
    assert new_ticket_comment.comment == comment
    assert new_ticket_comment.email == email


def test_create_waiting_answer_ticket_comment(client):
    ticket = create_tmp_ticket()
    answer_ticket = change_status_tmp_ticket(ticket.id, "answered")
    waiting_answer_ticket = change_status_tmp_ticket(answer_ticket.id, "waiting_answer")
    comment = fake.text()
    email = fake.email()
    new_ticket_comment = TicketComment.create(
        ticket_id=waiting_answer_ticket.id, comment=comment, email=email
    )
    assert new_ticket_comment.comment == comment
    assert new_ticket_comment.email == email


def test_create_closed_ticket_comment(client):
    with pytest.raises(ForbiddenException):
        ticket = create_tmp_ticket()
        closed_ticket = change_status_tmp_ticket(ticket.id, "closed")
        comment = fake.text()
        email = fake.email()
        new_ticket_comment = TicketComment.create(
            ticket_id=closed_ticket.id, comment=comment, email=email
        )
