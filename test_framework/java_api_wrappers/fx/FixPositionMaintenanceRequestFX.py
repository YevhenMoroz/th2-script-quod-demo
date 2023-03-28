from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import ORSMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from custom import basic_custom_actions as bca


class FixPositionMaintenanceRequestFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=PKSMessageType.FixPositionMaintenanceRequest.value, data_set=data_set)
        super().change_parameters(parameters)
        self.base_currency = self.get_data_set().get_currency_by_name("currency_eur")
        self.quote_currency = self.get_data_set().get_currency_by_name("currency_usd")

    def set_default_params(self):
        request_params = {
            "SEND_SUBJECT": "QUOD.PKS.REQUEST",
            "REPLY_SUBJECT": "QUOD.PKS.REPLY",
            "PositionMaintenanceRequestBlock": {
                "InstrumentBlock": {
                    "InstrSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                    "InstrType": self.get_data_set().get_fx_instr_type_ja("fx_spot")
                },
                "ClientAccountGroupID": self.get_data_set().get_client_by_name("client_mm_1"),
                "PosMaintAction": "DEL",
                "PosTransType": "ADJ",
                "ClientPosReqID": bca.client_orderid(9),
                "SettlDate": self.get_data_set().get_settle_date_by_name("spot_java_api"),
                "ClearingBusinessDate": self.get_data_set().get_settle_date_by_name("spot"),
                "PartiesList": {
                    "PartiesBlock": [
                        {"PartyID": self.get_data_set().get_account_by_name("account_mm_1"),
                         "PartyIDSource": "Proprietary",
                         "PartyRole": "PositionAccount"}
                    ]
                },
                "PositionAmountDataList": {
                    "PositionAmountDataBlock": [
                        {
                            "PosAmtType": "BASE",
                            "PosAmt": "0",
                            "PositionCurrency": self.base_currency,
                        },
                        {
                            "PosAmtType": "INIQ",
                            "PosAmt": "0",
                            "PositionCurrency": self.base_currency,
                        },
                        {
                            "PosAmtType": "CBUQ",
                            "PosAmt": "0",
                            "PositionCurrency": self.base_currency,
                        },
                        {
                            "PosAmtType": "CSLQ",
                            "PosAmt": "0",
                            "PositionCurrency": self.base_currency,
                        },
                        {
                            "PosAmtType": "LEB",
                            "PosAmt": "0",
                            "PositionCurrency": self.base_currency,
                        },
                        {
                            "PosAmtType": "LES",
                            "PosAmt": "0",
                            "PositionCurrency": self.base_currency,
                        },
                        {
                            "PosAmtType": "AVG",
                            "PosAmt": "0",
                            "PositionCurrency": self.base_currency,
                        },
                        {
                            "PosAmtType": "QSYS",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "SYSQ",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "QSYS",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "WORK",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "QCLB",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "QCLS",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "QSYS",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        }, {
                            "PosAmtType": "QWO",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        }, {
                            "PosAmtType": "SYQWO",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        }, {
                            "PosAmtType": "SYWO",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        }, {
                            "PosAmtType": "QDMP",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "QMMP",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "QYMP",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "QDPL",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "QMPL",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "QYPL",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "SYDPL",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "SYMPL",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "SYYPL",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "QUPL",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "SYUPL",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "QINI",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "QCUB",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "QCUS",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        },
                        {
                            "PosAmtType": "QUOQ",
                            "PosAmt": "0",
                            "PositionCurrency": self.quote_currency,
                        }
                    ]

                }

            }
        }
        super().change_parameters(request_params)
        return self

    def change_instrument(self, currency_pair, instr_type="FXSpot"):
        self.get_parameters()["PositionMaintenanceRequestBlock"]["InstrumentBlock"]["InstrSymbol"] = currency_pair
        self.get_parameters()["PositionMaintenanceRequestBlock"]["InstrumentBlock"]["InstrType"] = instr_type
        pos_data = self.get_parameters()["PositionMaintenanceRequestBlock"]["PositionAmountDataList"]
        for a in pos_data["PositionAmountDataBlock"]:
            if a["PositionCurrency"] == self.base_currency:
                a["PositionCurrency"] = currency_pair[0:3]
            else:
                a["PositionCurrency"] = currency_pair[4:7]
        return self

    def change_client(self, client):
        self.update_fields_in_component("PositionMaintenanceRequestBlock", {"ClientAccountGroupID": client})
        return self

    def change_account(self, account):
        self.get_parameters()["PositionMaintenanceRequestBlock"]["PartiesList"]["PartiesBlock"][0]["PartyID"] = account
        return self

    def change_settle_date(self, settle_date):
        self.update_fields_in_component("PositionMaintenanceRequestBlock", {"SettlDate": settle_date})
        return self
