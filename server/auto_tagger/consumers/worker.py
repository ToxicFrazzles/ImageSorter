from .auth_handler import AuthHandler
from .ping_handler import PingHandler


class WorkerConsumer(PingHandler, AuthHandler):
    status: dict
