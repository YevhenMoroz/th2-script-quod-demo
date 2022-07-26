from datetime import datetime

from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet
from pandas import Timestamp as tm


class RestApiSecurityPositionMessages(WebAdminRestApiMessages):
    def __init__(self, parameters='', data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)
        self.default_account_security_position = self.data_set.get_account_by_name('account_4')
        self.default_instrument_id = self.data_set.get_instrument_id_by_name('instrument_id_2')

    def find_positions(self, security_account_name, alive=False):
        self.message_type = "FindPositions"
        self.parameters = {'URI': {
            "queryLookup": security_account_name,
            "aliveOnly": alive
        }}

    def create_collateral_assignments(self, qty, custom_params=None):
        self.message_type = "CreateCollateralAssignment"
        # TDE value needed for increasing CollateralQty
        # TWI value needed for decreasing CollateralQty
        default_parameters = {
            "positionType": "N",
            "instrID": self.default_instrument_id,
            "accountID": self.default_account_security_position,
            "qty": qty,
            "transactTime": 1111111,
            "collateralAssignmentReason": "TDE"
        }
        if custom_params is not None:
            self.parameters = custom_params
        else:
            self.parameters = default_parameters

    def modify_security_positions(self, params):
        self.message_type = "ModifyPosition"
        self.parameters = params
