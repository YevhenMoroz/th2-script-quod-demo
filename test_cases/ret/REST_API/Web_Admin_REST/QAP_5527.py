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

    # region Pre-Condition Set hierarchy level - Test_Institution(id=3)
    institution_params = {

        "userConfirmFollowUp": "false",
        "userID": "adm_rest",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "headOfDesk": "false",
        "institutionID": 3
    }
    api_message_site_adm.modify_user(institution_params)
    api_manager_site_adm.send_post_request(api_message_site_adm)

    # region Send Get request and verify result
    api_message_tested_user.find_all_user()
    user_params = api_manager_tested_user.get_response_details(
        response=api_manager_tested_user.send_get_request(api_message_tested_user),
        response_name="UserResponse",
        expected_entity_name="adm_rest",
        entity_field_id="userID")

    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel after change on institutionID=3",
             expected_value="3",
             actual_value=user_params["institutionID"].simple_value)
    # endregion

    # region Set Test_Institution(id3), Test_Zone(id=6), Test_Location(id=6) and Test_Desk(id=6) - step 2
    modify_params_adm_rest = {
        "userConfirmFollowUp": "false",
        "userID": "adm_rest",
        "userEmail": "q",
        "clientUserID": "QAP-5444",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "permRoleID": 10007,
        "institutionID": 3,
        "zoneID": 6,
        "locationID": 6,
        "headOfDesk": "false",
        "preferredCommMethod": "EML",
        "deskUserRole": [
            {
                "deskID": 5
            }
        ]
    }
    api_message_tested_user.modify_user(modify_params_adm_rest)
    api_manager_tested_user.send_post_request(api_message_tested_user)
    # endregion

    # region Get and Verify - step 2
    api_message_tested_user.find_all_user()
    user_params = api_manager_tested_user.get_response_details(
        response=api_manager_tested_user.send_get_request(api_message_tested_user),
        response_name="UserResponse",
        expected_entity_name="adm_rest",
        entity_field_id="userID")
    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel for adm_rest",
             expected_value="3",
             actual_value=user_params['institutionID'].simple_value)
    zone_sts = ''
    location_sts = ''
    desk_sts = ''
    if user_params['zoneID'] == 6:
        zone_sts = 'adm_rest have hierarchy Zone'
    if user_params['locationID'] == 6:
        location_sts = 'adm_rest have hierarchy Location'
    if user_params['deskUserRole'] == 6:
        desk_sts = 'adm_rest have hierarchy Desk'

    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel for adm_rest that not assigned to zone",
             expected_value='',
             actual_value=zone_sts)
    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel for adm_rest that not assigned to location",
             expected_value='',
             actual_value=location_sts)
    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel for adm_rest that not assigned to desk",
             expected_value='',
             actual_value=desk_sts)
    # endregion

    # region Set empty institution, zone, location and desk hierarchy - step 3
    # This step not working, because have a bug according with "User Admin Data Segregation
    # User with hierarchical level = Institution should not set hierarchy level = Site
    # modify_params_no_hierarchy = {
    #     "userConfirmFollowUp": "false",
    #     "userID": "adm_rest",
    #     "userEmail": "q",
    #     "clientUserID": "QAP-5444",
    #     "useOneTimePasswd": "false",
    #     "pingRequired": "false",
    #     "generatePassword": "false",
    #     "generatePINCode": "false",
    #     "permRoleID": 10007,
    #     "headOfDesk": "false",
    #     "preferredCommMethod": "EML",
    # }
    # api_message_tested_user.modify_user(modify_params_no_hierarchy)
    # api_manager_tested_user.send_post_request(api_message_tested_user)
    # # endregion
    #
    # # region Get and Verify - step 3
    # api_message_tested_user.find_all_user()
    # user_params = api_manager_tested_user.get_response_details(
    #     response=api_manager_tested_user.send_get_request(api_message_tested_user),
    #     response_name="UserResponse",
    #     expected_entity_name="adm_rest",
    #     entity_field_id="userID")
    # verifier(case_id=case_id,
    #          event_name="Check User HierarchicalLevel for adm_rest",
    #          expected_value="3",
    #          actual_value=user_params['institutionID'].simple_value)
    # new_zone_sts = ''
    # new_location_sts = ''
    # new_desk_sts = ''
    # if user_params['zoneID'] == 6:
    #     new_zone_sts = 'adm_rest have hierarchy Zone'
    # if user_params['locationID'] == 6:
    #     new_location_sts = 'adm_rest have hierarchy Location'
    # if user_params['deskUserRole'] == 6:
    #     new_desk_sts = 'adm_rest have hierarchy Desk'
    #
    # verifier(case_id=case_id,
    #          event_name="Check User HierarchicalLevel for adm_rest that not assigned to zone",
    #          expected_value='',
    #          actual_value=new_zone_sts)
    # verifier(case_id=case_id,
    #          event_name="Check User HierarchicalLevel for adm_rest that not assigned to location",
    #          expected_value='',
    #          actual_value=new_location_sts)
    # verifier(case_id=case_id,
    #          event_name="Check User HierarchicalLevel for adm_rest that not assigned to location",
    #          expected_value='',
    #          actual_value=new_desk_sts)
    # endregion