from enum import Enum

from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest

from stubs import Stubs
from custom import basic_custom_actions as bca

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime, timedelta

from win_gui_modules.utils import set_session_id

rep_id = bca.create_event('java_api_example ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))


class ORSMessages(Enum):
    order_list_wave_creation_request = 'Order_OrderListWaveCreationRequest'
    order_submit = 'Order_OrderSubmit'
    trade_request = 'Order_TradeEntryRequest'


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
                'OrdID': "CO1211203153756175001",
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
        # 'AuthenticationBlock': {'AuthenticationBlock': "JavaApiUser",
        #                         'RoleID': 'Trader',
        #                         'SessionKey': 62000000481},
        order_list_wave_creation_request = {

            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'OrderListWaveCreationRequestBlock': {
                'ParentOrdrList': {'ParentOrdrBlock': [{'ParentOrdID': 'CO1211203153316175001'},
                                                       {'ParentOrdID': 'CO1211203153318175001'}]},
                'OrderListID': 'LI1211203153316175001',
                'PercentQtyToRelease': 1.000000000,
                'QtyPercentageProfile': "REM"

            }
        }

        self.act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
            message=bca.message_to_grpc_fix_standard(ORSMessages.trade_request.value,
                                                     trade_params, self.connectivity),
            parent_event_id=self.case_id))

        # Main method

    def execute(self):
        self.send_nos()
        Stubs.factory.close()


if __name__ == '__main__':
    session_id = set_session_id()
    TestCase(rep_id).execute()
