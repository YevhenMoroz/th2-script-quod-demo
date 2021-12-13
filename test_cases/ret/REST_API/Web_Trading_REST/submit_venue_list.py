from th2_grpc_common.common_pb2 import ConnectionID

from custom.basic_custom_actions import wrap_message
from custom import verifier
from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest, ExpectedMessage, \
    SubmitMessageMultipleResponseRequest
from custom import basic_custom_actions as bca

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime, timedelta


class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('QAP_6224', report_id)
        self.api = Stubs.act_rest
        self.http_conn = 'rest_wt320kuiper'
        self.ws_conn = 'api_session_320kuiper'
        self.exception_error = "11620 unknown client Tony / 11505 Runtime error (no VAccountGroup with keys [" \
                               "undefined] in cache or database)"

    def test_nos_method(self):

        time_now = datetime.utcnow()
        nos_params = {
            'ClOrdID': bca.client_orderid(9),
            'Side': 'Buy',
            'OrdType': 'Limit',
            'Price': 104,
            'Currency': 'INR',
            'TimeInForce': 'GoodTillDate',
            'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
            'ExpireDate': (time_now + timedelta(days=2)).strftime("%Y%m%d"),
            'ClientAccountGroupID': 'Tony',
            'OrdQty': 4444,
            'Instrument': {
                'InstrSymbol': 'INE467B01029',
                'SecurityID': '28612',
                'SecurityIDSource': 'EXC',
                'InstrType': 'Equity',
                'SecurityExchange': 'XNSE'
            }
        }

        request = SubmitMessageMultipleResponseRequest(
            message=wrap_message({}, 'VenueListRequest', self.http_conn),
            parent_event_id=self.case_id,
            description="Send VenueListRequest",
            expected_messages=[

                ExpectedMessage(
                    message_type='ReplyType',
                    key_fields={"ReplyType": "Accepted"},
                    connection_id=
                    ConnectionID(session_alias=self.http_conn)
                )
            ]
        )
        messages = Stubs.api_service.submitMessageWithMultipleResponse(request).response_message
        print(messages)

    # Main method
    def execute(self):
        self.test_nos_method()


if __name__ == '__main__':
    pass
