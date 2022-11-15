import os

from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiManager import WebAdminRestApiManager
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.web_admin_api.Users_API.RestApiUserSessionMessages import \
    RestApiUserSessionMessages
from test_framework.core.try_exept_decorator import try_except
from test_framework.rest_api_wrappers.utils.verifier import data_validation


class QAP_T3620(TestCase):
    def __init__(self, report_id, data_set: BaseDataSet, environment):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
        self.session_alias_wa_site = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.wa_api_manager_site = WebAdminRestApiManager(session_alias=self.session_alias_wa_site,
                                                          case_id=self.test_id)
        self.user_session_message = RestApiUserSessionMessages(data_set=data_set)
        self.test_user = "adm01"

    @try_except(test_id=os.path.basename(__file__)[:-3])
    def run_pre_conditions_and_steps(self):
        # region Drop user session and check result
        self.user_session_message.find_all_user_session()
        user_session = self.wa_api_manager_site.parse_response_details(
            response=self.wa_api_manager_site.send_get_request(self.user_session_message),
            filter_dict={"userID": self.test_user}
        )
        if user_session:
            self.user_session_message.drop_session(
                user_id=user_session[0]["userID"],
                role_id=user_session[0]["roleID"],
                session_key=user_session[0]["sessionKey"]
            )
            self.wa_api_manager_site.send_post_request(self.user_session_message)

            self.user_session_message.find_all_user_session()
            user_session_step2 = self.wa_api_manager_site.parse_response_details(
                response=self.wa_api_manager_site.send_get_request(self.user_session_message)
            )
            if user_session_step2:
                user_status = True
                for count in range(len(user_session_step2)):
                    user_session_id = user_session_step2[count]["userID"]
                    if user_session_id == self.test_user:
                        bca.create_event(f"User session for user {self.test_user} was not deleted",
                                         status='FAILED', parent_id=self.test_id)
                        user_status = False
                        break
                if user_status:
                    bca.create_event(f"User session for user {self.test_user} was deleted", parent_id=self.test_id)
            else:
                bca.create_event(f"User session was not received. Step 2", status='FAILED', parent_id=self.test_id)
        else:
            bca.create_event(f"User session was not received. Step 1", status='FAILED', parent_id=self.test_id)

