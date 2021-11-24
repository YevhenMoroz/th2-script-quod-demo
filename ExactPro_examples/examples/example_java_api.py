from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest

from stubs import Stubs
from custom import basic_custom_actions as bca

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime, timedelta

rep_id = bca.create_event('java_api_example ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))


class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('java api test', report_id)
        self.act_java_api = Stubs.act_java_api
        self.connectivity = '317_java_api'

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
                'ExecutionPolicy': 'Care',
                'ExternalCare': 'No'
            },
            'CDOrdAssignInstructionsBlock': {'RecipientUserID': 'ymoroz', 'RecipientRoleID': 'HSD',
                                             'RecipientDeskID': '6'}
        }

        trade_params = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'TradeEntryRequestBlock': {
                'OrdID': "CO1211006080150386001",
                'ExecPrice': "5.000000000",
                'ExecQty': "900.000000000",
                'TradeEntryTransType': 'NEW',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'LastMkt': 'XPAR',
                'TradeDate': (tm(datetime.utcnow().isoformat())).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'SettlDate': (tm(datetime.utcnow().isoformat()) + timedelta(days=2)).date().strftime(
                    '%Y-%m-%dT%H:%M:%S')
            }
        }

        self.act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
            message=bca.message_to_grpc('Order_OrderSubmit', nos_params, self.connectivity),
            parent_event_id=self.case_id))

        #Main method
#     def execute(self):
#         self.send_nos()
#         Stubs.factory.close()
#
#
# if __name__ == '__main__':
#     TestCase(rep_id).execute()
#     pass
