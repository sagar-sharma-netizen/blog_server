import functools
import json
from typing import Callable, Union, Tuple
from webob import Response


def jsonresponse(
        func: Callable[..., Union[dict, Tuple[str, dict]]]
) -> Callable[..., Response]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("jsonresponse")
        print(func)
        result = func(*args, **kwargs)
        print(result)
        if isinstance(result, tuple):
            status, result = result
        else:
            status, result = "200 Ok", result
        response = Response(status=status, body=json.dumps(result))
        response.headers.add("content-type", "application/json")
        return response

    return wrapper


def api(
        func: Callable[..., Union[dict, Tuple[str, dict]]]
) -> Callable:
    @functools.wraps(func)
    def wrapper(request):
        params = request.params
        body = request.body
        res = func(*body, **params)
        print(res)
        return res

    return wrapper
