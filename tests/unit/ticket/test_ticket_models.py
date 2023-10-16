import pytest

from faker import Faker
from uuid import UUID

from API.ticket.models import Ticket
from API.ticket.schemas import TicketStatus
from utils.exceptions import UnprocessableContent

from tests.unit.ticket.utils import (
    create_tmp_ticket,
    change_status_tmp_ticket,
)

fake = Faker()


def test_create_ticket(client):
    topic = fake.text()
    description = fake.text()
    email = fake.email()
    new_ticket = Ticket.create(
        topic=topic,
        description=description,
        email=email,
    )
    assert new_ticket.topic == topic
    assert new_ticket.description == description
    assert new_ticket.email == email
    assert new_ticket.status == "open"


def test_get_ticket(client):
    topic = fake.text()
    description = fake.text()
    email = fake.email()
    new_ticket = Ticket.create(
        topic=topic,
        description=description,
        email=email,
    )
    ticket = Ticket.get_ticket_object(new_ticket.id)
    assert ticket.topic == topic
    assert ticket.description == description
    assert ticket.email == email


# Change status. Success cases


def test_update_status_open_answered(client):
    # open -> answered
    ticket = create_tmp_ticket()
    upd_ticket = Ticket.update_status(
        ticket_id=ticket.id,
        status=TicketStatus("answered"),
    )
    assert upd_ticket.status == "answered"


def test_update_status_open_closed(client):
    # open -> closed
    ticket = create_tmp_ticket()
    upd_ticket = Ticket.update_status(
        ticket_id=ticket.id,
        status=TicketStatus("closed"),
    )
    assert upd_ticket.status == "closed"


def test_update_status_answered_waiting_answer(client):
    # answered -> waiting_answer
    ticket = create_tmp_ticket()
    answered_ticket = change_status_tmp_ticket(ticket.id, "answered")
    upd_ticket = Ticket.update_status(
        ticket_id=answered_ticket.id,
        status=TicketStatus("waiting_answer"),
    )
    assert upd_ticket.status == "waiting_answer"


def test_update_status_answered_closed(client):
    # answered -> closed
    ticket = create_tmp_ticket()
    answered_ticket = change_status_tmp_ticket(ticket.id, "answered")
    upd_ticket = Ticket.update_status(
        ticket_id=answered_ticket.id,
        status=TicketStatus("closed"),
    )
    assert upd_ticket.status == "closed"


def test_update_status_waiting_answer_answered(client):
    # waiting_answer -> answered
    ticket = create_tmp_ticket()
    answer_ticket = change_status_tmp_ticket(ticket.id, "answered")
    waiting_answer_ticket = change_status_tmp_ticket(answer_ticket.id, "waiting_answer")
    upd_ticket = Ticket.update_status(
        ticket_id=waiting_answer_ticket.id,
        status=TicketStatus("answered"),
    )
    assert upd_ticket.status == "answered"


# Change status. Fail cases


def test_update_status_open_waiting_answer(client):
    # open -> waiting_answer
    with pytest.raises(UnprocessableContent):
        ticket = create_tmp_ticket()
        upd_ticket = Ticket.update_status(
            ticket_id=ticket.id, status=TicketStatus("waiting_answer")
        )


def test_update_status_answered_open(client):
    # answered -> open
    with pytest.raises(UnprocessableContent):
        ticket = create_tmp_ticket()
        answered_ticket = change_status_tmp_ticket(ticket.id, "answered")
        upd_ticket = Ticket.update_status(
            ticket_id=answered_ticket.id, status=TicketStatus("open")
        )


def test_update_status_waiting_answer_open(client):
    # waiting_answer -> open
    with pytest.raises(UnprocessableContent):
        ticket = create_tmp_ticket()
        answer_ticket = change_status_tmp_ticket(ticket.id, "answered")
        waiting_answer_ticket = change_status_tmp_ticket(
            answer_ticket.id, "waiting_answer"
        )
        upd_ticket = Ticket.update_status(
            ticket_id=waiting_answer_ticket.id, status=TicketStatus("open")
        )


def test_update_status_waiting_answer_closed(client):
    # waiting_answer -> closed
    with pytest.raises(UnprocessableContent):
        ticket = create_tmp_ticket()
        answer_ticket = change_status_tmp_ticket(ticket.id, "answered")
        waiting_answer_ticket = change_status_tmp_ticket(
            answer_ticket.id, "waiting_answer"
        )
        upd_ticket = Ticket.update_status(
            ticket_id=waiting_answer_ticket.id, status=TicketStatus("closed")
        )


def test_update_status_closed_open(client):
    # closed -> open
    with pytest.raises(UnprocessableContent):
        ticket = create_tmp_ticket()
        closed_ticket = change_status_tmp_ticket(ticket.id, "closed")
        upd_ticket = Ticket.update_status(
            ticket_id=closed_ticket.id, status=TicketStatus("open")
        )


def test_update_status_closed_waiting_answer(client):
    # closed -> waiting_answer
    with pytest.raises(UnprocessableContent):
        ticket = create_tmp_ticket()
        closed_ticket = change_status_tmp_ticket(ticket.id, "closed")
        upd_ticket = Ticket.update_status(
            ticket_id=closed_ticket.id, status=TicketStatus("waiting_answer")
        )


def test_update_status_closed_answered(client):
    # closed -> answered
    with pytest.raises(UnprocessableContent):
        ticket = create_tmp_ticket()
        closed_ticket = change_status_tmp_ticket(ticket.id, "closed")
        upd_ticket = Ticket.update_status(
            ticket_id=closed_ticket.id, status=TicketStatus("answered")
        )
