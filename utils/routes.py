from users import user

ROUTE_PREFIX = "/blog_server"
routes = {
    "/users": {
        "GET": user.get_users
    }
}
