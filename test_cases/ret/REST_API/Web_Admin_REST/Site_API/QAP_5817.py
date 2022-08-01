import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Site_API.RestApiInstitutionMessages import RestApiInstitutionMessages
from test_framework.core.try_exept_decorator import try_except
from test_cases.wrapper.ret_wrappers import verifier


class QAP_5817(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.qap_id = os.path.basename(__file__)[:-3]
        self.test_id = bca.create_event(self.qap_id, report_id)
        self.session_alias_wa = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.wa_api_manager = WebAdminRestApiManager(session_alias=self.session_alias_wa, case_id=self.test_id)
        self.institution_message = RestApiInstitutionMessages(data_set=data_set)

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        self.institution_message.create_institution()
        self.institution_message.update_parameters(parameters={"crossCurrencySettlement": "true"})
        self.institution_message.update_parameters(parameters={"institutionName": self.qap_id + "_api"})
        institution_name = self.institution_message.parameters["institutionName"]
        self.wa_api_manager.send_post_request(self.institution_message)

        self.institution_message.find_all_institution()
        new_institution = self.wa_api_manager.parse_response_details(
            response=self.wa_api_manager.send_get_request(self.institution_message),
            filter_dict={"institutionName": institution_name})
        try:
            verifier(case_id=self.test_id,
                     event_name=f"Check that new institution -  '{institution_name}' is created",
                     expected_value="true",
                     actual_value=new_institution[0]["alive"])
            institution_fields = new_institution[0].keys()
            if "crossCurrencySettlement" in institution_fields:
                verifier(case_id=self.test_id,
                         event_name="Check that 'crossCurrencySettlement' is activated",
                         expected_value="true",
                         actual_value=new_institution[0]["crossCurrencySettlement"])
            else:
                bca.create_event(f'The crossCurrencySettlement field is deactivated', status='SUCCESS', parent_id=self.test_id)
        except (KeyError, IndexError, TypeError):
            bca.create_event('Response is empty', status='FAILED', parent_id=self.test_id)
