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
        'TradeDate': '*',
        "GrossTradeAmt": "*",
        "ClientAccountID": "*",
        "NetSettlAmt": "*",
        "NetMoney": "*"
    }
