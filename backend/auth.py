import hashlib
import hmac
import os
from urllib.parse import parse_qsl

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def check_telegram_auth(init_data: str) -> dict | None:
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()

    parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    hash_from_telegram = parsed_data.pop("hash", None)

    sorted_data = sorted(f"{k}={v}" for k, v in parsed_data.items())
    data_check_string = "\n".join(sorted_data)

    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if hmac_hash == hash_from_telegram:
        return parsed_data  # valid!
    return None  # invalid!
