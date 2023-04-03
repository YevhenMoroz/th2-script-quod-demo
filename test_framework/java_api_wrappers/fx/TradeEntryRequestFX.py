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
                "ExecPrice": "1.18",
                "ExecQty": "1000000",
                "TradeEntryTransType": "NEW",
                "VenueExecID": bca.client_orderid(7),
                "LastMkt": "XQFX",
                "SettlDate": self.get_data_set().get_settle_date_by_name("spot_java_api"),
                "TradeDate": self.get_data_set().get_settle_date_by_name("today_java_api"),
                "Side": "B",
                "Currency":self.get_data_set().get_currency_by_name("currency_eur"),
                "AccountGroupID": "CLIENT_TEST_EXT",
                "ListingID": "506403761",  # EUR/USD
                # "ListingID": "506404433",  # GBP/USD
                # "ListingID": "506409971", # USD/PHP
                # "ListingID": "506403285", # EUR/GBP
                "SettlCurrFxRate": "0",
                "ExecMiscBlock": {
                    "ExecMisc0": bca.client_orderid(10),
                }
            }
        }
        super().change_parameters(request_params)
        return self

    def set_params_for_fwd(self):
        request_params = {
            "SEND_SUBJECT": "QUOD.ORS.FE",
            "REPLY_SUBJECT": "QUOD.FE.ORS",
            "TradeEntryRequestBlock": {
                "ExecPrice": "1.18",
                "ExecQty": "1000000",
                "TradeEntryTransType": "NEW",
                "VenueExecID": bca.client_orderid(7),
                "LastMkt": "XQFX",
                "SettlDate": self.get_data_set().get_settle_date_by_name("wk1_java_api"),
                "TradeDate": self.get_data_set().get_settle_date_by_name("today_java_api"),
                "Side": "B",
                "AccountGroupID": "CLIENT1",
                "ListingID": "506403765",  # EUR/USD WK1
                "SettlCurrFxRate": "0",
                "ExecMiscBlock": {
                    "ExecMisc0": bca.client_orderid(10),
                }
            }
        }
        super().change_parameters(request_params)
        return self

    def get_exec_id(self, response) -> str:
        return response[1].get_parameters()["ExecutionReportBlock"]["ExecID"]

    def get_ah_exec_id(self, response) -> str:
        return response[4].get_parameters()["ExecutionReportBlock"]["ExecID"]

    def get_internal_exec_id(self, response) -> str:
        return response[0].get_parameters()["ExecutionReportBlock"]["ExecID"]

    def get_termination_time(self, response) -> str:
        return response[1].get_parameters()["ExecutionReportBlock"]["TerminationTime"]

    def get_venue_exec_id(self):
        return self.get_parameters()["TradeEntryRequestBlock"]["VenueExecID"]

    def get_exec_misc_0(self):
        return self.get_parameters()["TradeEntryRequestBlock"]["ExecMiscBlock"]["ExecMisc0"]
