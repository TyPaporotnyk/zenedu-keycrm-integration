import hashlib
import hmac
from datetime import datetime


def generate_way_for_pay_signature(merchant_account: str, merchant_secret_key: str, date_begin: int, date_end: int):
    str_to_sign = ";".join(
        [merchant_account, str(date_begin) if date_begin else "", str(date_end) if date_end else ""]
    )

    hmac_signature = hmac.new(
        merchant_secret_key.encode("utf-8"), str_to_sign.encode("utf-8"), hashlib.md5
    ).hexdigest()

    return hmac_signature


def convert_datetime_or_str_to_unix_datetime(date: datetime | str) -> int:
    if isinstance(date, datetime):
        date = int(date.timestamp())
    elif isinstance(date, str) and not date.isdigit():
        date = int(datetime.strptime(date, "%Y-%m-%d").timestamp())

    return date
