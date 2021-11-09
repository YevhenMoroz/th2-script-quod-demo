from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageMultipleResponseRequest, ExpectedMessage
from th2_grpc_common.common_pb2 import ConnectionID
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import wrap_message, create_event
from stubs import Stubs


def execute(report_id):
    case_id = create_event("md test", report_id)
    md_params = {
        "MDReqID": bca.client_orderid(10),
        "SubscriptionRequestType": "Snapshot",
        "MDReqInstruments":
            [
                {
                    "Instrument":
                        {
                            'InstrSymbol': 'INF277K015L8',
                            'SecurityID': '541794',
                            'SecurityIDSource': 'EXC',
                            'InstrType': 'Equity',
                            'SecurityExchange': 'XBOM'
                        }
                }
            ]
    }
    request = SubmitMessageMultipleResponseRequest(
        message=wrap_message(md_params, 'MarketDataRequest', 'trading_ret'),
        parent_event_id=case_id,
        description="Send MarketDataRequest",
        expected_messages=[
            ExpectedMessage(
                message_type='MarketDataReply',
                key_fields={"ReplyType": "Accepted"},
                connection_id=ConnectionID(session_alias='trading_ret')
            )
            , ExpectedMessage(
                message_type='MarketDataSnapshotFullRefresh',
                key_fields={"MDReqID": md_params['MDReqID']},
                connection_id=ConnectionID(session_alias='api_session_ret')
            )
        ]
    )
    messages = Stubs.api_service.submitMessageWithMultipleResponse(request).response_message
    print(messages)