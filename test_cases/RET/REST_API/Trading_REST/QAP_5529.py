from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from custom import basic_custom_actions as bca

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime


def test_nos_method(report_id):
    case_id = bca.create_event('QAP-5529', report_id)
    api = Stubs.act_rest
    connectivity = 'api_session_ret'
    checkpoint1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
    checkpoint_id1 = checkpoint1.checkpoint
    nos_params = {
        'ClOrdID': bca.client_orderid(9),
        'Side': 'Buy',
        'OrdType': 'Limit',
        'Price': 1,
        'Currency': 'INR',
        'TimeInForce': 'Day',
        'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
        'ClientAccountGroupID': 'HAKKIM',
        'OrdQty': 100,
        #'SettlCurrency': "USD",
        'PosValidity': "Delivery",
        'Instrument': {
            'InstrSymbol': 'INF277K015L8',
            'SecurityID': '541794',
            'SecurityIDSource': 'EXC',
            'InstrType': 'Equity',
            'SecurityExchange': 'XBOM'
        }

    }

    # response = api.submitNewOrderSingle(
    #     request=SubmitMessageRequest(message=bca.message_to_grpc('NewOrderSingle', nos_params, 'trading_ret')))
    response = api.submitNewOrderSingle(SubmitMessageRequest(message=bca.wrap_message(content=nos_params,
                                                             message_type='NewOrderSingle',
                                                             session_alias='trading_ret')))

    print(response)
    content = {
        "_type": "OrderUpdate",
        "AvgPrice": 0,
        "ClOrdID": "*",
        "ClientAccountGroupID": "HAKKIM",
        "CumQty": 0,
        "Currency": "INR",
        "ExecType": "Open",
        "Instrument": nos_params['Instrument'],
        "LeavesQty": 3333,
        "OrdID": '*',
        "OrdQty": 3333,
        "OrdType": "Limit",
        "OrderStatus": "Open",
        "Price": 10,
        "SettlDate": "2021-09-27",
        "Side": "Sell",
        "TimeInForce": "Day",
        "TransactTime": "*",
        "PosValidity": "Delivery"
    }
    Stubs.verifier.submitCheckRule(
        request=bca.create_check_rule(
            'OrderUpdate',
            bca.wrap_filter(content, 'OrderUpdate', ["OrderStatus", "ExecType"]),
            checkpoint_id1, connectivity, case_id
        ),

    )


# Main method
def execute(report_id):
    test_nos_method(report_id)
