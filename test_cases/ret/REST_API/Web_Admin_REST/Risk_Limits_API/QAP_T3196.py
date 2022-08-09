import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Risk_Limits_API.RestApiBuyingPowerMessages import \
    RestApiBuyingPowerMessages
from test_framework.core.try_exept_decorator import try_except


class QAP_T3196(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.qap_id = os.path.basename(__file__)[:-3]
        self.test_id = bca.create_event(self.qap_id, report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.buying_power_messages = RestApiBuyingPowerMessages(data_set)
        self.tested_bp_rule_name = "api_bp_rule"

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create BuyingPower with HoldingRation > 100 and verify result
        self.buying_power_messages.create_buying_power()
        self.buying_power_messages.update_parameters(parameters={'holdingsRatio': 140})

        self.wa_api_manager.send_post_request(self.buying_power_messages)

        self.buying_power_messages.find_all_buying_power_limit()
        buying_power_rule = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request(self.buying_power_messages),
            filter_dict={'buyingPowerLimitName': self.tested_bp_rule_name})
        print(buying_power_rule)

        if 'buyingPowerLimitName' in buying_power_rule[0].keys():
            bca.create_event('New BP rule was created with HoldingRatio > 100', status='FAILED', parent_id=self.test_id)
        else:
            bca.create_event("New BP rule wasn't created", status='SUCCESS', parent_id=self.test_id)
        # endregion
