from dataclasses import dataclass
from datetime import datetime
from typing import List

from httpx import Client

from apps.wayforpay.entities import Transaction
from apps.wayforpay.utils import convert_datetime_or_str_to_unix_datetime, generate_way_for_pay_signature

API_URL_PATH = "/api"


@dataclass
class WayForPayClient:
    http_client: Client
    merchant_account: str
    merchant_secret_key: str

    def get_transaction_list(self, date_begin: datetime | str, date_end: datetime | str) -> List[Transaction]:
        date_begin = convert_datetime_or_str_to_unix_datetime(date_begin)
        date_end = convert_datetime_or_str_to_unix_datetime(date_end)

        signature = generate_way_for_pay_signature(
            merchant_account=self.merchant_account,
            merchant_secret_key=self.merchant_secret_key,
            date_begin=date_begin,
            date_end=date_end,
        )

        json_data = {
            "apiVersion": 1,
            "transactionType": "TRANSACTION_LIST",
            "merchantAccount": self.merchant_account,
            "merchantSignature": signature,
            "dateBegin": date_begin,
            "dateEnd": date_end,
        }

        response = self.http_client.post(API_URL_PATH, json=json_data)

        data = response.json()

        transactions_data = data["transactionList"]

        transactions = [Transaction.from_dict(transaction) for transaction in transactions_data]

        return transactions
