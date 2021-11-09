import os

from custom import basic_custom_actions as bca
from quod_qa.wrapper.ret_wrappers import verifier
from quod_qa.wrapper.RestApiManager import RestApiManager
from quod_qa.wrapper.RestApiMessages import RestApiMessages


def execute(report_id):
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

    api_message = RestApiMessages()
    api_manager = RestApiManager(session_alias='rest_wa315luna', case_id=case_id)

    # # region Pre-Condition
    #
    # # Create and Assign new Client to Desk - Test_Desk
    modify_client_params = {
        "accountGroupName": "client_for_test",
        "accountMgrDeskID": 5,
        "clientAccountGroupID": "client_for_test",
        "accountGroupID": "client_for_test",
        "accountType": "HT",
        "accountScheme": "S",
        "transactionType": "C",
        "discloseExec": "M",
        "clearingAccountType": "FIR",
        "allocationInst": "MAN"
    }
    api_message.modify_client(params=modify_client_params)
    api_manager.send_post_request(api_message=api_message)

    api_message.find_all_client()
    client_params = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                     response_name="AccountGroupResponse",
                                                     expected_entity_name="client_for_test",
                                                     entity_field_id="accountGroupName")
    print(client_params)
    verifier(case_id=case_id,
             event_name="Check new Client after send POST request ",
             expected_value="5",
             actual_value=client_params["accountMgrDeskID"].simple_value)

    # # Assign user adm_rest to HierarchicalLevel - Test_Institution
    modify_user_params = {
        "userConfirmFollowUp": "false",
        "userID": "adm_rest",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "zoneID": "6",
        "headOfDesk": "false",
    }
    api_message.modify_user(params=modify_user_params)
    api_manager.send_post_request(api_message=api_message)

    api_message.find_all_user()
    user_params = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                   response_name="UserResponse",
                                                   expected_entity_name="adm_rest",
                                                   entity_field_id="userID")
    print(user_params)

    # print(type(user_params))
    verifier(case_id=case_id,
             event_name="Check User HierarchicalLevel after send POST request",
             expected_value="6",
             actual_value=user_params["institutionID"].simple_value)
    # end Pre-Condition region

    # region Get list of Client - Step 1
    api_message.find_all_client()
    client_desk = api_manager.get_response_multiple_details(response=api_manager.send_get_request(api_message),
                                                            response_name="AccountGroupResponse",
                                                            entity_field_id="accountGroupName",
                                                            field_name="accountMgrDeskID")
    print(client_desk)
    verifier(case_id=case_id,
             event_name="Check Client HierarchicalLevel",
             expected_value="5",
             actual_value=client_desk['client_for_test'])
    # # end region

    # region Disable Client - step 2
    api_message.disable_client(client_id="client_for_test")
    api_manager.send_post_request(api_message=api_message)

    api_message.find_all_client()
    api_manager.send_get_request(api_message)
    client_after_disable = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                            response_name="AccountGroupResponse",
                                                            expected_entity_name="client_for_test",
                                                            entity_field_id="accountGroupName")

    print(client_after_disable)
    verifier(case_id=case_id,
             event_name="Check Client Status after disable",
             expected_value="false",
             actual_value=client_after_disable["alive"].simple_value)

    api_message.enable_client(client_id="client_for_test")
    api_manager.send_post_request(api_message)

    api_message.find_all_client()
    client_after_enable = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                           response_name="AccountGroupResponse",
                                                           expected_entity_name="client_for_test",
                                                           entity_field_id="accountGroupName")
    verifier(case_id=case_id,
             event_name="Check Client Status after enable",
             expected_value="true",
             actual_value=client_after_enable["alive"].simple_value)

    # region Create new Client and check result - step 4
    create_params = {
        "accountMgrUserID": "QA4",
        "accountGroupName": "test_api_client_5393",
        "accountMgrDeskID": 1,
        "clientAccountGroupID": "test_api_client_5393",
        "accountGroupID": "test_api_client_5393",
        "accountType": "HT",
        "accountScheme": "S",
        "transactionType": "C",
        "discloseExec": "M",
        "accountMgrRoleID": "HSD",
        "clearingAccountType": "FIR",
        "allocationInst": "MAN"
    }
    api_message.create_client(create_params)
    api_manager.send_post_request(api_message)

    api_message.find_all_client()
    new_client_status = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                         response_name="AccountGroupResponse",
                                                         expected_entity_name="test_api_client_5393",
                                                         entity_field_id="accountGroupID")
    verifier(case_id=case_id,
             event_name="Check that new client is created after send create request",
             expected_value="true",
             actual_value=new_client_status["alive"].simple_value)
    # end region
