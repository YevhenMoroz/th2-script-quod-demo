from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from custom import basic_custom_actions as bca


class TradeEntryRequestFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=ORSMessageType.Fix_TradeEntryRequest.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_default_params(self):
        request_params = {
            "SEND_SUBJECT": "QUOD.ORS.FIX",
            "REPLY_SUBJECT": "QUOD.FE.ORS",
            "TradeEntryRequestBlock": {
                "ExecPrice": "1.18",
                "ExecQty": "1000000",
                "TradeEntryTransType": "NEW",
                "CDOrdFreeNotes": bca.client_orderid(7),
                "ClOrdID": bca.client_orderid(8),
                "LastMkt": "XQFX",
                "SettlDate": self.get_data_set().get_settle_date_by_name("spot_java_api"),
                # "SettlType": self.get_data_set().get_settle_type_by_name("spot"),
                "TradeDate": self.get_data_set().get_settle_date_by_name("today_java_api"),
                "Side": "B",
                "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
                "ClientAccountGroupID": "CLIENT_TEST_EXT",
                "InstrumentBlock": {
                    "InstrSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                    "InstrType": self.get_data_set().get_fx_instr_type_ja("fx_spot"),
                    "SecurityID": self.get_data_set().get_symbol_by_name("symbol_1"),
                    "SecurityExchange": "XQFX"
                },
                # "ListingID": "506403761",  # EUR/USD
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

    def change_instrument(self, symbol, istr_type):
        instrument = {
            "InstrSymbol": symbol,
            "InstrType": istr_type,
            "SecurityID": symbol,
            "SecurityExchange": "XQFX"
        }
        self.update_fields_in_component("TradeEntryRequestBlock", {"InstrumentBlock": instrument})

    # region Setters
    def set_exec_misc0(self, misc):
        self.get_parameters()["TradeEntryRequestBlock"]["ExecMiscBlock"]["ExecMisc0"] = misc

    def set_exec_misc1(self, misc):
        self.get_parameters()["TradeEntryRequestBlock"]["ExecMiscBlock"]["ExecMisc1"] = misc

    def set_exec_misc2(self, misc):
        self.get_parameters()["TradeEntryRequestBlock"]["ExecMiscBlock"]["ExecMisc2"] = misc

    def set_exec_misc3(self, misc):
        self.get_parameters()["TradeEntryRequestBlock"]["ExecMiscBlock"]["ExecMisc3"] = misc

    def set_exec_misc4(self, misc):
        self.get_parameters()["TradeEntryRequestBlock"]["ExecMiscBlock"]["ExecMisc4"] = misc

    def set_exec_misc5(self, misc):
        self.get_parameters()["TradeEntryRequestBlock"]["ExecMiscBlock"]["ExecMisc5"] = misc

    def set_exec_misc6(self, misc):
        self.get_parameters()["TradeEntryRequestBlock"]["ExecMiscBlock"]["ExecMisc6"] = misc

    def set_exec_misc7(self, misc):
        self.get_parameters()["TradeEntryRequestBlock"]["ExecMiscBlock"]["ExecMisc7"] = misc

    def set_exec_misc8(self, misc):
        self.get_parameters()["TradeEntryRequestBlock"]["ExecMiscBlock"]["ExecMisc8"] = misc

    def set_exec_misc9(self, misc):
        self.get_parameters()["TradeEntryRequestBlock"]["ExecMiscBlock"]["ExecMisc9"] = misc

    # endregion
    # region Getters
    def get_exec_id(self, response) -> str:
        return response[4].get_parameters()["ExecutionReportBlock"]["ExecID"]

    def get_mo_id(self, response) -> str:
        return response[0].get_parameters()["OrdNotificationBlock"]["OrdID"]

    def get_ah_exec_id(self, response) -> str:
        return response[-1].get_parameters()["ExecutionReportBlock"]["ExecID"]

    def get_ah_ord_id(self, response) -> str:
        return response[-1].get_parameters()["ExecutionReportBlock"]["OrdID"]

    def get_ord_id_from_held(self, response) -> str:
        return response[-2].get_parameters()["HeldOrderNotifBlock"]["OrdID"]

    def get_internal_exec_id(self, response) -> str:
        return response[0].get_parameters()["ExecutionReportBlock"]["ExecID"]

    def get_termination_time(self, response) -> str:
        return response[1].get_parameters()["ExecutionReportBlock"]["CreationTime"]

    def get_venue_exec_id(self):
        return self.get_parameters()["TradeEntryRequestBlock"]["VenueExecID"]

    def get_exec_misc_0(self):
        return self.get_parameters()["TradeEntryRequestBlock"]["ExecMiscBlock"]["ExecMisc0"]

    def get_exec_qty(self):
        return self.get_parameters()["TradeEntryRequestBlock"]["ExecQty"]

    def get_exec_price(self):
        return self.get_parameters()["TradeEntryRequestBlock"]["ExecPrice"]
    # endregion
