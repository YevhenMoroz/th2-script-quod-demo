from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime


class Confirmation(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.Confirmation.value)
        super().change_parameters(parameters)

    def set_default(self, data_set: BaseDataSet) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "AllocationInstructionBlock": {
                "ExecAllocList": {
                    "ExecAllocBlock": [{"ExecQty": "100",
                                        "ExecID": "*",
                                        "ExecPrice": "10"}]},
                "AllocInstructionID": "0",
                "AllocTransType": "New",
                "AllocType": "ReadyToBook",
                "Side": "Buy",
                "Currency": data_set.get_currency_by_name("currency_1"),
                "TradeDate": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%d'),
                "Qty": "100",
                "SettlDate": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%d'),
                "GrossTradeAmt": "1000",
                "BookingType": "RegularBooking",
                "InstrID": data_set.get_instrument_id_by_name("instrument_1"),
                "AvgPx": "10",
                "AccountGroupID": data_set.get_client_by_name("client_1"),
                "ErroneousTrade": "No",
                "NetGrossInd": "Gross",
                "SettlCurrAmt": "1000",
                "RecomputeInSettlCurrency": "No",
                "ComputeFeesCommissions": "No"}}
        super().change_parameters(base_parameters)
