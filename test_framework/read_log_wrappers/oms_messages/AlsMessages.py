from enum import Enum


class AlsMessages(Enum):
    execution_report = {
        "ConfirmationID": "*",
        "AccountGroupID": "*",
        "ConfirmStatus": "*",
        "AllocQty": "*",
        "AvgPx": "*",
        "GrossPrice": "*",
        "NetPrice": "*",
        "Currency": "*",
        "GrossTradeAmt": "*",
        "ClientAccountID": "*",
        "NetSettlAmt": "*",
        "NetMoney": "*"
    }
