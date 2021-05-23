import re
from typing import Dict, Tuple, Optional, Pattern, Callable, Set
from collections import OrderedDict, defaultdict
from functools import partial
from webob import Request, Response
from utils.routes import routes, ROUTE_PREFIX

HandlerT = Callable[[Request], Response]
RouteT = Tuple[Pattern[str], HandlerT]
RoutesT = Dict[str, Dict[str, RouteT]]
RouteHandlerT = Callable[..., Response]


class Router:
    def __init__(self) -> None:
        self.routes_by_method: RoutesT = defaultdict(OrderedDict)
        self.route_names: Set[str] = set()

    def add_route(
            self,
            name: str,
            method: str,
            path: str,
            handler: RouteHandlerT
    ) -> None:
        print("path", path)
        assert path.startswith("/")
        if name in self.route_names:
            raise ValueError(f"A route named {name} already exists.")

        route_template = ""
        print(path.split("/")[1:])
        for segment in path.split("/")[1:]:
            if segment.startswith("{") and segment.endswith("}"):
                segment_name = segment[1:-1]
                route_template += f"/(?P<{segment_name}>[^/]+)"
            else:
                route_template += f"/{segment}"

        route_re = re.compile(f"^{route_template}$")
        self.routes_by_method[method][name] = route_re, handler
        self.route_names.add(name)

    def lookup(self, method: str, path: str) -> Optional[HandlerT]:
        print("path", path)
        print(self.routes_by_method[method].values())
        path = path.replace(ROUTE_PREFIX, "")
        all_routes = routes.get(path.lower(), None)
        if all_routes is not None:
            route = all_routes.get(method, None)
            if route is not None:
                return route
        # for route_re, handler in self.routes_by_method[method].values():
        #     match = route_re.match(path)
        #     if match is not None:
        #         params = match.groupdict()
        #         return partial(handler, **params)
        return None
