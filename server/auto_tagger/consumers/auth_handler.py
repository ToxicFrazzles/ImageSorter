import json

from common import message_codes as mc
from .base_consumer import BaseConsumer
from .db_helpers import get_tagger
from ..models import Tagger
from . import conn_state


class AuthHandler(BaseConsumer):
    challenge: str

    async def connect(self):
        print("Connect")
        self.con_state = conn_state.CONNECTED
        await self.accept()
        msg = {
            "opcode": mc.HELLO,
            "challenge": Tagger.get_challenge()
        }
        self.challenge = msg["challenge"]
        await self.send(json.dumps(msg))
        self.con_state = conn_state.HELLO_SENT

    async def disconnect(self, code):
        print("Disconnected!")

    async def _auth_handler(self, msg_obj: dict):
        client_id = msg_obj["client_id"]
        response = msg_obj["response"]
        tagger: Tagger = await get_tagger(client_id)
        if tagger.can_auth(self.challenge, response):
            self.tagger = tagger
            self.con_state = conn_state.AUTHED
            await self.send(json.dumps({"opcode": mc.AUTHED}))
        else:
            await self.close()

    handlers = {
        mc.AUTH: _auth_handler
    }
