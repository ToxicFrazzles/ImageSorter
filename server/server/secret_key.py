import string
import secrets
from pathlib import Path
import os


def gen_secret_key():
    chars = string.ascii_letters + string.digits + string.punctuation
    result = ""
    for _ in range(32):
        result += secrets.choice(chars)
    return result


def get_secret_key():
    key = os.environ.get("SECRET_KEY", None)
    if key is not None:
        return key
    keyfile_path = Path("secret_key.txt")
    if keyfile_path.is_file():
        with keyfile_path.open() as f:
            return f.read().strip()
    key = gen_secret_key()
    with keyfile_path.open("w") as f:
        f.write(key)
    return key
