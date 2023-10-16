from faker import Faker
from uuid import UUID

from API.ticket.models import Ticket
from API.ticket.schemas import TicketStatus

fake = Faker()


def create_tmp_ticket():
    topic = fake.text()
    description = fake.text()
    email = fake.email()
    return Ticket.create(
        topic=topic,
        description=description,
        email=email,
    )


def change_status_tmp_ticket(ticket_id: UUID, status: str):
    return Ticket.update_status(
        ticket_id=ticket_id,
        status=TicketStatus(status),
    )
