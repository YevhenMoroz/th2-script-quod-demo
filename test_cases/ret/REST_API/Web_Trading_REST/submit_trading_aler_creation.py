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
            "AlertType": "Repeating",
            "AlertOperator": "GreaterThan",
            "AlertUnit": "Absolute",
            "FieldName": "BestBid",
            "AlertValue": "104",
            "Instrument": {"SecurityID": '28612',
                           "SecurityIDSource": 'EXC',
                           "InstrSymbol": 'INE467B01029',
                           "InstrType": "Equity"}
        }

        request = SubmitMessageMultipleResponseRequest(
            message=wrap_message(nos_params, 'TradingAlertCreationRequest', self.http_conn),
            parent_event_id=self.case_id,
            description="Send TradingAlertCreationRequest",
            expected_messages=[

                ExpectedMessage(
                    message_type='ReplyType',
                    key_fields={"ReplyType": "Accepted"},
                    connection_id=
                    ConnectionID(session_alias=self.ws_conn)
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
