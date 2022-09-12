from copy import deepcopy

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages
from test_framework.rest_api_wrappers.oms.VenueSecActNameEntity import VenueSecActNameEntity


class RestAPIModifySecurityAccountMessage(RestApiMessages):

    def __init__(self, data_set: BaseDataSet):
        super().__init__("", data_set)
        self.message_type = "ModifySecurityAccount"
        self.all_venue_sec_act_names: list = []

    def set_common_venue_sec_act_names(self, security_account_name_from_data_set):
        tuple_of_venue_sec_act_names = deepcopy(
            self.data_set.get_all_venue_sec_account_names_of_acc(security_account_name_from_data_set))
        for entity in tuple_of_venue_sec_act_names:
            self.all_venue_sec_act_names.append(VenueSecActNameEntity(entity).convert_value_to_dict())

    def modify_security_account_without_repeating_group(self, security_account, client, params=None):
        default_parameters = {
            'accountGroupID': client,
            'accountID': security_account,
            'clientAccountID': security_account,
            'alive': True,
            'tradeConfirmEligibility': True,
            'clearingAccountType': self.data_set.get_clearing_account_type('institutional'),
            'venueSecActName': self.all_venue_sec_act_names,
            'clientAccountIDSource': self.data_set.get_account_id_source('oth'),
            'isWashBook': False
        }
        if params:
            default_parameters.update(params)
        self.parameters.update(default_parameters)

    def modify_repeating_group_of_security_account(self, params: dict, venue_id: str):
        '''
        find needfull repeating via VenueID
        params can accept as key:
                "levyFeeExemption"
                "perTransacFeeExemption"
                "stampFeeExemption"
                "venueAccountIDSource"
               "venueAccountName"
                "venueClientAccountName"
                "venueID"
        '''
        for repeating_group in self.all_venue_sec_act_names:
            if venue_id is repeating_group['venueID']:
                repeating_group.update(params)
        print(self.all_venue_sec_act_names)
