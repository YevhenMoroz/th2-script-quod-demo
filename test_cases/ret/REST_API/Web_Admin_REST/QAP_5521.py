import os

from custom import basic_custom_actions as bca
from test_framework.old_wrappers.ret_wrappers import verifier
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


def execute(report_id):
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

    api_message = RestApiMessages()
    api_manager = RestApiManager(session_alias='rest_wa315luna_site_admin', case_id=case_id)

    # region Set hierarchy level Test_Desk(id=6) - step 2
    desk_params = {
        "userConfirmFollowUp": "false",
        "userID": "user_adm",
        "userEmail": "q",
        "clientUserID": "QAP-5441",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "permRoleID": 10007,
        "preferredCommMethod": "EML",
        "deskUserRole": [
            {
                "deskID": 5
            }
        ]
    }
    api_message.modify_user(desk_params)
    api_manager.send_post_request(api_message)
    # endregion

    # region Send Get request and verify result - step 2
    api_message.find_all_user()
    user_params = api_manager.get_response_details(
        response=api_manager.send_get_request(api_message),
        response_name="UserResponse",
        expected_entity_name="user_adm",
        entity_field_id="userID")
    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel after change on deskID=5",
             expected_value="5",
             actual_value=user_params["deskUserRole"].list_value.values[0].message_value.fields["deskID"].simple_value)
    # endregion

    # region Set hierarchical level Test_Location(id=6) - step 3
    location_params = {
        "userConfirmFollowUp": "false",
        "userID": "user_adm",
        "userEmail": "q",
        "clientUserID": "QAP-5441",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "permRoleID": 10007,
        "preferredCommMethod": "EML",
        "locationID": 6
    }
    api_message.modify_user(location_params)
    api_manager.send_post_request(api_message)

    # region Send Get request and verify result - step 3
    api_message.find_all_user()
    user_params = api_manager.get_response_details(
        response=api_manager.send_get_request(api_message),
        response_name="UserResponse",
        expected_entity_name="user_adm",
        entity_field_id="userID")

    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel after change on locationID=6",
             expected_value="6",
             actual_value=user_params["locationID"].simple_value)
    # endregion

    # region Set hierarchical level Test_Zone(id=6) - step 4
    zone_params = {
        "userConfirmFollowUp": "false",
        "userID": "user_adm",
        "userEmail": "q",
        "clientUserID": "QAP-5441",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "permRoleID": 10007,
        "preferredCommMethod": "EML",
        "zoneID": 6
    }
    api_message.modify_user(zone_params)
    api_manager.send_post_request(api_message)

    # region Send Get request and verify result - step 4
    api_message.find_all_user()
    user_params = api_manager.get_response_details(
        response=api_manager.send_get_request(api_message),
        response_name="UserResponse",
        expected_entity_name="user_adm",
        entity_field_id="userID")

    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel after change on zoneID=6",
             expected_value="6",
             actual_value=user_params["zoneID"].simple_value)
    # endregion

    # region Set hierarchical level Test_Institution(id=3) - step 5
    institution_params = {
        "userConfirmFollowUp": "false",
        "userID": "user_adm",
        "userEmail": "q",
        "clientUserID": "QAP-5441",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "permRoleID": 10007,
        "preferredCommMethod": "EML",
        "institutionID": 3
    }
    api_message.modify_user(institution_params)
    api_manager.send_post_request(api_message)
    # endregion

    # region Send Get request and verify result - step 5
    api_message.find_all_user()
    user_params = api_manager.get_response_details(
        response=api_manager.send_get_request(api_message),
        response_name="UserResponse",
        expected_entity_name="user_adm",
        entity_field_id="userID")

    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel after change on institutionID=3",
             expected_value="3",
             actual_value=user_params["institutionID"].simple_value)
    # endregion

    # region Set hierarchical level Site - step 6
    site_params = {
        "userConfirmFollowUp": "false",
        "userID": "user_adm",
        "userEmail": "q",
        "clientUserID": "QAP-5441",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "permRoleID": 10007,
        "preferredCommMethod": "EML",
    }
    api_message.modify_user(site_params)
    api_manager.send_post_request(api_message)
    # endregion

    # region Send Get request and verify result - step 6
    api_message.find_all_user()
    user_params = api_manager.get_response_details(
        response=api_manager.send_get_request(api_message),
        response_name="UserResponse",
        expected_entity_name="user_adm",
        entity_field_id="userID")

    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel after change on Site, that user was not assign to Institution",
             expected_value="",
             actual_value=user_params["institutionID"].simple_value)
    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel after change on Site, that user was not assign to Zone",
             expected_value="",
             actual_value=user_params["zoneID"].simple_value)
    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel after change on Site, that user was not assign to Location",
             expected_value="",
             actual_value=user_params["locationID"].simple_value)
    try:
        desk_id = user_params["deskUserRole"].list_value.values[0].message_value.fields["deskID"].simple_value
        desk_sts = 'User assigned to certain Desk'
        verifier(case_id=case_id,
                 event_name="Check User HierarchicalLevel after change on Site, that user was not assign to Desk",
                 expected_value=desk_sts,
                 actual_value=desk_id)
    except:
        verifier(case_id=case_id,
                 event_name="Check User HierarchicalLevel after change on Site, that user was not assign to Desk",
                 expected_value='',
                 actual_value='')
    # endregion
