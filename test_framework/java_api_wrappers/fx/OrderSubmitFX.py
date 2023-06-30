from copy import deepcopy
from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.OrderSubmit import OrderSubmit


class OrderSubmitFX(OrderSubmit):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'NewOrderSingleBlock': {
                'Side': 'Buy',
                'QtyType': 'Units',
                'OrdType': 'Limit',
                'TimeInForce': 'IOC',
                'SettlCurrency': 'EUR',
                'OrdCapacity': 'Principal',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'ExecutionOnly': 'No',
                'ClientInstructionsOnly': 'No',
                'ExternalCare': "No",
                'SpecialDeal': "No",
                'OrdQty': "1000000",
                'AccountGroupID': data_set.get_client_by_name("client_6"),
                'ExecutionPolicy': 'DMA',
                'ListingList': {'ListingBlock': [
                    {"ListingID": "100000939"}]},
                'InstrID': data_set.get_instr_id_by_name("eur_usd_spot"),
            }
        }

    def set_default_dma(self):
        self.change_parameters(deepcopy(self.base_parameters))
        self.update_fields_in_component('NewOrderSingleBlock',
                                        {"OrdType": 'Market'})
        return self

    def set_passive_algo(self):
        self.change_parameters(deepcopy(self.base_parameters))
        self.update_fields_in_component('NewOrderSingleBlock',
                                        {"OrdType": 'Limit', "Price": "1.18151", "OrdQty": "90000000",
                                         'ExecutionPolicy': 'S', 'ClOrdID': basic_custom_actions.client_orderid(9),
                                         'TimeInForce': 'Day', "AlgoParametersBlock": {
                                            "AlgoPolicyID": "400019", "AlgoType": "MUL", "ScenarioID": "7"},
                                         'ListingList': {'ListingBlock': [
                                             {"ListingID": "100000939"}, {"ListingID": "100000671"},
                                             {"ListingID": "1107422424"}, {"ListingID": "100000585"},
                                             {"ListingID": "100000241"}, {"ListingID": "100000843"},
                                             {"ListingID": "100000002"}, {"ListingID": "100000071"},
                                             {"ListingID": "100000327"}, {"ListingID": "100000413"},
                                             {"ListingID": "100000499"}, ]},
                                         "AccountGroupID": "ASPECT_CITI",
                                         "DisplayPx": "1.18152",
                                         "PriceDelta": "0",
                                         })
        return self

    def set_default_care(self, recipient="API", desk="2", role="TRA"):
        params = {'CDOrdAssignInstructionsBlock': {}}
        if recipient:
            params["CDOrdAssignInstructionsBlock"]["RecipientUserID"] = recipient
        if desk:
            params["CDOrdAssignInstructionsBlock"]["RecipientDeskID"] = desk
        if role:
            params["CDOrdAssignInstructionsBlock"]["RecipientRoleID"] = role
        self.change_parameters(deepcopy(self.base_parameters))
        self.update_fields_in_component('NewOrderSingleBlock',
                                        {"OrdType": 'Limit', "Price": "1.18", 'ExecutionPolicy': 'Care'})
        self.add_tag(params)
        return self

        # TODO TWAP and VWAP algo orders
        # if external_algo_twap:
        # algo_params = {"AlgoParametersBlock": {"AlgoType": "MultiListing",
        #                                        "ScenarioID": "7",
        #                                        "SORAlgoPolicyID": "400019"},
        #                }
        # self.update_fields_in_component('NewOrderSingleBlock', algo_params)