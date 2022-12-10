from django.db import models
import secrets
import string
import hashlib


def _gen_id(length: int) -> str:
    chars = string.ascii_letters + string.digits
    result = ""
    for _ in range(length):
        result += secrets.choice(chars)
    return result


def default_client_id() -> str:
    return _gen_id(16)


def default_client_secret() -> str:
    return _gen_id(32)


class Tagger(models.Model):
    name = models.CharField(max_length=16)
    client_id = models.CharField(max_length=16, default=default_client_id)
    client_secret = models.CharField(max_length=32, default=default_client_secret)
    active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(null=True, default=None)

    @staticmethod
    def get_challenge():
        return _gen_id(8)

    def can_auth(self, challenge: str, response: str) -> bool:
        m = hashlib.sha256()
        m.update(self.client_secret.encode())
        m.update(challenge.encode())
        answer = m.hexdigest()
        if len(answer) != len(response):
            return False
        match = True
        for a, r in zip(answer, response):
            match &= a == r
        return match


