from th2_grpc_common.common_pb2 import ConnectionID

from custom.basic_custom_actions import wrap_message
from test_framework.old_wrappers.ret_wrappers import verifier
from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest, SubmitMessageMultipleResponseRequest, \
    ExpectedMessage
from custom import basic_custom_actions as bca

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime


def test_nos_method(report_id):
    case_id = bca.create_event('QAP-5529', report_id)
    api = Stubs.act_rest
    trading_conn = 'trading_ret'
    ws_conn = 'api_session_ret'
    checkpoint1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
    checkpoint_id1 = checkpoint1.checkpoint
    new_order_params = {
        'ClOrdID': bca.client_orderid(9),
        'Side': 'Buy',
        'OrdType': 'Limit',
        'Price': 1,
        'Currency': 'INR',
        'TimeInForce': 'Day',
        'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
        'ClientAccountGroupID': 'HAKKIM',
        'OrdQty': 100,
        'PosValidity': "Delivery",
        'Instrument': {
            'InstrSymbol': 'INF277K015L8',
            'SecurityID': '541794',
            'SecurityIDSource': 'EXC',
            'InstrType': 'Equity',
            'SecurityExchange': 'XBOM'
        }

    }

    api.submitNewOrderSingle(SubmitMessageRequest(message=bca.wrap_message(content=new_order_params,
                                                                           message_type='NewOrderSingle',
                                                                           session_alias='trading_ret')))

    content = {
        "_type": "OrderUpdate",
        "AvgPrice": 0,
        "ClOrdID": "*",
        "ClientAccountGroupID": "HAKKIM",
        "CumQty": 0,
        "Currency": "INR",
        "ExecType": "Open",
        "LeavesQty": 100,
        "OrdID": '*',
        "OrdQty": 100,
        "OrdType": "Limit",
        "OrderStatus": "Open",
        "Price": 1,
        "SettlDate": "*",
        "Side": "Buy",
        "TimeInForce": "Day",
        "TransactTime": "*",
        "PosValidity": "Delivery"
    }
    Stubs.verifier.submitCheckRule(
        request=bca.create_check_rule(
            'OrderUpdate',
            bca.wrap_filter(content, 'OrderUpdate', ["OrderStatus", "ExecType"]),
            checkpoint_id1, ws_conn, case_id
        ),

    )

    modify_params = {
        'ClOrdID': new_order_params['ClOrdID'],
        'Side': new_order_params['Side'],
        'OrdType': new_order_params['OrdType'],
        'ClientAccountGroupID': new_order_params['ClientAccountGroupID'],
        'OrdQty': new_order_params['OrdQty'],
        'Instrument': new_order_params['Instrument'],
        'Price': new_order_params['Price'],
        'PosValidity': 'TP2'
    }
    modify_request = SubmitMessageMultipleResponseRequest(
        message=wrap_message(modify_params, 'OrderModificationRequest', trading_conn),
        parent_event_id=case_id,
        description="Send OrderModificationRequest",
        expected_messages=[

            ExpectedMessage(
                message_type='OrderUpdate',
                key_fields={"PosValidity": "TPlus2"},
                connection_id=ConnectionID(session_alias=ws_conn)
            )
        ]
    )
    modify_messages = Stubs.api_service.submitMessageWithMultipleResponse(modify_request).response_message
    verifier(case_id=case_id,
             event_name="Check that PosValidity field is modified",
             expected_value="TPlus2",
             actual_value=modify_messages[0].fields["PosValidity"].simple_value)


# Main method
def execute(report_id):
    test_nos_method(report_id)
