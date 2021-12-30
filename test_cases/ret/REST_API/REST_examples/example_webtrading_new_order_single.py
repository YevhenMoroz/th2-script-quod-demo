from th2_grpc_common.common_pb2 import ConnectionID

from custom.basic_custom_actions import wrap_message
from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest, ExpectedMessage, \
    SubmitMessageMultipleResponseRequest
from custom import basic_custom_actions as bca

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime, timedelta


class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('Example REST NewOrderSingle', report_id)
        self.api = Stubs.act_rest
        self.connectivity = 'api_session_ret'

    def test_nos_method(self):

        time_now = datetime.utcnow()
        nos_params = {
            'ClOrdID': bca.client_orderid(9),
            'Side': 'Buy',
            'OrdType': 'Limit',
            'Price': 103,
            'Currency': 'INR',
            'TimeInForce': 'GoodTillDate',
            'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
            'ExpireDate': (time_now + timedelta(days=2)).strftime("%Y%m%d"),
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
            message=wrap_message(nos_params, 'NewOrderSingle', 'rest_wt320kuiper'),
            parent_event_id=self.case_id,
            description="Send NewOrderSingle",
            expected_messages=[

                ExpectedMessage(
                    message_type='OrderUpdate',
                    key_fields={"OrderStatus": "Open"},
                    connection_id=
                    ConnectionID(session_alias='api_session_320kuiper')
                )
            ]
        )
        messages = Stubs.api_service.submitMessageWithMultipleResponse(request).response_message
        print(messages)
        # print(type(messages))
        # print(messages[0].fields["AvgPrice"])


    # Main method
    def execute(self):
        self.test_nos_method()


if __name__ == '__main__':
    pass
