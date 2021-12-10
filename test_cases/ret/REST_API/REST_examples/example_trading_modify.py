from th2_grpc_common.common_pb2 import ConnectionID

from custom.basic_custom_actions import wrap_message
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages
from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest, ExpectedMessage, \
    SubmitMessageMultipleResponseRequest
from custom import basic_custom_actions as bca

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime


class TestCase:
    def __init__(self, report_id):

        self.case_id = bca.create_event('Example REST Modify message', report_id)
        self.api = Stubs.act_rest
        self.connectivity = 'api_session_ret'

    def test_nos_method(self):

        nos_params = {
            'ClOrdID': bca.client_orderid(9),
            'Side': 'Buy',
            'OrdType': 'Limit',
            'Price': 10,
            'Currency': 'INR',
            'TimeInForce': 'Day',
            'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
            'ClientAccountGroupID': 'HAKKIM',
            'OrdQty': 3333,
            'Instrument': {
                'InstrSymbol': 'INE467B01029',
                'SecurityID': '28612',
                'SecurityIDSource': 'EXC',
                'InstrType': 'Equity',
                'SecurityExchange': 'XNSE'
            }
        }

        request = SubmitMessageMultipleResponseRequest(
            message=wrap_message(nos_params, 'NewOrderSingle', 'trading_ret'),
            parent_event_id=self.case_id,
            description="Send NewOrderSingle",
            expected_messages=[

                ExpectedMessage(
                    message_type='OrderUpdate',
                    key_fields={"OrderStatus": "Open"},
                    connection_id=ConnectionID(session_alias='api_session_ret')
                )
            ]
        )
        messages = Stubs.api_service.submitMessageWithMultipleResponse(request).response_message
        print(messages)

        modify_params = {
            'ClOrdID': nos_params['ClOrdID'],
            'Side': nos_params['Side'],
            'OrdType': nos_params['OrdType'],
            'ClientAccountGroupID': nos_params['ClientAccountGroupID'],
            'OrdQty': nos_params['OrdQty'],
            'Instrument': nos_params['Instrument'],
            'Price': 30

        }
        modify_request = SubmitMessageMultipleResponseRequest(
            message=wrap_message(modify_params, 'OrderModificationRequest', 'trading_ret'),
            parent_event_id=self.case_id,
            description="Send OrderModificationRequest",
            expected_messages=[

                ExpectedMessage(
                    message_type='OrderModificationReply',
                    key_fields={"ReplyType": "Accepted"},
                    connection_id=ConnectionID(session_alias='trading_ret')
                ),

                ExpectedMessage(
                    message_type='OrderUpdate',
                    key_fields={"OrderStatus": "Open"},
                    connection_id=ConnectionID(session_alias='api_session_ret')
                )
            ]
        )
        modify_messages = Stubs.api_service.submitMessageWithMultipleResponse(modify_request).response_message
        print(modify_messages)
    # Main method
    def execute(self):
        self.test_nos_method()


if __name__ == '__main__':
    pass
