from .database import connect
from .handlers import get_handler
from .request import Request
from .responses import NotFoundResponse
from .routing import route


def get_response(request):
    matched_route = route(request.db, request.path)
    if not matched_route:
        return NotFoundResponse()
    handler = get_handler(matched_route["handler"])
    response = handler(request)
    return response


def make_app(test_db=None):
    def app(environ, start_response):
        db = test_db or connect("db.sqlite")
        request = Request(environ, db)
        response = get_response(request)
        start_response(response.get_status_line(), response.get_headers())
        return response.get_content()

    return app