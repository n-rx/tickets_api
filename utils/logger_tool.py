import logging

from datetime import datetime
from functools import wraps

from utils.exceptions import (
    NoRequiredFieldsException,
    InvalidFieldTypeException,
    ConflictException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    UnprocessableContent,
)
from utils.http_errors import raise_error


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logfile.log")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
logger.addHandler(file_handler)


def log_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(
            "[{dt}] [{fnc}]".format(
                dt=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                fnc=func.__name__,
            )
        )

        try:
            result = func(*args, **kwargs)
            return result
        except NoRequiredFieldsException as no_required_fields:
            logger.exception(
                "Exception raised in {0}. exception: {1}".format(
                    func.__name__, str(no_required_fields)
                )
            )
            return raise_error(error=str(no_required_fields))
        except InvalidFieldTypeException as invalid_field_type:
            logger.exception(
                "Exception raised in {0}. exception: {1}".format(
                    func.__name__, str(invalid_field_type)
                )
            )
            return raise_error(error=str(invalid_field_type))
        except ConflictException as conflict:
            logger.exception(
                "Exception raised in {0}. exception: {1}".format(
                    func.__name__, str(conflict)
                )
            )
            return raise_error(error=str(conflict), error_code=409)
        except NotFoundException as not_found:
            logger.exception(
                "Exception raised in {0}. exception: {1}".format(
                    func.__name__, str(not_found)
                )
            )
            return raise_error(error=str(not_found), error_code=404)
        except UnauthorizedException as unauthorized:
            logger.exception(
                "Exception raised in {0}. exception: {1}".format(
                    func.__name__, str(unauthorized)
                )
            )
            return raise_error(error=str(unauthorized), error_code=401)
        except ForbiddenException as forbidden:
            logger.exception(
                "Exception raised in {0}. exception: {1}".format(
                    func.__name__, str(forbidden)
                )
            )
            return raise_error(error=str(forbidden), error_code=403)
        except UnprocessableContent as unprocessable_content:
            logger.exception(
                "Exception raised in {0}. exception: {1}".format(
                    func.__name__, str(unprocessable_content)
                )
            )
            return raise_error(error=str(unprocessable_content), error_code=422)
        except Exception as e:
            logger.exception(
                "Exception raised in {0}. exception: {1}".format(func.__name__, str(e))
            )
            return raise_error(error="Bad Request", error_code=400)

    return wrapper
