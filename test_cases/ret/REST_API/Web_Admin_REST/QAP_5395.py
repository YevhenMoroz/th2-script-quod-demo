import os

from custom import basic_custom_actions as bca
from test_framework.old_wrappers.ret_wrappers import verifier
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


def execute(report_id):
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

    api_message = RestApiMessages()
    api_manager = RestApiManager(session_alias='rest_wa315luna', case_id=case_id)

    # region Pre_Condition

    create_params = {
        "accountGroupName": "test_api_client_5395",
        "clientAccountGroupID": "test_api_client_5395",
        "accountGroupID": "test_api_client_5395",
        "accountType": "HT",
        "accountScheme": "S",
        "transactionType": "C",
        "discloseExec": "M",
        "clearingAccountType": "FIR",
        "allocationInst": "MAN"
    }
    api_message.create_client(create_params)
    api_manager.send_post_request(api_message)

    api_message.find_all_client()
    new_client_status = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                         response_name="AccountGroupResponse",
                                                         expected_entity_name="test_api_client_5395",
                                                         entity_field_id="accountGroupID")

    verifier(case_id=case_id,
             event_name="Check that new client is created",
             expected_value="true",
             actual_value=new_client_status["alive"].simple_value)

    modify_user_account_group = {
        "userConfirmFollowUp": "false",
        "userID": "user_loc",
        "userEmail": "q",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "permRoleID": 10011,
        "headOfDesk": "false",
        "preferredCommMethod": "EML",
        "locationID": 6,
        "userRolesAccountGroup": [
            {
                "accountGroupID": "test_api_client_5395",
                "userRoleAccountGroupType": "U"
            }
        ]
    }
    api_message.modify_user(params=modify_user_account_group)
    api_manager.send_post_request(api_message=api_message)

    api_message.find_all_user()
    user_account_group = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                          response_name="UserResponse",
                                                          expected_entity_name="user_loc",
                                                          entity_field_id="userID")

    verifier(case_id=case_id,
             event_name="Check userRolesAccountGroup",
             expected_value="test_api_client_5395",
             actual_value=user_account_group["userRolesAccountGroup"].list_value.values[0].message_value.fields[
                 "accountGroupID"].simple_value)
    # endregion

    modify_user_hierarchy = {
        "userConfirmFollowUp": "false",
        "userID": "adm_rest",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "zoneID": "6",
        "headOfDesk": "false",
    }
    api_message.modify_user(params=modify_user_hierarchy)
    api_manager.send_post_request(api_message=api_message)

    api_message.find_all_user()
    user_hierarchy = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                      response_name="UserResponse",
                                                      expected_entity_name="adm_rest",
                                                      entity_field_id="userID")

    # print(type(user_params))
    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel",
             expected_value="6",
             actual_value=user_hierarchy["zoneID"].simple_value)

    # region Get and verify clients according with HierarchicalLevel - step 1
    api_message.find_all_client()
    client_status_step1 = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                           response_name="AccountGroupResponse",
                                                           expected_entity_name="test_api_client_5395",
                                                           entity_field_id="accountGroupName")
    print(client_status_step1)
    verifier(case_id=case_id,
             event_name="Check that new client is appeared for adm_rest user",
             expected_value="true",
             actual_value=client_status_step1["alive"].simple_value)
    # endregion

    # region Modify client
    modify_client_step3 = {
        "accountMgrUserID": "user_desk",
        "accountGroupName": "client_api_test_5395",
        "accountMgrDeskID": 5,
        "clientAccountGroupID": "client_api_test_5395",
        "accountGroupID": "client_api_test_5395",
        "accountType": "HT",
        "accountScheme": "S",
        "transactionType": "C",
        "discloseExec": "M",
        "accountMgrRoleID": "ADM",
        "clearingAccountType": "FIR",
        "allocationInst": "MAN"
    }
    api_message.modify_client(modify_client_step3)
    api_manager.send_post_request(api_message)

    api_message.find_all_client()
    client_fields_step3 = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                           response_name="AccountGroupResponse",
                                                           expected_entity_name="test_api_client_5395",
                                                           entity_field_id="accountGroupName")
    verifier(case_id=case_id,
             event_name="Check accountMgrUserID",
             expected_value="user_desk",
             actual_value=client_fields_step3["accountMgrUserID"].simple_value)
    verifier(case_id=case_id,
             event_name="Check accountMgrDeskID",
             expected_value="5",
             actual_value=client_fields_step3["accountMgrDeskID"].simple_value)

    # endregion

    api_message.modify_user_to_site()
    api_manager.send_post_request(api_message)
