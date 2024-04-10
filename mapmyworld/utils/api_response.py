
from flask import jsonify, make_response
from mapmyworld.utils import messages


def generic_response(object: dict = {}, message: str = "", code: int = 200, status: int = True):
    return make_response(jsonify({**object, 'message': message, 'status': status}), code)


def generic_error_response(message="", code=400, errors=dict()):
    """
    Genera una respuesta de error genérica con un formato específico.
    """
    return make_response(jsonify({'message': message, 'status': False, "errors": errors}), code)


def generic_msg_ok_response(message):
    return make_response(jsonify({'message': message, 'status': True}), 200)


def generic_not_content_response():
    return make_response("", 204)


def unexpected_error(error):
    return make_response(jsonify({'message': error, 'status': False}), 500)
