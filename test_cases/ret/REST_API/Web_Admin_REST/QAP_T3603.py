import os

from custom import basic_custom_actions as bca
from test_framework.old_wrappers.ret_wrappers import verifier
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


def execute(report_id):
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

    # for this connection used - site_adm_rest user
    api_message_site_adm = RestApiMessages()
    api_manager_site_adm = RestApiManager(session_alias='rest_wa315luna_site_admin', case_id=case_id)

    # for this connection used - adm_rest user
    api_message_tested_user = RestApiMessages()
    api_manager_tested_user = RestApiManager(session_alias='rest_wa315luna', case_id=case_id)

    # region Pre-Condition Set hierarchy level - Test_Location(id=6)
    location_params = {

        "userConfirmFollowUp": "false",
        "userID": "adm_rest",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "headOfDesk": "false",
        "locationID": 6
    }
    api_message_site_adm.modify_user(location_params)
    api_manager_site_adm.send_post_request(api_message_site_adm)

    # region Send Get request and verify result
    api_message_tested_user.find_all_user()
    user_params = api_manager_tested_user.get_response_details(
        response=api_manager_tested_user.send_get_request(api_message_tested_user),
        response_name="UserResponse",
        expected_entity_name="adm_rest",
        entity_field_id="userID")

    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel after change on locationID=6",
             expected_value="6",
             actual_value=user_params["locationID"].simple_value)
    # endregion

    # region Set the same desk via user which have hierarchy level=Desk - step 2
    modify_params = {
        "userConfirmFollowUp": "false",
        "userID": "user_desk",
        "userEmail": "q",
        "clientUserID": "QAP_T3629",
        "useOneTimePasswd": "false",
        "roleID": "TRA",
        "pingRequired": "false",
        "deactivated": "false",
        "loginLocked": "false",
        "permRoleID": 10007,
        "headOfDesk": "false",
        "preferredCommMethod": "EML",
        "deskUserRole": [
            {
                "deskID": 4
            }
        ]
    }
    api_message_tested_user.modify_user(modify_params)
    api_manager_tested_user.send_post_request(api_message_tested_user)
    # endregion

    # # region Send Get request and verify result - step 3
    api_message_tested_user.find_all_user()
    user_params = api_manager_tested_user.get_response_details(
        response=api_manager_tested_user.send_get_request(api_message_tested_user),
        response_name="UserResponse",
        expected_entity_name="user_desk",
        entity_field_id="userID")
    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel for user_desk",
             expected_value="5",
             actual_value=user_params["deskUserRole"].list_value.values[0].message_value.fields["deskID"].simple_value)
    # endregion
