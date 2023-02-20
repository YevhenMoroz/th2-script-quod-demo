from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from custom import basic_custom_actions as bca


class TradeEntryRequestFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=ORSMessageType.TradeEntryRequest.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_default_params(self):
        request_params = {
            "SEND_SUBJECT": "QUOD.ORS.FE",
            "REPLY_SUBJECT": "QUOD.FE.ORS",
            "TradeEntryRequestBlock": {
                "ExecPrice": "1.2",
                "ExecQty": "25000000",
                "TradeEntryTransType": "NEW",
                "VenueExecID": "Test123",
                "LastMkt": "XQFX",
                "SettlDate": self.get_data_set().get_settle_date_by_name("spot_java_api"),
                "TradeDate": self.get_data_set().get_settle_date_by_name("today_java_api"),
                "Side": "B",
                "AccountGroupID": "CLIENT_TEST_EXT",
                "ListingID": "506403761", # EUR/USD
                # "ListingID": "506404433", # GBP/USD
                # "ListingID": "506409971", # USD/PHP
                "SettlCurrFxRate": "0",
                "OrdrMiscBlock": {
                    "OrdrMisc2": "test"
                },
                "ExecMiscBlock": {
                    "ExecMisc2": "test2"
                }
            }
        }
        super().change_parameters(request_params)
        return self

