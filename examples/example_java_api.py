import hashlib
import base64

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
        self.login = 'HD3'
        self.password = 'HD3'

    def get_hashed_password(self):
        hashed_password = hashlib.sha256()
        hashed_password.update(bytearray(self.login + self.password, 'UTF-8'))
        return base64.b64encode(hashed_password.digest()).decode('UTF-8')

    def send_login(self):
        login_message = {
            'Passwd': self.get_hashed_password(),
            'UserID': self.login,
            'LoginHost': 'TEST_HOSTNAME',
            'Origin': 'TRD',
            'AsyncSubject': 'inbox123'
        }
        login_response = self.act_java_api.sendMessage(
            request=ActJavaSubmitMessageRequest(
                message=bca.message_to_grpc('Order_Login', login_message, self.connectivity)))

    def send_nos_old(self):
        cl_ord_id = bca.client_orderid(9)
        print(cl_ord_id)
        nos_params = {
            'NewOrderSingleBlock': {
                'ClOrdID': cl_ord_id,
                'Side': 'Buy',
                'OrdType': 'Limit',
                'Price': 5,
                'Currency': 'EUR',
                'TimeInForce': 'Day',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'ClientAccountGroupID': 'TEST2',
                'OrdQty': 100,
                'InstrumentBlock': {
                    'InstrSymbol': 'FR0010263202_EUR',
                    'SecurityID': 'FR0010263202',
                    'SecurityIDSource': 'ISIN',
                    'InstrType': 'Equity',
                    'SecurityExchange': 'XPAR'
                }
            }
        }
        self.act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
            message=bca.message_to_grpc('Fix_NewOrderSingle', nos_params, 'quod_http')))

    def send_nos_new(self):
        nos_params = {
            'AuthenticationBlock': {
                'UserID': "HD5",
                'RoleID': 'HeadOfSaleDealer',
                'SessionKey': 30900000303
            },
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
                'OrdQty': 100.000000000,
                'AccountGroupID': 'CLIENT1',
                'InstrID': '5XRAA7DXZg14IOkuNrAfsg',
                'ExecutionPolicy': 'DMA',
                'ExternalCare': 'No'
            }
        }

        print(ActJavaSubmitMessageRequest(
            message=bca.message_to_grpc('Order_OrderSubmit', nos_params, 'quod_http')))

        self.act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
            message=bca.message_to_grpc('Order_OrderSubmit', nos_params, 'quod_http')))

    # Main method
    def execute(self):
        self.send_login()
        # self.send_nos_old()
        # self.send_nos_new()


if __name__ == '__main__':
    pass
