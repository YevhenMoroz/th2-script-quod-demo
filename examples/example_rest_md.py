from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from custom import basic_custom_actions as bca

import time


class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('Example REST MarketDataRequest', report_id)
        self.api = Stubs.act_rest

    def send_md_snapshot_request(self):
        md_params = {
            "MDReqID": bca.client_orderid(10),
            "SubscriptionRequestType": "Snapshot",
            "MDReqInstruments":
                [
                    {
                        "Instrument":
                            {
                                "InstrSymbol": "GB00B1S49Q91_GBP",
                                "SecurityID": "GB00B1S49Q91",
                                "SecurityIDSource": "ISIN",
                                "InstrType": "Equity",
                                "SecurityExchange": "XLON"
                            }
                    }
                ]
        }

        self.api.submitMarketDataRequest(
            request=SubmitMessageRequest(message=bca.message_to_grpc('MarketDataRequest', md_params, 'quod_rest')))

    # Main method
    def execute(self):
        self.send_md_snapshot_request()


if __name__ == '__main__':
    pass
