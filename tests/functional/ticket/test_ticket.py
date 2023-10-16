from faker import Faker

from API.ticket.models import Ticket
from tests.unit.ticket.utils import create_tmp_ticket, change_status_tmp_ticket

fake = Faker()


def test_create_ticket(client):
    topic = fake.text()
    description = fake.text()
    email = fake.email()
    res = client.post(
        "/api/ticket/",
        json={"topic": topic, "description": description, "email": email},
    )
    assert res.status_code == 201
    assert res.json.get("id") is not None

    created_ticket = Ticket.get_ticket_object(res.json.get("id"))

    assert created_ticket.topic == topic
    assert created_ticket.description == description
    assert created_ticket.email == email
    assert created_ticket.status == "open"


def test_get_ticket(client):
    topic = fake.text()
    description = fake.text()
    email = fake.email()
    create_ticket = client.post(
        "/api/ticket/",
        json={"topic": topic, "description": description, "email": email},
    )
    get_ticket = client.get(f"/api/ticket/{create_ticket.json.get('id')}")
    assert get_ticket.status_code == 200


def test_update_status_open_answered(client):
    # open -> answered
    ticket = create_tmp_ticket()
    res = client.patch(
        f"/api/ticket/{ticket.id}/status",
        json={"status": "answered"},
    )
    assert res.status_code == 200
    assert res.json.get("id") == str(ticket.id)
    changed_ticket = Ticket.get_ticket_object(res.json.get("id"))
    assert changed_ticket.status == "answered"


def test_update_status_open_waiting_answer(client):
    # open -> waiting_answer
    ticket = create_tmp_ticket()
    res = client.patch(
        f"/api/ticket/{ticket.id}/status",
        json={"status": "waiting_answer"},
    )
    assert res.status_code == 422


def test_update_status_open_closed(client):
    # open -> closed
    ticket = create_tmp_ticket()
    res = client.patch(
        f"/api/ticket/{ticket.id}/status",
        json={"status": "closed"},
    )
    assert res.status_code == 200
    assert res.json.get("id") == str(ticket.id)
    changed_ticket = Ticket.get_ticket_object(res.json.get("id"))
    assert changed_ticket.status == "closed"


def test_update_status_answered_open(client):
    # answered -> open
    ticket = create_tmp_ticket()
    answer_ticket = change_status_tmp_ticket(ticket.id, "answered")
    res = client.patch(
        f"/api/ticket/{answer_ticket.id}/status",
        json={"status": "open"},
    )
    assert res.status_code == 422


def test_update_status_answered_waiting_answer(client):
    # answered -> waiting_answer
    ticket = create_tmp_ticket()
    anwered_ticket = change_status_tmp_ticket(ticket.id, "answered")
    res = client.patch(
        f"/api/ticket/{anwered_ticket.id}/status",
        json={"status": "waiting_answer"},
    )
    assert res.status_code == 200
    assert res.json.get("id") == str(anwered_ticket.id)
    changed_ticket = Ticket.get_ticket_object(res.json.get("id"))
    assert changed_ticket.status == "waiting_answer"


def test_update_status_answered_closed(client):
    # answered -> closed
    ticket = create_tmp_ticket()
    anwered_ticket = change_status_tmp_ticket(ticket.id, "answered")
    res = client.patch(
        f"/api/ticket/{anwered_ticket.id}/status",
        json={"status": "closed"},
    )
    assert res.status_code == 200
    assert res.json.get("id") == str(anwered_ticket.id)
    changed_ticket = Ticket.get_ticket_object(res.json.get("id"))
    assert changed_ticket.status == "closed"


def test_update_status_waiting_answer_open(client):
    # waiting_answer -> open
    ticket = create_tmp_ticket()
    answer_ticket = change_status_tmp_ticket(ticket.id, "answered")
    waiting_answer_ticket = change_status_tmp_ticket(answer_ticket.id, "waiting_answer")
    res = client.patch(
        f"/api/ticket/{waiting_answer_ticket.id}/status",
        json={"status": "open"},
    )
    assert res.status_code == 422


def test_update_status_waiting_answer_answered(client):
    # waiting_answer -> answered
    ticket = create_tmp_ticket()
    answer_ticket = change_status_tmp_ticket(ticket.id, "answered")
    waiting_answer_ticket = change_status_tmp_ticket(answer_ticket.id, "waiting_answer")
    res = client.patch(
        f"/api/ticket/{waiting_answer_ticket.id}/status",
        json={"status": "answered"},
    )
    assert res.status_code == 200
    assert res.json.get("id") == str(answer_ticket.id)
    changed_ticket = Ticket.get_ticket_object(res.json.get("id"))
    assert changed_ticket.status == "answered"


def test_update_status_waiting_answer_closed(client):
    # waiting_answer -> closed
    ticket = create_tmp_ticket()
    answer_ticket = change_status_tmp_ticket(ticket.id, "answered")
    waiting_answer_ticket = change_status_tmp_ticket(answer_ticket.id, "waiting_answer")
    res = client.patch(
        f"/api/ticket/{waiting_answer_ticket.id}/status",
        json={"status": "closed"},
    )
    assert res.status_code == 422


def test_update_status_closed_open(client):
    # closed -> open
    ticket = create_tmp_ticket()
    closed_ticket = change_status_tmp_ticket(ticket.id, "closed")
    res = client.patch(
        f"/api/ticket/{closed_ticket.id}/status",
        json={"status": "open"},
    )
    assert res.status_code == 422


def test_update_status_closed_answered(client):
    # closed -> answered
    ticket = create_tmp_ticket()
    closed_ticket = change_status_tmp_ticket(ticket.id, "closed")
    res = client.patch(
        f"/api/ticket/{closed_ticket.id}/status",
        json={"status": "answered"},
    )
    assert res.status_code == 422


def test_update_status_closed_waiting_answer(client):
    # closed -> waiting_answer
    ticket = create_tmp_ticket()
    closed_ticket = change_status_tmp_ticket(ticket.id, "closed")
    res = client.patch(
        f"/api/ticket/{closed_ticket.id}/status",
        json={"status": "waiting_answer"},
    )
    assert res.status_code == 422


def test_update_status_invalid_value(client):
    topic = fake.text()
    description = fake.text()
    email = fake.email()
    created_ticket = client.post(
        "/api/ticket/",
        json={"topic": topic, "description": description, "email": email},
    ).json.get("id")

    res = client.patch(
        f"/api/ticket/{created_ticket}/status",
        json={"status": fake.text()},
    )
    assert res.status_code == 400
