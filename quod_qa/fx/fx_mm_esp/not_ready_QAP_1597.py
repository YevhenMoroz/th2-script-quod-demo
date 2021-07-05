import logging
import os
from datetime import datetime
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest
from win_gui_modules.common_wrappers import BaseTileDetails

from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from copy import deepcopy
from custom.basic_custom_actions import create_event
from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call, get_opened_fe



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
# connectivity = 'fix-ss-308-mercury-standard'
connectivity = 'fix-qsesp-303'
account = 'MMCLIENT1'
qty = 1000000
client_tier='Bronze'
symbol='YYY/XXX'


class TestCase:
    def __init__(self, report_id):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Services setup
        self.fix_act = Stubs.fix_act
        self.verifier = Stubs.verifier
        self.common_act = Stubs.win_act
        self.ob_act = Stubs.win_act_order_book
        self.cpt_service = Stubs.win_act_cp_service


        # Case parameters setup
        self.case_id = bca.create_event('QAP_1597', report_id)
        self.session_id = set_session_id()
        set_base(self.session_id, self.case_id)
        self.base_request = get_base_request(self.session_id, self.case_id)

        self.case_params = {
            'Connectivity': connectivity,
            'MDReqID': bca.client_orderid(10),
            'ClOrdID': bca.client_orderid(9),
            'Account': account,
            'HandlInst': '1',
            'Side': '1',
            'OrderQty': qty,
            'OrdType': '2',
            # 'Price': 35.002,
            'TimeInForce': '4',
            'Currency': 'EUR',
            'SettlCurrency': 'USD',
            'SettlType': 0,
            'SettlDate': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y%m%d %H:%M:%S'),
            'Instrument': {
                'Symbol': symbol,
                'SecurityType': 'FXSPOT',
                'SecurityIDSource': '8',
                'SecurityID': 'EUR/USD',
                'SecurityExchange': 'XQFX',
            },
            'Product': '4',
        }

        # This parameters can be used for ExecutionReport message
        self.reusable_order_params = {
            'Account': self.case_params['Account'],
            'HandlInst': self.case_params['HandlInst'],
            'Side': self.case_params['Side'],
            'TimeInForce': self.case_params['TimeInForce'],
            'OrdType': self.case_params['OrdType'],
            'OrderCapacity': 'A',
            'Currency': self.case_params['Currency'],
            'Instrument': {
                'Symbol': self.case_params['Instrument']['Symbol'],
                'SecurityIDSource': self.case_params['Instrument']['SecurityIDSource'],
                'SecurityID': self.case_params['Instrument']['SecurityID'],
                'SecurityExchange': self.case_params['Instrument']['SecurityExchange']
            }
        }

        # Last checkpoint. Need in the future for check ExecutionReport via FIX
        self.last_checkpoint = None


    # Send MarketDataRequest subscribe method
    def send_md_subscribe(self):
        md_params = {
            'SenderSubID': self.case_params['Account'],
            'MDReqID': self.case_params['MDReqID'],
            'SubscriptionRequestType': '1',
            'MarketDepth': '0',
            'MDUpdateType': '0',
            'NoMDEntryTypes': [{'MDEntryType': '0'}, {'MDEntryType': '1'}],
            'NoRelatedSymbols': [
                {
                    'Instrument': {
                        'Symbol': self.case_params['Instrument']['Symbol'],
                        'SecurityType': self.case_params['Instrument']['SecurityType']
                    },
                    'SettlDate': self.case_params['SettlDate'],
                    'SettlType': self.case_params['SettlType']
                }
            ],
            'Product': self.case_params['Product']
        }

        subscribe = self.fix_act.placeMarketDataRequestFIX(
            bca.convert_to_request(
                'Send MDR (subscribe)',
                self.case_params['Connectivity'],
                self.case_id,
                bca.message_to_grpc('MarketDataRequest', md_params, self.case_params['Connectivity'])
            ))




        md_reject = {
            'MDReqID': md_params['MDReqID'],
        }

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Receive MarketDataSnapshotFullRefresh (pending)',
                bca.filter_to_grpc('MarketDataRequestReject',md_reject, ['MDReqID']),
                subscribe.checkpoint_id,
                self.case_params['Connectivity'],
                self.case_id
            )
        )

        # return md_params



    def execute(self):

        try:


            # Step 1-2
            self.send_md_subscribe()









        except Exception as e:
            logging.error('Error execution', exc_info=True)

        # close_fe(self.case_id, self.session_id)




if __name__ == '__main__':
    pass