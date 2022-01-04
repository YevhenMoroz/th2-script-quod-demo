from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from custom import basic_custom_actions as bca

import time


class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('Example REST MarketDataRequest', report_id)
        self.api = Stubs.act_rest
        self.connectivity = 'api_session_ret'

    def send_md_snapshot_request(self):
        checkpoint1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(self.case_id))
        checkpoint_id1 = checkpoint1.checkpoint

        md_params = {
            "MDReqID": bca.client_orderid(10),
            "SubscriptionRequestType": "Snapshot",
            "MDReqInstruments":
                [
                    {
                        "Instrument":
                            {
                                'InstrSymbol': 'INE467B01029',
                                'SecurityID': '28612',
                                'SecurityIDSource': 'EXC',
                                'InstrType': 'Equity',
                                'SecurityExchange': 'XNSE'
                            }
                    }
                ]
        }

        response = self.api.submitMarketDataRequest(
            request=SubmitMessageRequest(message=bca.wrap_message(md_params, "MarketDataRequest", 'trading_ret'),
                                         parent_event_id=self.case_id))
        print(response)
        content = {
            "_type": "MarketDataSnapshotFullRefresh",
            "MDReqID": md_params["MDReqID"],
            "MDTime": "2021-09-21T14:43:39.772722",
            "MarketDataFulls": [
                {
                    "MDEntryPx": 5,
                    "MDEntrySize": 5555,
                    "MDEntryType": "Bid"
                }
            ]
        }
        Stubs.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'MarketDataSnapshotFullRefresh',
                bca.wrap_filter(content, 'MarketDataSnapshotFullRefresh', "_type"),
                checkpoint_id1, self.connectivity, self.case_id
            ),

        )

    # Main method
    def execute(self):
        self.send_md_snapshot_request()


if __name__ == '__main__':
    pass
