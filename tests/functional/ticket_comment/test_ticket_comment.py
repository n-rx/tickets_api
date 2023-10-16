from faker import Faker

from API.ticket_comment.models import TicketComment
from tests.unit.ticket.utils import create_tmp_ticket, change_status_tmp_ticket
from utils.exceptions import ForbiddenException

fake = Faker()


def test_create_open_ticket_comment(client):
    ticket = create_tmp_ticket()
    comment = fake.text()
    email = fake.email()
    res = client.post(
        f"/api/ticket/{ticket.id}/comment",
        json={"comment": comment, "email": email},
    )
    assert res.status_code == 201
    assert res.json.get("id") is not None


def test_get_ticket_comment(client):
    ticket = create_tmp_ticket()
    comment = fake.text()
    email = fake.email()
    create_comment = client.post(
        f"/api/ticket/{ticket.id}/comment",
        json={"comment": comment, "email": email},
    )
    get_comment = client.get(f"/api/ticket/{ticket.id}/comment")
    comment_items = get_comment.json.get("items")
    assert get_comment.status_code == 200
    assert comment_items[0].get("id") == create_comment.json.get("id")


def test_create_answered_ticket_comment(client):
    ticket = create_tmp_ticket()
    answered_ticket = change_status_tmp_ticket(ticket.id, "answered")
    comment = fake.text()
    email = fake.email()
    res = client.post(
        f"/api/ticket/{answered_ticket.id}/comment",
        json={"comment": comment, "email": email},
    )
    assert res.status_code == 201
    assert res.json.get("id") is not None


def test_create_waiting_answer_ticket_comment(client):
    ticket = create_tmp_ticket()
    answer_ticket = change_status_tmp_ticket(ticket.id, "answered")
    waiting_answer_ticket = change_status_tmp_ticket(answer_ticket.id, "waiting_answer")
    comment = fake.text()
    email = fake.email()
    res = client.post(
        f"/api/ticket/{waiting_answer_ticket.id}/comment",
        json={"comment": comment, "email": email},
    )
    assert res.status_code == 201
    assert res.json.get("id") is not None


def test_create_closed_ticket_comment(client):
    ticket = create_tmp_ticket()
    closed_ticket = change_status_tmp_ticket(ticket.id, "closed")
    comment = fake.text()
    email = fake.email()
    res = client.post(
        f"/api/ticket/{closed_ticket.id}/comment",
        json={"comment": comment, "email": email},
    )
    assert res.status_code == 403
