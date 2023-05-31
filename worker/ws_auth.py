import hashlib

from common import message_codes as mc
from . import config
from .media_manager import Module, receive_handler, MessageContext, MediaManager


class WSAuth(Module):
    def __init__(self, manager: MediaManager):
        self.manager = manager

    @receive_handler(mc.HELLO)
    async def hello_handler(self, ctx: MessageContext):
        m = hashlib.sha256()
        m.update(config.config.client_secret.encode())
        m.update(ctx.msg["challenge"].encode())
        answer = m.hexdigest()
        await ctx.reply({
            "opcode": mc.AUTH,
            "client_id": config.config.client_id,
            "response": answer
        })

    @receive_handler(mc.AUTHED)
    async def authed_handler(self, ctx: MessageContext):
        print("Websocket Authenticated!")
