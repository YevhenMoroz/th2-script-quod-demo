from th2_grpc_common.common_pb2 import ConnectionID

from custom.basic_custom_actions import wrap_message
from test_cases.wrapper.ret_wrappers import verifier
from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest, ExpectedMessage, \
    SubmitMessageMultipleResponseRequest
from custom import basic_custom_actions as bca

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime, timedelta


class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('QAP_6572', report_id)
        self.api = Stubs.act_rest
        self.http_conn = 'rest_wt320kuiper'
        self.ws_conn = 'api_session_320kuiper'

    def get_historical_market_data(self):
        time_now = datetime.utcnow()
        params = {
            "StartTime": "2022-01-20T10:07:59.588Z",
            "EndTime": "2022-01-29T10:07:59Z",
            "Instrument": {'InstrSymbol': 'SPICEJET-IQ[NSE]',
                           'SecurityID': '11564',
                           'SecurityIDSource': 'EXC',
                           'InstrType': 'EQU',
                           }
        }

        request = SubmitMessageMultipleResponseRequest(
            message=wrap_message(params, 'HistoricalMarketDataRequest', self.http_conn),
            parent_event_id=self.case_id,
            description="Send HistoricalMarketDataRequest",
            expected_messages=[

                ExpectedMessage(
                    message_type='HistoricalMarketDataReply',
                    key_fields={},
                    connection_id=
                    ConnectionID(session_alias=self.http_conn)
                )
            ]
        )
        messages = Stubs.api_service.submitMessageWithMultipleResponse(request).response_message
        print(messages)

    # Main method
    def execute(self):
        self.get_historical_market_data()


if __name__ == '__main__':
    pass
