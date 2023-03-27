from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime


class FixAllocationInstruction(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.FixAllocationInstruction.value)
        super().change_parameters(parameters)

    def set_default(self, data_set: BaseDataSet) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.ALLOC.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "AllocationInstructionBlock": {
                "ExecAllocList": {
                    "ExecAllocBlock": [{"ExecQty": "100",
                                        "ExecID": "*",
                                        "ExecPrice": "10"}]},
                "ClientAllocID": "0",
                "AllocTransType": "New",
                "AllocType": "ReadyToBook",
                "Side": "Buy",
                "Currency": data_set.get_currency_by_name("currency_1"),
                "TradeDate": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%d'),
                "Qty": "100",
                "SettlDate": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%d'),
                "GrossTradeAmt": "1000",
                "BookingType": "RegularBooking",
                "InstrumentBlock": {"InstrSymbol": "FR0010436584_EUR",
                                    "SecurityID": "FR0010436584",
                                    "SecurityIDSource": "ISIN",
                                    "InstrType": "Equity"},
                "AvgPx": "10",
                "AccountGroupID": data_set.get_client_by_name("client_1")}}
        super().change_parameters(base_parameters)
