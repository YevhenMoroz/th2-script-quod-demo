from datetime import datetime

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixMessageRequestForPositions import FixMessageRequestForPositions


class FixMessageRequestForPositionsFX(FixMessageRequestForPositions):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(parameters, data_set=data_set)

    def set_default(self):
        base_parameters = {
            "PosReqID": bca.client_orderid(9),
            "PosReqType": "0",
            "SubscriptionRequestType": "1",
            "TransactTime": datetime.utcnow().isoformat(),
            "Account": self.get_data_set().get_client_by_name("client_mm_1"),
            "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
            "ClearingBusinessDate": self.get_data_set().get_settle_date_by_name("spot"),
            "SettlDate": self.get_data_set().get_settle_date_by_name("spot"),
            "Instrument": {
                "SecurityType": self.get_data_set().get_security_type_by_name("fx_spot"),
                "Symbol": self.get_data_set().get_symbol_by_name("symbol_1"),
            },
            #     "Parties": {"NoPartyIDs":[{
            #         "PartyID": self.get_data_set().get_account_by_name("account_mm_1"),
            #         "PartyIDSource": "POS",
            #         "PartyRole": "D"}]
            # }
        }
        super().change_parameters(base_parameters)
        return self

    def set_params_for_fwd(self):
        base_parameters = {
            "PosReqID": bca.client_orderid(9),
            "PosReqType": "0",
            "SubscriptionRequestType": "1",
            "TransactTime": datetime.utcnow().isoformat(),
            "Account": self.get_data_set().get_client_by_name("client_mm_1"),
            "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
            "ClearingBusinessDate": self.get_data_set().get_settle_date_by_name("wk1"),
            "SettlDate": self.get_data_set().get_settle_date_by_name("wk1"),
            "Instrument": {
                "SecurityType": self.get_data_set().get_security_type_by_name("fx_fwd"),
                "Symbol": self.get_data_set().get_symbol_by_name("symbol_1"),
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_unsubscribe(self):
        self.change_parameter("SubscriptionRequestType", "2")
        return self
