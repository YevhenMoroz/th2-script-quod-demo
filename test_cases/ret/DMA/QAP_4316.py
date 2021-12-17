from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from custom import basic_custom_actions as bca

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime


class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('QAP_4316', report_id)
        self.api = Stubs.act_rest
        self.connectivity = 'api_session_ret'

    def new_order_single(self):
        checkpoint1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(self.case_id))
        checkpoint_id1 = checkpoint1.checkpoint
        nos_params = {
            'ClOrdID': bca.client_orderid(9),
            'Side': 'Buy',
            'OrdType': 'Limit',
            'Price': 10,
            'Currency': 'INR',
            'TimeInForce': 'Day',
            'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
            'ClientAccountGroupID': "TestClient",
            'OrdQty': 3333,
            'Instrument': {
                'InstrSymbol': 'INE467B01029',
                'SecurityID': '28612',
                'SecurityIDSource': 'EXC',
                'InstrType': 'Equity',
                'SecurityExchange': 'XNSE'
            }
        }

        response = self.api.submitNewOrderSingle(
            request=SubmitMessageRequest(message=bca.message_to_grpc('NewOrderSingle', nos_params, 'trading_ret')))
        print(response)

        content = {
            "_type": "OrderUpdate",
            "AvgPrice": 0,
            "ClOrdID": "*",
            "ClientAccountGroupID": "undefined",
            "CumQty": 0,
            "Currency": "INR",
            "ExecType": "Rejected",
            "FreeNotes": "11620 unknown client TestClient / 11505 Runtime error (no VAccountGroup with keys [undefined] in cache or database)",
            "LeavesQty": 0,
            "OrdID": '*',
            "OrdQty": 3333,
            "OrdType": "Limit",
            "OrderStatus": "Rejected",
            "Price": 10,
            "SettlDate": "*",
            "Side": "Buy",
            "TimeInForce": "Day",
            "TransactTime": "*"
        }
        Stubs.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'OrderUpdate',
                bca.wrap_filter(content, 'OrderUpdate', ["OrderStatus"]),
                checkpoint_id1, self.connectivity, self.case_id
            ),

        )

    # Main method
    def execute(self):
        self.new_order_single()