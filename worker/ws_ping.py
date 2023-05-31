import time

from common import message_codes as mc
from .media_manager import MediaManager, Module, MessageContext, receive_handler


class WSPing(Module):
    def __init__(self, manager: MediaManager):
        self.manager = manager
        self.manager.avg_ping = 1000

    @receive_handler(mc.PONG)
    async def pong_handler(self, ctx: MessageContext):
        dur = (time.time() - ctx.msg["time"])*1000
        self.manager.avg_ping = (dur + self.manager.avg_ping) / 2
