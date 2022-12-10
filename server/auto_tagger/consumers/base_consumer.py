import json
from typing import Optional, Callable, TypeVar, Awaitable, Dict

from channels.generic.websocket import AsyncWebsocketConsumer

from . import conn_state

Self = TypeVar("Self", bound="BaseConsumer")
Handler = Callable[[Self, dict], Awaitable]


class BaseConsumer(AsyncWebsocketConsumer):
    con_state: int = conn_state.UNKNOWN
    handlers: Dict[int, Handler]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.handlers: Dict[int, Handler] = {}
        for cls in self.__class__.__bases__:
            if hasattr(cls, "handlers"):
                self.handlers.update(cls.handlers)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            msg_obj = json.loads(text_data)
        except json.JSONDecodeError:
            await self.close()
            return
        op_code = msg_obj.get("opcode", -1)
        handler: Optional[Handler] = self.handlers.get(op_code, None)
        if handler is not None:
            await handler(self, msg_obj)
