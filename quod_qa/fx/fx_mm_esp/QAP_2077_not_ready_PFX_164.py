import logging
import os
from datetime import datetime
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.common_wrappers import BaseTileDetails

from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from copy import deepcopy
from custom.basic_custom_actions import create_event
from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call, get_opened_fe
import time


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
# connectivity = 'fix-ss-308-mercury-standard'
connectivity = 'fix-qsesp-303'
account = 'MMCLIENT1'
qty = 1000000

class TestCase:
    def __init__(self, report_id):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Services setup
        self.fix_act = Stubs.fix_act
        self.verifier = Stubs.verifier
        self.common_act = Stubs.win_act
        self.ob_act = Stubs.win_act_order_book



        # Case parameters setup
        self.case_id = bca.create_event('QAP_2077', report_id)
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
            'TimeInForce': '3',
            'Currency': 'EUR',
            'SettlCurrency': 'USD',
            'SettlType': 0,
            'SettlDate': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y%m%d %H:%M:%S'),
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityType': 'FXSPOT',
                'SecurityIDSource': '8',
                'SecurityID': 'EUR/USD',
                'SecurityExchange': 'XQFX',
                'Product': '4'
            }
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
                'SecurityExchange': self.case_params['Instrument']['SecurityExchange'],
                'Product': self.case_params['Instrument']['Product']
            }
        }

        # Last checkpoint. Need in the future for check ExecutionReport via FIX
        self.last_checkpoint = None

    # FE open method
    # def prepare_frontend(self):
    #         user = Stubs.custom_config['qf_trading_fe_folder_308']
    #         work_dir = Stubs.custom_config['qf_trading_fe_folder_308']
    #         password = Stubs.custom_config['qf_trading_fe_folder_308']
    #         if not Stubs.frontend_is_open:
    #             prepare_fe(self.case_id, self.session_id, work_dir, user, password)

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
                        'SecurityType': self.case_params['Instrument']['SecurityType'],
                        'Product': self.case_params['Instrument']['Product']
                    },
                    'SettlDate': self.case_params['SettlDate'],
                    'SettlType': self.case_params['SettlType']
                }
            ]
        }

        subscribe = self.fix_act.placeMarketDataRequestFIX(
            bca.convert_to_request(
                'Send MDR (subscribe)',
                self.case_params['Connectivity'],
                self.case_id,
                bca.message_to_grpc('MarketDataRequest', md_params, self.case_params['Connectivity'])
            ))
        time.sleep(3)

        self.case_params['Price'] = subscribe \
            .response_messages_list[0].fields['NoMDEntries'] \
            .message_value.fields['NoMDEntries'].list_value.values[1] \
            .message_value.fields['MDEntryPx'].simple_value

        print(f"Price is: {self.case_params['Price']}")

        # Qty = subscribe \
        #     .response_messages_list[0].fields['NoMDEntries'] \
        #     .message_value.fields['NoMDEntries'].list_value.values[1] \
        #     .message_value.fields['MDEntrySize'].simple_value

        print(self.case_params['Price'])
        md_subscribe_response = {
            'MDReqID': md_params['MDReqID'],
            'Instrument': {
                'Symbol': self.case_params['Instrument']['Symbol']
            },
            'LastUpdateTime': '*',
            'NoMDEntries': [
                {
                    'SettlType': 0,
                    'MDEntryPx': '*',
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.case_params['SettlDate'].split(' ')[0],
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 1,
                    'MDEntryDate': '*',
                    'MDEntryType': 0
                },
                {
                    'SettlType': 0,
                    'MDEntryPx': '*',
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.case_params['SettlDate'].split(' ')[0],
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 1,
                    'MDEntryDate': '*',
                    'MDEntryType': 1
                },
                {
                    'SettlType': 0,
                    'MDEntryPx': '*',
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.case_params['SettlDate'].split(' ')[0],
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 2,
                    'MDEntryDate': '*',
                    'MDEntryType': 0
                },
                {
                    'SettlType': 0,
                    'MDEntryPx': '*',
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.case_params['SettlDate'].split(' ')[0],
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 2,
                    'MDEntryDate': '*',
                    'MDEntryType': 1
                },
                {
                    'SettlType': 0,
                    'MDEntryPx': '*',
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.case_params['SettlDate'].split(' ')[0],
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 3,
                    'MDEntryDate': '*',
                    'MDEntryType': 0
                },
                {
                    'SettlType': 0,
                    'MDEntryPx': '*',
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.case_params['SettlDate'].split(' ')[0],
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 3,
                    'MDEntryDate': '*',
                    'MDEntryType': 1
                }
            ]
        }

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Receive MarketDataSnapshotFullRefresh (pending)',
                bca.filter_to_grpc('MarketDataSnapshotFullRefresh', md_subscribe_response, ['MDReqID']),
                subscribe.checkpoint_id,
                self.case_params['Connectivity'],
                self.case_id
            )
        )

        # Return MarketDataRequest params for unsubscribe in future
        return md_params

    # Send MarketDataRequest unsubscribe method
    def send_md_unsubscribe(self, md_params):
        md_params['SubscriptionRequestType'] = '2'

        self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send MDR (unsubscribe)',
                self.case_params['Connectivity'],
                self.case_id,
                bca.message_to_grpc('MarketDataRequest', md_params, self.case_params['Connectivity'])
            ))



        # Send FOK order via FIX

    def send_order(self):
        order_params = {
            'Account': self.case_params['Account'],
            'HandlInst': self.case_params['HandlInst'],
            'Side': self.case_params['Side'],
            # 'OrderQty': self.case_params['OrderQty'],
            'OrderQty': 17000000,
            'TimeInForce': self.case_params['TimeInForce'],
            'Price': self.case_params['Price'],
            'OrdType': self.case_params['OrdType'],
            'ClOrdID': self.case_params['ClOrdID'],
            'TransactTime': datetime.utcnow().isoformat(),
            'SettlType': self.case_params['SettlType'],
            'SettlDate': self.case_params['SettlDate'],
            'Instrument': {
                'Symbol': self.case_params['Instrument']['Symbol'],
                'Product': self.case_params['Instrument']['Product']
            },
            'Currency': self.case_params['Currency'],

        }

        new_order = self.fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                'Send new IOC order', self.case_params['Connectivity'], self.case_id,
                bca.message_to_grpc('NewOrderSingle', order_params, self.case_params['Connectivity'])
            ))

        checkpoint = new_order.checkpoint_id
        pending_er_params = {
            **self.reusable_order_params,
            'ExecID': '*',
            'ClOrdID': order_params['ClOrdID'],
            'OrderID': new_order.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'CumQty': '0',
            'LastPx': '0',
            'LastQty': '0',
            'QtyType': '0',
            'OrderQty': order_params['OrderQty'],
            'Price': order_params['Price'],
            'SettlCurrency': self.case_params['SettlCurrency'],
            'AvgPx': '0',
            'OrdStatus': 'A',
            'ExecType': 'A',
            'NoParty': [{
                'PartyID': 'gtwquod3',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }],
            'LeavesQty': order_params['OrderQty'],
        }

        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Pending',
                bca.filter_to_grpc('ExecutionReport', pending_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint, self.case_params['Connectivity'], self.case_id
            ),
            timeout=3000
        )

        new_er_params = deepcopy(pending_er_params)
        new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
        new_er_params['SettlDate'] = self.case_params['SettlDate'].split(' ')[0]
        new_er_params['SettlType'] = self.case_params['SettlType']
        new_er_params['ExecRestatementReason'] = '4'

        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = New',
                bca.filter_to_grpc('ExecutionReport', new_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint, self.case_params['Connectivity'], self.case_id
            ),
            timeout=3000
        )

        self.last_checkpoint = checkpoint

        # Check order status via FIX and GUI

    def check_filled(self):
        er_filled = {
            **self.reusable_order_params,
            'ClOrdID': self.case_params['ClOrdID'],
            'OrderID': '*',
            'ExecID': '*',
            'TransactTime': '*',
            'LastSpotRate': self.case_params['Price'],
            'LastQty': self.case_params['OrderQty'],
            'CumQty': self.case_params['OrderQty'],
            'QtyType': '0',
            'Price': self.case_params['Price'],
            'OrderQty': self.case_params['OrderQty'],
            'LastPx': self.case_params['Price'],
            'AvgPx': self.case_params['Price'],
            'OrdStatus': '2',
            'ExecType': 'F',
            'LeavesQty': '0',
            'SettlType': self.case_params['SettlType'],
            'SettlDate': self.case_params['SettlDate'].split(' ')[0],
            'Currency': self.case_params['Currency'],
            'SettlCurrency': self.case_params['SettlCurrency'],
            'TradeDate': '*',
            'ExDestination': 'XQFX',
            'GrossTradeAmt': '*',
            'NoParty': [{
                'PartyID': 'gtwquod3',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }]
        }
        er_filled['Instrument']['SecurityType'] = self.case_params['Instrument']['SecurityType']

        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Filled',
                bca.filter_to_grpc('ExecutionReport', er_filled, ['ClOrdID', 'OrdStatus']),
                self.last_checkpoint, self.case_params['Connectivity'], self.case_id
            ),
            timeout=3000
        )

        # execution_id = bca.client_orderid(4)
        # ob = OrdersDetails()
        # ob.set_default_params(self.base_request)
        # ob.set_extraction_id(execution_id)
        # ob_cl_ord_id = ExtractionDetail("orderBook.clordid", "ClOrdID")
        # ob_tif = ExtractionDetail("orderBook.timeinforce", "TIF")
        # ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
        # ob.add_single_order_info(
        #     OrderInfo.create(
        #         action=ExtractionAction.create_extraction_action(extraction_details=[ob_exec_sts, ob_cl_ord_id, ob_tif])))
        # call(self.ob_act.getOrdersDetails, ob.request())
        # call(self.common_act.verifyEntities, verification(execution_id, "checking OB",
        #                                                   [verify_ent("OB ClOrdID vs FIX ClOrdID", ob_cl_ord_id.name,
        #                                                               er_filled['ClOrdID']),
        #                                                    verify_ent("OB ExecSts", ob_exec_sts.name, "Filled"),
        #                                                    verify_ent("OB TIF",ob_tif.name,"FillOrKill")]))






    def execute(self):

        try:

            # if not Stubs.frontend_is_open:
            #     prepare_fe_2(self.case_id, self.session_id)
            # else:
            #     get_opened_fe(self.case_id, self.session_id)

            # Step 1
            market_data_params = self.send_md_subscribe()
            self.send_order()
            # # Steps 3-4
            self.check_filled()
            #
            self.send_md_unsubscribe(market_data_params)


        except Exception as e:
            logging.error('Error execution', exc_info=True)

        # close_fe(self.case_id, self.session_id)


if __name__ == '__main__':
    pass