import logging

import time

from rule_management import RuleManager
from stubs import Stubs
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd

from win_gui_modules.aggregated_rates_wrappers import PlaceRFQRequest, RFQTileOrderSide, ModifyRFQTileRequest
from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.client_pricing_wrappers import BaseTileDetails
from win_gui_modules.quote_wrappers import QuoteDetailsRequest

from copy import deepcopy
from datetime import datetime


class TestCase:
    def __init__(self, report_id):
        # Logger setup
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Services setup
        self.fix_act = Stubs.fix_act
        self.verifier = Stubs.verifier
        # self.common_act = Stubs.win_act
        # self.ar_service = Stubs.win_act_aggregated_rates_service
        # self.ob_act = Stubs.win_act_order_book

        # Case parameters setup
        self.case_id = bca.create_event('QAP-1520', report_id)
        self.session_id = set_session_id()
        set_base(self.session_id, self.case_id)
        self.base_request = get_base_request(self.session_id, self.case_id)
        # self.base_details = BaseTileDetails(base=self.base_request)

        self.user = Stubs.custom_config['qf_trading_fe_user_303']
        self.case_params = {
            'Connectivity': 'fix-qsesp-303',
            'MDReqID': bca.client_orderid(10),
            'Account': 'MMCLIENT1',
            'HandlInst': '1',
            'Side': '1',
            'OrderQty': 1000000,
            'OrdType': '2',
            'Price': 35.002,
            'TimeInForce': '3',
            'SettlType': 0,
            'SettlDate': tsd.spo(),
            'Instrument': {
                'Symbol': 'EUR/USD',
                'Product': '4',
                'SecurityType': 'FXSPOT'
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
            'Currency': 'EUR'
        }

        # Case rules
        self.rule_manager = RuleManager()
        self.NOS = None
        self.TRFQ = None

    # FE open method
    def prepare_frontend(self):
        work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
        password = Stubs.custom_config['qf_trading_fe_password_303']
        if not Stubs.frontend_is_open:
            prepare_fe(self.case_id, self.session_id, work_dir, self.user, password)

    # Add case rules method
    def add_rules(self):
        # self.NOS = self.rule_manager.add_NOS()
        # self.TRFQ = self.rule_manager.add_TRFQ('fix-fh-fx-rfq')
        pass

    # Remove case rules method
    def remove_rules(self):
        # self.rule_manager.remove_rule(self.NOS)
        # self.rule_manager.remove_rule(self.TRFQ)
        pass

    # Send MarketDataRequest subscribe method
    def send_md_subscribe(self):
        # MarketDataRequest parameters
        md_params = {
            'SenderSubID': self.case_params['Account'],
            'MDReqID': self.case_params['MDReqID'],
            'SubscriptionRequestType': '1',
            'MarketDepth': '0',
            'MDUpdateType': '0',
            'NoMDEntryTypes': [{'MDEntryType': '0'}, {'MDEntryType': '1'}],
            'NoRelatedSymbols': [
                {
                    'Instrument': self.case_params['Instrument'],
                    'SettlDate': self.case_params['SettlDate']
                }
            ]
        }

        # Send MarketDataRequest via FIX
        subscribe = self.fix_act.placeMarketDataRequestFIX(
            bca.convert_to_request(
                'Send MDR (subscribe)',
                self.case_params['Connectivity'],
                self.case_id,
                bca.message_to_grpc('MarketDataRequest', md_params, self.case_params['Connectivity'])
            ))

        # MarketDataRequest response parameters
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
                    'SettlDate': self.case_params['SettlDate'],
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
                    'SettlDate': self.case_params['SettlDate'],
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 1,
                    'MDEntryDate': '*',
                    'MDEntryType': 1
                },
                {
                    'SettlType': 0,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.case_params['SettlDate'],
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 2,
                    'MDEntryDate': '*',
                    'MDEntryType': 0
                },
                {
                    'SettlType': 0,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.case_params['SettlDate'],
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 2,
                    'MDEntryDate': '*',
                    'MDEntryType': 1
                },
                {
                    'SettlType': 0,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.case_params['SettlDate'],
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 3,
                    'MDEntryDate': '*',
                    'MDEntryType': 0
                },
                {
                    'SettlType': 0,
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'QuoteEntryID': '*',
                    'MDOriginType': 1,
                    'SettlDate': self.case_params['SettlDate'],
                    'MDQuoteType': 1,
                    'MDEntryPositionNo': 3,
                    'MDEntryDate': '*',
                    'MDEntryType': 1
                }
            ]
        }

        # Check MarketDataRequest response via FIX
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
        # Change MarketDataRequest from 'Subscribe' to 'Unsubscribe'
        md_params['SubscriptionRequestType'] = '2'
        # Send MarketDataRequest via FIX
        self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send MDR (unsubscribe)',
                self.case_params['Connectivity'],
                self.case_id,
                bca.message_to_grpc('MarketDataRequest', md_params, self.case_params['Connectivity'])
            ))

    def send_order(self):
        sor_order_params = {
            'Account': self.case_params['Account'],
            'HandlInst': self.case_params['HandlInst'],
            'Side': self.case_params['Side'],
            'OrderQty': self.case_params['OrderQty'],
            'TimeInForce': self.case_params['TimeInForce'],
            'Price': self.case_params['Price'],
            'OrdType': self.case_params['OrdType'],
            'ClOrdID': bca.client_orderid(9),
            'TransactTime': datetime.utcnow().isoformat(),
            'SettlType': self.case_params['SettlType'],
            'SettlDate': self.case_params['SettlDate'],
            'Instrument': self.case_params['Instrument'],
            'Currency': 'EUR',
            'Text': 'QAP-1520'
        }

        new_sor_order = self.fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                "Send new IOC order", self.case_params['Connectivity'], self.case_id,
                bca.message_to_grpc('NewOrderSingle', sor_order_params, self.case_params['Connectivity'])
            ))

        checkpoint_1 = new_sor_order.checkpoint_id
        pending_er_params = {
            **self.reusable_order_params,
            'ClOrdID': sor_order_params['ClOrdID'],
            'OrderID': new_sor_order.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'CumQty': '0',
            'LastPx': '0',
            'LastQty': '0',
            'QtyType': '0',
            'AvgPx': '0',
            'OrdStatus': 'A',
            'ExecType': 'A',
            'NoParty': [{
                'PartyID': 'gtwquod5',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }],
            'LeavesQty': sor_order_params['OrderQty'],
            'Instrument': self.case_params['Instrument']
        }
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                "Execution Report with OrdStatus = Pending",
                bca.filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1, self.case_params['Connectivity'], self.case_id
            ),
            timeout=3000
        )

        new_er_params = deepcopy(pending_er_params)
        new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
        new_er_params['Instrument'] = {
            'Symbol': self.case_params['Instrument']['Symbol']
        }
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                "Execution Report with OrdStatus = New",
                bca.filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1, self.case_params['Connectivity'], self.case_id
            ),
            timeout=3000
        )

    # Main method. Must call in demo.py by "QAP_1520.TestCase(report_id).execute()" command
    def execute(self):
        # try:
        #     self.prepare_frontend()
        #     self.add_rules()
        #
        # except Exception as e:
        #     logging.error('Error execution', exc_info=True)
        #
        # self.remove_rules()
        # close_fe(self.case_id, self.session_id)
        market_data_params = self.send_md_subscribe()
        time.sleep(6)
        self.send_order()
        self.send_md_unsubscribe(market_data_params)


if __name__ == '__main__':
    pass
