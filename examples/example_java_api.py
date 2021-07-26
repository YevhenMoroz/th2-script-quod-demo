from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest

from stubs import Stubs
from custom import basic_custom_actions as bca

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime


class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('java api test', report_id)
        self.act_java_api = Stubs.act_java_api
        self.connectivity = 'quod_http'

    def send_nos(self):
        nos_params = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'NewOrderSingleBlock': {
                'ListingList': {
                    'ListingBlock': [
                        {
                            'ListingID': 1200
                        }
                    ]
                },
                'Side': 'Buy',
                'Price': 21.000000000,
                'QtyType': 'Units',
                'OrdType': 'Limit',
                'TimeInForce': 'Day',
                'PositionEffect': 'Open',
                'SettlCurrency': 'EUR',
                'OrdCapacity': 'Agency',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'MaxPriceLevels': 1,
                'ExecutionOnly': 'No',
                'ClientInstructionsOnly': 'No',
                'BookingType': 'RegularBooking',
                'OrdQty': 666.000000000,
                'AccountGroupID': 'CLIENT1',
                'InstrID': '5XRAA7DXZg14IOkuNrAfsg',
                'ExecutionPolicy': 'DMA',
                'ExternalCare': 'No'
            }
        }

        print(ActJavaSubmitMessageRequest(
            message=bca.message_to_grpc('Order_OrderSubmit', nos_params, 'quod_http')))

        response= self.act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
            message=bca.message_to_grpc('Order_OrderSubmit', nos_params, 'quod_http')))

        print(f'*********** response sendMessage = {response}************')


    # Main method
    def execute(self):
        self.send_nos()


if __name__ == '__main__':
    pass
