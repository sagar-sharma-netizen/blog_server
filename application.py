import functools
import json
from typing import Optional, Callable, Tuple, Union
from webob import Request, Response
from utils.router import Router, RouteHandlerT


class Application:
    def __init__(self, request: Request, environ) -> None:
        self.router = Router()
        self.request = request
        self.environ = environ

    def add_route(
            self,
            path: str,
            method: str,
            handler: RouteHandlerT,
            name: Optional[str]
    ) -> None:
        self.router.add_route(path=path, method=method, handler=handler, name=name or handler.__name__)

    # decorator: route
    def route(
            self,
            path: str,
            method: str,
            name: Optional[str] = None
    ) -> Callable[[RouteHandlerT], RouteHandlerT]:
        def decorator(handler: RouteHandlerT) -> RouteHandlerT:
            self.add_route(path=path, method=method, handler=handler, name=name)
            return handler
        return decorator

    def __call__(self) -> Response:
        handler = self.router.lookup(self.request.method, self.request.path)
        if handler is None:
            return Response("404 Not Found")
        return handler(self.request)


def boot(environ, start_response) -> Response:
    # boot application
    request = Request(environ)
    app = Application(request=request, environ=environ)
    res = app()
    return res(environ, start_response)
