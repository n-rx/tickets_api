"""
The object_serializer function serializes a SQLAlchemy model into a dictionary.

This function takes an SQLAlchemy model object as input and converts it into a
dictionary, where keys represent column names, and values are the corresponding
values in the model. The serialization process includes converting UUID objects to strings
and datetime objects to ISO 8601 formatted strings.

Parameters:
    - model: An SQLAlchemy model object to be serialized.

Returns:
    dict: A dictionary containing the serialized data of the input model.
"""

from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import class_mapper


def object_serializer(model):
    """
    Serializes an SQLAlchemy model into a dictionary.

    Args:
        model: An SQLAlchemy model object to be serialized.

    Returns:
        dict: A dictionary with column names as keys and serialized values.
    """
    if not model:
        return None

    serialized = {}
    mapper = class_mapper(model.__class__)

    for column in mapper.columns:
        field_name = column.key
        value = getattr(model, field_name)

        if isinstance(value, UUID):
            value = str(value)
        elif isinstance(value, datetime):
            value = value.isoformat()

        serialized[field_name] = value

    return serialized
