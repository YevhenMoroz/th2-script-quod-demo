import os
from th2_grpc_common.common_pb2 import ConnectionID

from custom.basic_custom_actions import wrap_message
from custom import verifier
from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageMultipleResponseRequest, ExpectedMessage
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages
from custom import basic_custom_actions as bca
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime


def execute(report_id):
    case_id = bca.create_event(os.path.basename(__file__)[:-3], report_id)
    api = Stubs.act_rest
    trading_conn = 'trading_ret'
    ws_conn = 'api_session_ret'

    api_messages_webadmin = RestApiMessages()
    api_manager_webadmin = RestApiManager(session_alias='rest_wa315luna_site_admin', case_id=case_id)

    # region Pre-Condition

    # region Set hierarchical level Test_Desk(id=5) for the api_client and verify result
    client_modify_params = {
        "accountGroupName": "api_client",
        "accountMgrDeskID": 5,
        "clientAccountGroupID": "api_client",
        "accountGroupID": "api_client",
        "accountType": "HT",
        "accountScheme": "S",
        "transactionType": "C",
        "discloseExec": "M",
        "clearingAccountType": "FIR",
        "allocationInst": "MAN",
        "alive": "true"
    }
    api_messages_webadmin.modify_client(client_modify_params)
    api_manager_webadmin.send_post_request(api_messages_webadmin)

    api_messages_webadmin.find_all_client()
    client_params = api_manager_webadmin.get_response_details(
        response=api_manager_webadmin.send_get_request(api_messages_webadmin),
        response_name="AccountGroupResponse",
        expected_entity_name="api_client",
        entity_field_id="accountGroupID")
    try:
        verifier(case_id=case_id,
                 event_name="Check Client HierarchicalLevel after change on accountMgrDeskId=5",
                 expected_value="5",
                 actual_value=client_params["accountMgrDeskID"].simple_value)
    except:
        bca.create_event(f'Fail test event. Response is empty',
                         status='FAILED',
                         parent_id=case_id)
    # endregion

    # region Set hierarchical level Test_Desk(id=5) for the trading_rest user and verify result
    api_user_modify_params = {
        "userConfirmFollowUp": "false",
        "userID": "trading_rest",
        "userEmail": "trading_rest",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "permRoleID": 10011,
        "counterpartID": 1,
        "headOfDesk": "false",
        "preferredCommMethod": "EML",
        "deskUserRole": [
            {
                "deskID": 5
            }
        ]
    }
    api_messages_webadmin.modify_user(api_user_modify_params)
    api_manager_webadmin.send_post_request(api_messages_webadmin)

    api_messages_webadmin.find_all_user()
    user_params = api_manager_webadmin.get_response_details(
        response=api_manager_webadmin.send_get_request(api_messages_webadmin),
        response_name="UserResponse",
        expected_entity_name="trading_rest",
        entity_field_id="userID")

    try:
        verifier(case_id=case_id,
                 event_name="Check User HierarchicalLevel after change on deskID=5",
                 expected_value="5",
                 actual_value=user_params["deskUserRole"].list_value.values[0].message_value.fields[
                     "deskID"].simple_value)
    except:
        bca.create_event(f'Fail test event. User trading_rest not assign to Test_Desk(id=5)',
                         status='FAILED',
                         parent_id=case_id)
    # endregion
    # endregion

    # region Send new order and verify result - step 1

    new_order_params = {
        'ClOrdID': bca.client_orderid(9),
        'Side': 'Buy',
        'OrdType': 'Limit',
        'Price': 1,
        'Currency': 'INR',
        'TimeInForce': 'Day',
        'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
        'ClientAccountGroupID': "api_client",
        'OrdQty': 100,
        'Instrument': {
            'InstrSymbol': 'INF277K015L8',
            'SecurityID': '541794',
            'SecurityIDSource': 'EXC',
            'InstrType': 'Equity',
            'SecurityExchange': 'XBOM'
        }

    }
    new_order_single_request = SubmitMessageMultipleResponseRequest(
        message=wrap_message(new_order_params, 'NewOrderSingle', trading_conn),
        parent_event_id=case_id,
        description="Send NewOrderSingle",
        expected_messages=[

            ExpectedMessage(
                message_type='OrderUpdate',
                key_fields={"OrderStatus": "Open"},
                connection_id=ConnectionID(session_alias=ws_conn)
            ),
        ]
    )
    new_order_single_response = Stubs.api_service.submitMessageWithMultipleResponse(
        new_order_single_request).response_message
    #print(new_order_single_response)
    # endregion

    # api_user_modify_params = {
    #     "userConfirmFollowUp": "false",
    #     "userID": "trading_rest",
    #     "userEmail": "trading_rest",
    #     "useOneTimePasswd": "false",
    #     "pingRequired": "false",
    #     "generatePassword": "false",
    #     "generatePINCode": "false",
    #     "permRoleID": 10011,
    #     "counterpartID": 1,
    #     "headOfDesk": "false",
    #     "preferredCommMethod": "EML",
    #     "deskUserRole": [
    #         {
    #             "deskID": 1
    #         }
    #     ]
    # }
    # api_messages_webadmin.modify_user(api_user_modify_params)
    # api_manager_webadmin.send_post_request(api_messages_webadmin)
    #
    # api_messages_webadmin.find_all_user()
    # user_params = api_manager_webadmin.get_response_details(
    #     response=api_manager_webadmin.send_get_request(api_messages_webadmin),
    #     response_name="UserResponse",
    #     expected_entity_name="trading_rest",
    #     entity_field_id="userID")
    #
    # try:
    #     verifier(case_id=case_id,
    #              event_name="Check User HierarchicalLevel after change on deskID=1",
    #              expected_value="1",
    #              actual_value=user_params["deskUserRole"].list_value.values[0].message_value.fields[
    #                  "deskID"].simple_value)
    # except:
    #     bca.create_event(f'Fail test event. User trading_rest not assign to RIN-DESK(id=1)',
    #                      status='FAILED',
    #                      parent_id=case_id)

    # new_order_params_step1 = {
    #     'ClOrdID': bca.client_orderid(9),
    #     'Side': 'Buy',
    #     'OrdType': 'Limit',
    #     'Price': 4,
    #     'Currency': 'INR',
    #     'TimeInForce': 'Day',
    #     'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
    #     'ClientAccountGroupID': "POOJA",
    #     'OrdQty': 123,
    #     'Instrument': {
    #         'InstrSymbol': 'INF277K015L8',
    #         'SecurityID': '541794',
    #         'SecurityIDSource': 'EXC',
    #         'InstrType': 'Equity',
    #         'SecurityExchange': 'XBOM'
    #     }
    #
    # }
    # new_order_single_request_step1 = SubmitMessageMultipleResponseRequest(
    #     message=wrap_message(new_order_params_step1, 'NewOrderSingle', trading_conn),
    #     parent_event_id=case_id,
    #     description="Send NewOrderSingle",
    #     expected_messages=[
    #
    #         ExpectedMessage(
    #             message_type='OrderUpdate',
    #             key_fields={"OrderStatus": "Rejected"},
    #             connection_id=ConnectionID(session_alias=ws_conn)
    #         ),
    #     ]
    # )
    # new_order_single_response_step1 = Stubs.api_service.submitMessageWithMultipleResponse(
    #     new_order_single_request_step1).response_message
    # print(new_order_single_response_step1)

    modify_params = {
        'ClOrdID': "791513093",
        'Side': new_order_params['Side'],
        'OrdType': new_order_params['OrdType'],
        'ClientAccountGroupID': "HAKKIM",
        'OrdQty': new_order_params['OrdQty'],
        'Instrument': new_order_params['Instrument'],
        'Price': 5

    }
    modify_request = SubmitMessageMultipleResponseRequest(
        message=wrap_message(modify_params, 'OrderModificationRequest', trading_conn),
        parent_event_id=case_id,
        description="Send OrderModificationRequest",
        expected_messages=[

            ExpectedMessage(
                message_type='OrderUpdate',
                key_fields={"OrderStatus": "Open"},
                connection_id=ConnectionID(session_alias=ws_conn)
            )
        ]
    )
    modify_messages = Stubs.api_service.submitMessageWithMultipleResponse(modify_request).response_message
    print(modify_messages)
