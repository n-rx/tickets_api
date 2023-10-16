import json

from uuid import UUID

from flask import Blueprint, request, jsonify, current_app
from flask_cors import CORS
from flask_pydantic import validate

from API.ticket.schemas import (
    GetMultipleTickets,
    TicketBase,
    GetOneTicket,
    TicketQueryBase,
    UpdateStatus,
    TicketCreateBody,
)
from API.ticket_comment.schemas import (
    TicketCommentQueryBase,
    TicketCommentBody,
    GetMultipleTicketComment,
)
from API.ticket.models import Ticket
from API.ticket_comment.models import TicketComment

from utils.logger_tool import log_wrapper
from utils.db.object_serializer import object_serializer


ticket_api = Blueprint("ticket_api", __name__, url_prefix="/api/ticket")
CORS(ticket_api)


@ticket_api.route("/", methods=["GET"])
@log_wrapper
@validate()
def get_multiple(query: TicketQueryBase):
    result = Ticket.get_all(page=query.page, items_per_page=query.items_per_page)
    return GetMultipleTickets(**result), 200


@ticket_api.route("/<uuid:ticket_id>", methods=["GET"])
@log_wrapper
@validate()
def get_one(ticket_id: UUID):
    redis_client = current_app.redis
    cache_key = f"ticket:{ticket_id}"
    result = redis_client.get(cache_key)
    if result:
        result_str = result.decode("utf-8")
        result_dict = json.loads(result_str)
        return GetOneTicket(**result_dict)
    result = Ticket.get_ticket_object(ticket_id)
    if result.status == "closed":
        redis_client.setex(cache_key, 7200, json.dumps(object_serializer(result)))
    return GetOneTicket(**object_serializer(result)), 200


@ticket_api.route("/", methods=["POST"])
@log_wrapper
@validate()
def create(body: TicketCreateBody):
    new_ticket = Ticket.create(
        topic=body.topic,
        description=body.description,
        email=body.email,
    )
    return TicketBase(id=new_ticket.id), 201


@ticket_api.route("/<uuid:ticket_id>/status", methods=["PATCH"])
@log_wrapper
@validate()
def update_status(body: UpdateStatus, ticket_id: UUID):
    upd_ticket = Ticket.update_status(ticket_id, body.status)
    if upd_ticket.status == "closed":
        redis_client = current_app.redis
        cache_key = f"ticket:{ticket_id}"
        redis_client.setex(cache_key, 7200, json.dumps(object_serializer(upd_ticket)))
    return TicketBase(id=upd_ticket.id), 200


@ticket_api.route("/<uuid:ticket_id>/comment", methods=["POST"])
@log_wrapper
@validate()
def create_comment(body: TicketCommentBody, ticket_id: UUID):
    new_comment = TicketComment.create(
        ticket_id=ticket_id, comment=body.comment, email=body.email
    )
    return TicketBase(id=new_comment.id), 201


@ticket_api.route("/<uuid:ticket_id>/comment", methods=["GET"])
@log_wrapper
@validate()
def get_comment(query: TicketCommentQueryBase, ticket_id: UUID):
    result = TicketComment.get_all_by_ticket(
        str(ticket_id), query.page, query.items_per_page
    )
    return GetMultipleTicketComment(**result), 200
