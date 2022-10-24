from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.OrderSubmit import OrderSubmit


class OrderSubmitOMS(OrderSubmit):
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
                'OrdType': 'Market',
                'TimeInForce': 'Day',
                'PositionEffect': 'Open',
                'SettlCurrency': 'EUR',
                'OrdCapacity': 'Agency',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'MaxPriceLevels': "1",
                'ExecutionOnly': 'No',
                'ClientInstructionsOnly': 'No',
                'BookingType': 'RegularBooking',
                'OrdQty': "100",
                'AccountGroupID': data_set.get_client_by_name("client_1"),
                'ExecutionPolicy': 'DMA',
                'ListingList': {'ListingBlock': [{'ListingID': data_set.get_listing_id_by_name("listing_1")}]},
                'InstrID': data_set.get_instrument_id_by_name("instrument_1"),
                "ClOrdID": basic_custom_actions.client_orderid(9),
            }
        }

    def set_default_care_limit(self, recipient=None, desk=None, role=None, external_algo_twap=False):
        params = {'CDOrdAssignInstructionsBlock': {}}
        if recipient:
            params["CDOrdAssignInstructionsBlock"]["RecipientUserID"] = recipient
        if desk:
            params["CDOrdAssignInstructionsBlock"]["RecipientDeskID"] = desk
        if role:
            params["CDOrdAssignInstructionsBlock"]["RecipientRoleID"] = role
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('NewOrderSingleBlock',
                                        {"OrdType": 'Limit', "Price": "20", 'ExecutionPolicy': 'Care'})
        self.add_tag(params)
        algo_params = {"AlgoParametersBlock": {"AlgoType": "External",
                                               "ScenarioID": "101",
                                               "AlgoPolicyID": "1000131"},
                       "ExternalAlgoParametersBlock": {"ExternalAlgoParameterListBlock":
                           {"ExternalAlgoParameterBlock": [
                               {'AlgoParameterName': "StrategyTag",
                                "AlgoParamString": "TWAP",
                                'VenueScenarioParameterID': "7505"}]},
                           'ScenarioID': "101",
                           "ScenarioIdentifier": "8031",
                           "VenueScenarioID": "TWAP",
                           "VenueScenarioVersionID": "9682",
                           "VenueScenarioVersionValue": "ATDLEQ5.3.1"}}
        if external_algo_twap:
            self.update_fields_in_component('NewOrderSingleBlock', algo_params)
        return self

    def set_default_dma_limit(self):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('NewOrderSingleBlock', {"Price": '20', "OrdType": 'Limit'})
        return self

    def set_default_dma_market(self):
        self.change_parameters(self.base_parameters)
        return self

    def set_default_care_market(self, recipient=None, desk=None, role=None):
        params = {'CDOrdAssignInstructionsBlock': {}}
        if recipient:
            params["CDOrdAssignInstructionsBlock"]["RecipientUserID"] = recipient
        if desk:
            params["CDOrdAssignInstructionsBlock"]["RecipientDeskID"] = desk
        if role:
            params["CDOrdAssignInstructionsBlock"]["RecipientRoleID"] = role
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('NewOrderSingleBlock', {'ExecutionPolicy': 'Care'})
        self.add_tag(params)
        return self

    def set_default_child_care(self, recipient=None, desk=None, role=None, parent_id: str = None):
        params = {'CDOrdAssignInstructionsBlock': {}}
        if recipient:
            params["CDOrdAssignInstructionsBlock"]["RecipientUserID"] = recipient
        if desk:
            params["CDOrdAssignInstructionsBlock"]["RecipientDeskID"] = desk
        if role:
            params["CDOrdAssignInstructionsBlock"]["RecipientRoleID"] = role
        self.change_parameters(self.base_parameters)
        parent_params = {"ParentOrdrBlock": [{"ParentOrdID": parent_id}]}
        self.update_fields_in_component('NewOrderSingleBlock',
                                        {"OrdType": 'Limit', "Price": "20", 'ExecutionPolicy': 'Care',
                                         'ClOrdID':  basic_custom_actions.client_orderid(9), "ParentOrdrList": parent_params})
        self.add_tag(params)
        return self

    def set_default_child_dma(self, parent_id: str = None, client_order_id: str = None):
        if client_order_id:
            cl_ord_id = client_order_id
        else:
            cl_ord_id = basic_custom_actions.client_orderid(9)
        self.change_parameters(self.base_parameters)
        parent_params = {"ParentOrdrBlock": [{"ParentOrdID": parent_id}]}
        self.update_fields_in_component('NewOrderSingleBlock',
                                        {"OrdType": 'Limit', "Price": "20", "ParentOrdrList": parent_params,
                                         'ClOrdID': cl_ord_id})
        return self
