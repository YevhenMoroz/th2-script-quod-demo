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

    # region Set hierarchical level - Test_Location(id=6)
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
    # endregion

    # region Send Get request and verify result
    api_message_site_adm.find_all_user()
    user_params = api_manager_site_adm.get_response_details(
        response=api_manager_site_adm.send_get_request(api_message_site_adm),
        response_name="UserResponse",
        expected_entity_name="adm_rest",
        entity_field_id="userID")

    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel after change on locationID=6",
             expected_value="6",
             actual_value=user_params["locationID"].simple_value)
    # endregion

    # region Change settings for user with hierarchy - Test_Desk(id=6) via user with hierarchy - Test_Location(id=6)
    # Change field clientUserID from QAP-5444 to QAP-5444-test - step 2
    modify_params_desk_user = {
        "userConfirmFollowUp": "false",
        "userID": "user_desk",
        "userEmail": "1",
        "clientUserID": "QAP-5444-test",
        "useOneTimePasswd": "false",
        "venueUserID": "\"\"",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "permRoleID": 10007,
        "headOfDesk": "false",
        "preferredCommMethod": "EML",
        "deskUserRole": [
            {
                "deskID": 5
            }
        ]
    }
    api_message_tested_user.modify_user(modify_params_desk_user)
    api_manager_tested_user.send_post_request(api_message_tested_user)
    # endregion

    # region Send Get request and verify result - step 2
    api_message_tested_user.find_all_user()
    user_params = api_manager_tested_user.get_response_details(
        response=api_manager_tested_user.send_get_request(api_message_tested_user),
        response_name="UserResponse",
        expected_entity_name="user_desk",
        entity_field_id="userID")

    verifier(case_id=case_id,
             event_name="Check tested field = clientUserID",
             expected_value="QAP-5444-test",
             actual_value=user_params["clientUserID"].simple_value)
    # endregion


