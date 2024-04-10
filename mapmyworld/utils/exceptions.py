from werkzeug.exceptions import RequestEntityTooLarge, UnsupportedMediaType
from mapmyworld.utils import api_response as Response
from flask import current_app
import traceback


def handle_exception(e):
    tb = traceback.extract_tb(e.__traceback__)[-1]
    filename = tb.filename.split('/')[-1]
    lineno = tb.lineno

    current_app.logger.error(
        "%s:%d Excepción capturada: %s", filename, lineno, str(e))

    if isinstance(e, UnsupportedMediaType):
        return Response.generic_error_response(message=str(e), code=415)

    return Response.unexpected_error("Internal Server Error")
