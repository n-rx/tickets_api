from uuid import UUID
from werkzeug.routing import BaseConverter


class UUIDConverter(BaseConverter):
    """Werkzeug URL converter for UUIDs.

    Args:
        BaseConverter (type): The parent class from Werkzeug for creating URL converters.
    """

    def to_python(self, value):
        try:
            return UUID(value)
        except ValueError:
            raise ValueError("Invalid UUID format.")

    def to_url(self, value):
        if isinstance(value, UUID):
            return str(value)
