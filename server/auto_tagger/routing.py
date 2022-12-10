from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path("ws/auto_tag/", consumers.WorkerConsumer.as_asgi())
]
