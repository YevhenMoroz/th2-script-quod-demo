import os

from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import convert_to_get_request, wrap_message, create_check_rule, wrap_filter
from quod_qa.wrapper.ret_wrappers import verifier
from stubs import Stubs
from quod_qa.wrapper.RestApiManager import RestApiManager
from quod_qa.wrapper.RestApiMessages import RestApiMessages


def execute(report_id):

    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

    api_message = RestApiMessages()
    api_manager = RestApiManager(session_alias='rest_wa315luna', case_id=case_id)
    tested_client = "test_api_client"

    # # region Pre-Condition
    user_params = {
        "userConfirmFollowUp": "false",
        "userID": "adm_rest",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "headOfDesk": "false",
    }
    api_message.modify_user(user_params)
    api_manager.send_post_request(api_message)
    # end region

    # region disable Client and check result - step 2
    api_message.disable_client(client_id=tested_client)
    api_manager.send_post_request(api_message=api_message)

    api_message.find_all_client()
    client_status_after_disable = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                                   response_name="AccountGroupResponse",
                                                                   expected_entity_name=tested_client,
                                                                   entity_field_id="accountGroupID")
    print(client_status_after_disable)
    verifier(case_id=case_id,
             event_name="Check Client Status after send disable request",
             expected_value="false",
             actual_value=client_status_after_disable["alive"].simple_value)
    # end region

    # region enable Client and check result - step 3
    api_message.enable_client(client_id=tested_client)
    api_manager.send_post_request(api_message)

    api_message.find_all_client()
    client_status_after_enable = api_manager.get_response_details(response=api_manager.send_get_request(api_message),
                                                                  response_name="AccountGroupResponse",
                                                                  expected_entity_name=tested_client,
                                                                  entity_field_id="accountGroupID")
    verifier(case_id=case_id,
             event_name="Check Client Status after send enable request",
             expected_value="true",
             actual_value=client_status_after_enable["alive"].simple_value)
    # end region

    # region Create new Client and check result - step 4
    create_params = {
        "accountMgrUserID": "QA4",
        "accountGroupName": "test_api_client_5360",
        "accountMgrDeskID": 1,
        "clientAccountGroupID": "test_api_client_5360",
        "accountGroupID": "test_api_client_5360",
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
                                                         expected_entity_name="test_api_client_5360",
                                                         entity_field_id="accountGroupID")
    verifier(case_id=case_id,
             event_name="Check that new client is created after send create request",
             expected_value="true",
             actual_value=new_client_status["alive"].simple_value)
    # end region
