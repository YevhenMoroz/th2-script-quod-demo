from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from custom import basic_custom_actions as bca

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime


class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('test', report_id)
        self.api = Stubs.act_rest

    def test_nos_method(self):
        nos_params = {
            'ClOrdID': bca.client_orderid(9),
            'Side': 'Buy',
            'OrdType': 'Limit',
            'Price': 5,
            'Currency': 'EUR',
            'TimeInForce': 'Day',
            'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
            'ClientAccountGroupID': 'TEST2',
            'OrdQty': 100,
            'Instrument': {
                'InstrSymbol': 'FR0010263202_EUR',
                'SecurityID': 'FR0010263202',
                'SecurityIDSource': 'ISIN',
                'InstrType': 'Equity',
                'SecurityExchange': 'XPAR'
            }
        }

        self.api.submitNewOrderSingle(
            request=SubmitMessageRequest(message=bca.message_to_grpc('NewOrderSingle', nos_params, 'quod_rest')))

    # Main method
    def execute(self):
        self.test_nos_method()


if __name__ == '__main__':
    pass
