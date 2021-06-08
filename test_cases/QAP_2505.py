import locale
import logging
import time
from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from custom.verifier import Verifier
from rule_management import RuleManager
from stubs import Stubs

from custom import basic_custom_actions as bca, tenor_settlement_date as tsd

from win_gui_modules.aggregated_rates_wrappers import PlaceRFQRequest, RFQTileOrderSide, ModifyRFQTileRequest, \
    ContextAction, ExtractRFQTileValues, TableActionsRequest, TableAction, MoveESPOrderTicketRequest
from win_gui_modules.dealing_positions_wrappers import ExtractionPositionsAction, ExtractionPositionsFieldsDetails, \
    GetOrdersDetailsRequest, PositionsInfo
from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe_2, close_fe, \
    get_opened_fe, prepare_fe303, get_opened_fe_303
from win_gui_modules.wrappers import set_base, verification, verify_ent
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.client_pricing_wrappers import BaseTileDetails


class TestCase:
    def __init__(self, report_id):
        # Logger setup
        self.ord_id = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Services setup
        self.act = Stubs.fix_act
        self.verifier = Stubs.verifier
        self.common_act = Stubs.win_act
        self.ar_service = Stubs.win_act_aggregated_rates_service
        self.ob_act = Stubs.win_act_order_book
        self.pos_service = Stubs.act_fx_dealing_positions

        # Case parameters setup
        self.case_id = bca.create_event('QAP-2505', report_id)
        self.session_id = set_session_id()
        set_base(self.session_id, self.case_id)
        self.base_request = get_base_request(self.session_id, self.case_id)
        self.base_details = BaseTileDetails(base=self.base_request)

        self.venue = 'HSB'
        self.user = Stubs.custom_config['qf_trading_fe_user_303']
        self.quote_id = None
        self.price = None

        # Case rules
        self.rule_manager = RuleManager()
        self.RFQ = None
        self.TRFQ = None
        self.case_params = {
            'TraderConnectivity': 'gtwquod5-fx',
            'Account': 'MMCLIENT1',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD5',
        }
        self.reusable_params = {
            'Account': self.case_params['Account'],
            'Side': 1,
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityType': 'FXSPOT',
                'Product': 4
            },
            'SettlDate': tsd.spo(),
            'SettlType': '0'
        }

        self.cond_params = {}

    # Add case rules method
    def add_rules(self):
        self.RFQ = self.rule_manager.add_RFQ('fix-fh-fx-rfq')
        self.TRFQ = self.rule_manager.add_TRFQ('fix-fh-fx-rfq')
        # self.logger(f"Start rules with id's: \n  {self.RFQ}, {self.TRFQ}")

    # FE open method
    def prepare_frontend(self):
        work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
        password = Stubs.custom_config['qf_trading_fe_password_303']
        prepare_fe303(self.case_id, self.session_id, work_dir, self.user, password)

    # Remove case rules method
    def remove_rules(self):
        self.rule_manager.remove_rule(self.RFQ)
        self.rule_manager.remove_rule(self.TRFQ)
        self.rule_manager.print_active_rules()

    def send_rfq_via_FIX(self, qty, side, name):

        rfq_params_terminated = {
            'QuoteReqID': bca.client_orderid(9),
            'NoRelatedSymbols': [{
                **self.reusable_params,
                'Side': side,
                'Currency': 'EUR',
                'QuoteType': '1',
                'OrderQty': qty,
                'OrdType': 'D',
                'ExpireTime': self.reusable_params['SettlDate'] + '-23:59:00.000',
                'TransactTime': (datetime.utcnow().isoformat())
            }]
        }
        rfq_term = self.act.placeQuoteFIX(
            bca.convert_to_request(
                'Send RFQ for: ' + name,
                self.case_params['TraderConnectivity'],
                self.case_id,
                bca.message_to_grpc('QuoteRequest', rfq_params_terminated, self.case_params['TraderConnectivity'])
            ))

        if side == 1:
            self.price = rfq_term.response_messages_list[0].fields['OfferPx'].simple_value
            self.cond_params = {
                'OfferSpotRate': '*',
                'OfferPx': '*',
                'OfferSize': rfq_params_terminated['NoRelatedSymbols'][0]['OrderQty']
            }
        elif side == 2:
            self.price = rfq_term.response_messages_list[0].fields['BidPx'].simple_value
            self.cond_params = {
                'BidSpotRate': '*',
                'BidPx': '*',
                'BidSize': rfq_params_terminated['NoRelatedSymbols'][0]['OrderQty']
            }

        quote_params = {
            **self.reusable_params,
            **self.cond_params,
            'Side': rfq_params_terminated['NoRelatedSymbols'][0]['Side'],
            'QuoteReqID': rfq_params_terminated['QuoteReqID'],
            'QuoteID': '*',
            'ValidUntilTime': '*',
            'Currency': rfq_params_terminated['NoRelatedSymbols'][0]['Currency'],
            'QuoteType': 1
        }

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Quote Received for: ' + name,
                bca.filter_to_grpc('Quote', quote_params, ['QuoteReqID']),
                rfq_term.checkpoint_id,
                self.case_params['TraderConnectivity'],
                self.case_id
            )
        )

        # NewOrderSingle params for Quote Filled
        order_params = {
            **self.reusable_params,
            'Side': side,
            'QuoteID': rfq_term.response_messages_list[0].fields['QuoteID'],
            'ClOrdID': bca.client_orderid(9),
            'OrdType': 'D',
            'TransactTime': (datetime.utcnow().isoformat()),
            'OrderQty': rfq_params_terminated['NoRelatedSymbols'][0]['OrderQty'],
            'Price': self.price,
            'TimeInForce': 4
        }

        # Send NewOrderSingle for Quote Filled
        send_order = self.act.placeOrderFIX(
            bca.convert_to_request(
                'Send NewOrderSingle for: ' + name,
                self.case_params['TraderConnectivity'],
                self.case_id,
                bca.message_to_grpc('NewOrderSingle', order_params, self.case_params['TraderConnectivity'])
            ))

        er_pending_params = {
            'Side': order_params['Side'],
            'Account': self.reusable_params['Account'],
            'ClOrdID': order_params['ClOrdID'],
            'OrderQty': order_params['OrderQty'],
            'LeavesQty': order_params['OrderQty'],
            'TimeInForce': order_params['TimeInForce'],
            'OrdType': order_params['OrdType'],
            'Price': self.price,
            'OrderID': send_order.response_messages_list[0].fields['OrderID'].simple_value,
            'NoParty': [
                {'PartyRole': 36, 'PartyID': 'gtwquod5', 'PartyIDSource': 'D'}
            ],
            'Instrument': {
                'Symbol': self.reusable_params['Instrument']['Symbol'],
                'SecurityIDSource': 8,
                'SecurityID': self.reusable_params['Instrument']['Symbol'],
                'SecurityExchange': 'XQFX',
                'Product': 4
            },
            'SettlCurrency': 'USD',
            'Currency': rfq_params_terminated['NoRelatedSymbols'][0]['Currency'],
            'HandlInst': 1,
            'AvgPx': 0,
            'QtyType': 0,
            'LastQty': 0,
            'CumQty': 0,
            'LastPx': 0,
            'OrdStatus': 'A',
            'ExecType': 'A',
            'ExecID': '*',
            'TransactTime': '*',
            'OrderCapacity': 'A'
        }

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Execution Report for NewOrderSingle',
                bca.filter_to_grpc('ExecutionReport', er_pending_params, ['ClOrdID', 'OrdStatus', 'ExecType']),
                send_order.checkpoint_id,
                self.case_params['TraderConnectivity'],
                self.case_id
            )
        )

        er_filled_params = {
            'Side': order_params['Side'],
            'Account': 'MMCLIENT1_1',
            'SettlDate': self.reusable_params['SettlDate'],
            'TradeDate': datetime.utcnow().strftime('%Y%m%d'),
            'SettlType': self.reusable_params['SettlType'],
            'ClOrdID': order_params['ClOrdID'],
            'OrderQty': order_params['OrderQty'],
            'LeavesQty': 0,
            'TimeInForce': order_params['TimeInForce'],
            'OrdType': order_params['OrdType'],
            'Price': self.price,
            'OrderID': send_order.response_messages_list[0].fields['OrderID'].simple_value,
            'NoParty': [
                {'PartyRole': 36, 'PartyID': 'gtwquod5', 'PartyIDSource': 'D'}
            ],
            'Instrument': {
                'SecurityType': 'FXSPOT',
                'Symbol': 'EUR/USD',
                'SecurityIDSource': 8,
                'SecurityID': 'EUR/USD',
                'SecurityExchange': 'XQFX',
                'Product': 4
            },
            'SettlCurrency': 'USD',
            'Currency': 'EUR',
            'HandlInst': 1,
            'AvgPx': self.price,
            'QtyType': 0,
            'LastQty': order_params['OrderQty'],
            'CumQty': order_params['OrderQty'],
            'LastPx': self.price,
            'OrdStatus': 2,
            'ExecType': 'F',
            'ExecID': '*',
            'TransactTime': '*',
            'LastSpotRate': '*',
            'OrderCapacity': 'A',
            'ExDestination': 'XQFX',
            'GrossTradeAmt': '*'
        }

        self.ord_id = er_filled_params['OrderID']

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Receive ExecutionReport Filled',
                bca.filter_to_grpc('ExecutionReport', er_filled_params, ['ClOrdID', 'OrdStatus', 'ExecType']),
                send_order.checkpoint_id,
                self.case_params['TraderConnectivity'],
                self.case_id
            )
        )

    def con_qty(self, qty):
        con_qty = f"{qty.replace(',', '')}"
        return float(con_qty)

    # Check OrderBook method
    def check_ob(self):
        execution_id = bca.client_orderid(4)
        ob = OrdersDetails()
        ob.set_default_params(self.base_request)
        ob.set_extraction_id(execution_id)
        ob.set_filter(["Order ID", self.ord_id])
        # print(self.ord_id)
        # sub_order_id_dt = ExtractionDetail("subOrder_lvl_1.id", "ExecID")
        sub_order_qty = ExtractionDetail("subOrder_lvl_1.id", "Qty")
        sub_order_price = ExtractionDetail("subOrder_lvl_1.execprice", "ExecPrice")
        lvl1_info = OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[sub_order_qty,
                                                                                 sub_order_price]))
        lvl1_details = OrdersDetails.create(info=lvl1_info)
        ob.add_single_order_info(
            OrderInfo.create(
                action=ExtractionAction.create_extraction_action(), sub_order_details=lvl1_details))
        request = call(self.ob_act.getOrdersDetails, ob.request())
        return self.con_qty(request[sub_order_price.name])
        # print("ExecPrice: " + request[sub_order_price.name])

    def get_dealing_position(self):
        extraction_id = bca.client_orderid(4)
        quote_pos_details = GetOrdersDetailsRequest()
        quote_pos_details.set_default_params(self.base_request)
        quote_pos_details.set_extraction_id(extraction_id)

        quote_pos = ExtractionPositionsFieldsDetails("qt_pos.position", "Quote Position (EUR)")

        quote_pos_details.add_single_positions_info(
            PositionsInfo.create(
                action=ExtractionPositionsAction.create_extraction_action(extraction_details=[quote_pos])))

        response = call(self.pos_service.getFxDealingPositionsDetails, quote_pos_details.request())
        # print(response[quote_pos.value])
        return self.con_qty(response[quote_pos.value])

    def compare_position(self, pre_position, position, post_positon, name):
        cust_verifier = Verifier(self.case_id)
        cust_verifier.set_event_name('Checking Quote Position for ' + name)
        post_pos = pre_position + position
        cust_verifier.compare_values('Quote Position', str(post_pos), str(post_positon))
        cust_verifier.verify()

    # Main method. Must call in demo.py by "QAP_682.TestCase(report_id).execute()" command
    def execute(self):
        try:
            qty_1 = 6000000
            qty_2 = 2000000
            qty_3 = 8000000
            qty_4 = 3000000
            self.prepare_frontend()

            # Step 1: RFQ + Order Buy Side Qty: 6M
            name = '6M Buy Side'
            pre_position = self.get_dealing_position()
            self.send_rfq_via_FIX(qty_1, 1, name)
            position_6M = self.get_dealing_position()
            exec_price = self.check_ob()
            position = exec_price * -abs(qty_1)
            self.compare_position(pre_position, position, position_6M, name)

            # Step 2: RFQ + Order Buy Side Qty: 2M
            name = '2M Buy Side'
            self.send_rfq_via_FIX(qty_2, 1, name)
            position_2M = self.get_dealing_position()
            exec_price = self.check_ob()
            position = exec_price * -abs(qty_2)
            self.compare_position(position_6M, position, position_2M, name)

            # Step 3: RFQ + Order Sell Side Qty: 8M
            name = '8M Sell Side'
            self.send_rfq_via_FIX(qty_3, 2, name)
            position_8M = self.get_dealing_position()
            exec_price = self.check_ob()
            position = exec_price * abs(qty_3)
            self.compare_position(position_2M, position, position_8M, name)

            # Step 4: RFQ + Order Sell Side Qty: 3M
            name = '3M Sell Side'
            self.send_rfq_via_FIX(qty_4, 2, name)
            position_3M = self.get_dealing_position()
            exec_price = self.check_ob()
            position = exec_price * abs(qty_4)
            self.compare_position(position_8M, position, position_3M, name)

        except Exception as e:
            logging.error('Error execution', exc_info=True)

        close_fe(self.case_id, self.session_id)


if __name__ == '__main__':
    pass
