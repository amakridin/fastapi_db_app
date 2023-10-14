from . import users, bots, admin

ROUTERS = [
    users.router,
    bots.router,
    admin.router,
]
