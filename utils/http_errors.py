from flask import jsonify


def raise_error(error: str, error_code: int = 400):
    return jsonify({"message": error}), error_code
