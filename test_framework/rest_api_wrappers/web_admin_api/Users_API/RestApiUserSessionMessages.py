from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiUserSessionMessages(WebAdminRestApiMessages):

    def find_all_user_session(self):
        self.message_type = "FindAllUserSession"

    def drop_session(self, user_id, role_id, session_key):
        self.message_type = "DropSession"
        drop_session_params = {
            "dropSessionElement": [
                {
                    "userID": user_id,
                    "roleID": role_id,
                    "sessionKey": session_key
                }
            ]
        }
        self.parameters = drop_session_params
