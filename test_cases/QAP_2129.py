import locale
import logging, random
import re
import time
from datetime import datetime

from custom.verifier import Verifier
from rule_management import RuleManager
from stubs import Stubs
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd

# from win_gui_modules.aggregated_rates_wrappers import PlaceRFQRequest, RFQTileOrderSide, ModifyRFQTileRequest
from win_gui_modules.application_wrappers import CloseApplicationRequest, OpenApplicationRequest, LoginDetailsRequest
from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe, prepare_fe303
from win_gui_modules.wrappers import set_base, verification, verify_ent
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.client_pricing_wrappers import BaseTileDetails
from win_gui_modules.quote_wrappers import QuoteDetailsRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class TestCase:

    def __init__(self, report_id):
        self.act = Stubs.fix_act
        self.common_act = Stubs.win_act
        self.ar_service = Stubs.win_act_aggregated_rates_service
        self.event_store = Stubs.event_store
        self.verifier = Stubs.verifier
        self.simulator = Stubs.simulator

        seconds, nanos = bca.timestamps()  # Store case start time
        self.case_name = "QAP-2129"
        self.case_id = bca.create_event(self.case_name, report_id)
        self.rand_qty = random.randint(1, 100000)

        self.work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
        self.user = Stubs.custom_config['qf_trading_fe_user_303']
        self.password = Stubs.custom_config['qf_trading_fe_password_303']

        self.session_id = set_session_id()
        set_base(self.session_id, self.case_id)
        self.base_request = get_base_request(self.session_id, self.case_id)
        base_details = BaseTileDetails(base=self.base_request)

        self.qty_new, self.can_qty, self.term_qty, self.rej_qty, self.exp_qty = 0, 0, 0, 0, 0
        self.rfq_qty_list = []

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

    @staticmethod
    def comma_qty(qty):
        locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
        return locale.format_string('%d', qty, grouping=True)

    def send_RFQ_via_FIX(self):

        # RFQ parameters for receive Status New
        rfq_params_new = {
            'QuoteReqID': bca.client_orderid(9),
            'NoRelatedSymbols': [{
                **self.reusable_params,
                'Currency': 'EUR',
                'QuoteType': '1',
                'OrderQty': 16000000 + self.rand_qty,
                'OrdType': 'D',
                'ExpireTime': self.reusable_params['SettlDate'] + '-23:59:00.125',
                'TransactTime': (datetime.utcnow().isoformat())
            }]
        }

        self.act.sendMessage(
            bca.convert_to_request(
                'Send RFQ_New',
                self.case_params['TraderConnectivity'],
                self.case_id,
                bca.message_to_grpc('QuoteRequest', rfq_params_new, self.case_params['TraderConnectivity'])
            ))
        self.qty_new = self.comma_qty(rfq_params_new['NoRelatedSymbols'][0]['OrderQty'])
        self.rfq_qty_list = ['New RFQ: ' + self.qty_new]

        # RFQ parameters for receive Status Expired
        rfq_params_expired = {
            'QuoteReqID': bca.client_orderid(9),
            'NoRelatedSymbols': [{
                **self.reusable_params,
                'Currency': 'EUR',
                'QuoteType': '1',
                'OrderQty': 2000000 + self.rand_qty,
                'OrdType': 'D',
                'ExpireTime': self.reusable_params['SettlDate'] + '-23:59:00.000',
                'TransactTime': (datetime.utcnow().isoformat())
            }]
        }

        rfq_exp = self.act.placeQuoteFIX(
            bca.convert_to_request(
                'Send RFQ_Expired',
                self.case_params['TraderConnectivity'],
                self.case_id,
                bca.message_to_grpc('QuoteRequest', rfq_params_expired, self.case_params['TraderConnectivity'])
            ))

        self.exp_qty = self.comma_qty(rfq_params_expired['NoRelatedSymbols'][0]['OrderQty'])
        self.rfq_qty_list.append('Expired RFQ: ' + self.exp_qty)

        quote_params_exp = {
            **self.reusable_params,
            'QuoteReqID': rfq_params_expired['QuoteReqID'],
            'OfferPx': 35.001,
            'OfferSize': rfq_params_expired['NoRelatedSymbols'][0]['OrderQty'],
            'QuoteID': '*',
            'OfferSpotRate': '35.001',
            'ValidUntilTime': '*',
            'Currency': 'EUR',
            'QuoteType': 1
        }

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Quote Received',
                bca.filter_to_grpc('Quote', quote_params_exp, ['QuoteReqID']),
                rfq_exp.checkpoint_id,
                self.case_params['TraderConnectivity'],
                self.case_id
            )
        )

        # RFQ parameters for receive Status Rejected
        rfq_params_rejected = {
            'QuoteReqID': bca.client_orderid(9),
            'NoRelatedSymbols': [{
                **self.reusable_params,
                'Currency': 'EUS',
                'QuoteType': '1',
                'OrderQty': 11000000 + self.rand_qty,
                'OrdType': 'D',
                'ExpireTime': self.reusable_params['SettlDate'] + '-23:59:00.000',
                'TransactTime': (datetime.utcnow().isoformat())
            }]
        }

        self.act.placeQuoteFIX(
            bca.convert_to_request(
                'Send RFQ_Rejected',
                self.case_params['TraderConnectivity'],
                self.case_id,
                bca.message_to_grpc('QuoteRequest', rfq_params_rejected, self.case_params['TraderConnectivity'])
            ))
        self.rej_qty = self.comma_qty(rfq_params_rejected['NoRelatedSymbols'][0]['OrderQty'])
        self.rfq_qty_list.append('Rejected RFQ: ' + self.rej_qty)

        # RFQ parameters for receive Status Canceled
        rfq_params_canceled = {
            'QuoteReqID': bca.client_orderid(9),
            'NoRelatedSymbols': [{
                **self.reusable_params,
                'Currency': 'EUR',
                'QuoteType': '1',
                'OrderQty': 1200000 + self.rand_qty,
                'OrdType': 'D',
                'ExpireTime': self.reusable_params['SettlDate'] + '-23:59:00.000',
                'TransactTime': (datetime.utcnow().isoformat())
            }]
        }

        quote_canceled = self.act.placeQuoteFIX(
            bca.convert_to_request(
                'Send RFQ_Canceled',
                self.case_params['TraderConnectivity'],
                self.case_id,
                bca.message_to_grpc('QuoteRequest', rfq_params_canceled, self.case_params['TraderConnectivity'])
            ))

        self.can_qty = self.comma_qty(rfq_params_canceled['NoRelatedSymbols'][0]['OrderQty'])
        self.rfq_qty_list.append('Canceled RFQ: ' + self.can_qty)

        quote_params_can = {
            **self.reusable_params,
            'QuoteReqID': rfq_params_canceled['QuoteReqID'],
            'OfferPx': 35.001,
            'OfferSize': rfq_params_canceled['NoRelatedSymbols'][0]['OrderQty'],
            'QuoteID': '*',
            'OfferSpotRate': '35.001',
            'ValidUntilTime': '*',
            'Currency': 'EUR',
            'QuoteType': 1
        }

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Quote Received',
                bca.filter_to_grpc('Quote', quote_params_can, ['QuoteReqID']),
                quote_canceled.checkpoint_id,
                self.case_params['TraderConnectivity'],
                self.case_id
            )
        )
        # logger.info(quote_canceled.response_messages_list[0].fields['QuoteReqID'].simple_value)

        cancel_quote_params = {
            'QuoteReqID': quote_canceled.response_messages_list[0].fields['QuoteReqID'].simple_value,
            'QuoteCancelType': 5,
            'QuoteID': quote_canceled.response_messages_list[0].fields['QuoteID'].simple_value
        }

        self.act.sendMessage(
            bca.convert_to_request(
                'Send QuoteCancel',
                self.case_params['TraderConnectivity'],
                self.case_id,
                bca.message_to_grpc('QuoteCancel', cancel_quote_params, self.case_params['TraderConnectivity'])
            ))

        # RFQ parameters for receive Status Terminated
        rfq_params_terminated = {
            'QuoteReqID': bca.client_orderid(9),
            'NoRelatedSymbols': [{
                **self.reusable_params,
                'Currency': 'EUR',
                'QuoteType': '1',
                'OrderQty': 1300000 + self.rand_qty,
                'OrdType': 'D',
                'ExpireTime': self.reusable_params['SettlDate'] + '-23:59:00.000',
                'TransactTime': (datetime.utcnow().isoformat())
            }]
        }

        # Send RFQ_Terminated / Quote Executed
        rfq_term = self.act.placeQuoteFIX(
            bca.convert_to_request(
                'Send RFQ_Terminated',
                self.case_params['TraderConnectivity'],
                self.case_id,
                bca.message_to_grpc('QuoteRequest', rfq_params_terminated, self.case_params['TraderConnectivity'])
            ))

        self.term_qty = self.comma_qty(rfq_params_terminated['NoRelatedSymbols'][0]['OrderQty'])
        self.rfq_qty_list.append('Terminated RFQ: ' + self.term_qty)

        quote_params = {
            **self.reusable_params,
            'QuoteReqID': rfq_params_terminated['QuoteReqID'],
            'OfferPx': 35.001,
            'OfferSize': rfq_params_terminated['NoRelatedSymbols'][0]['OrderQty'],
            'QuoteID': '*',
            'OfferSpotRate': '35.001',
            'ValidUntilTime': '*',
            'Currency': 'EUR',
            'QuoteType': 1
        }

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Quote Received',
                bca.filter_to_grpc('Quote', quote_params, ['QuoteReqID']),
                rfq_term.checkpoint_id,
                self.case_params['TraderConnectivity'],
                self.case_id
            )
        )

        # NewOrderSingle params for Quote Filled
        order_params = {
            **self.reusable_params,
            'QuoteID': rfq_term.response_messages_list[0].fields['QuoteID'],
            'ClOrdID': bca.client_orderid(9),
            'OrdType': 'D',
            'TransactTime': (datetime.utcnow().isoformat()),
            'OrderQty': rfq_params_terminated['NoRelatedSymbols'][0]['OrderQty'],
            'Price': rfq_term.response_messages_list[0].fields['OfferPx'].simple_value,
            'TimeInForce': 4
        }

        # Send NewOrderSingle for Quote Filled
        send_order = self.act.placeOrderFIX(
            bca.convert_to_request(
                "Send NewOrderSingle",
                self.case_params['TraderConnectivity'],
                self.case_id,
                bca.message_to_grpc('NewOrderSingle', order_params, self.case_params['TraderConnectivity'])
            ))

        er_pending_params = {
            'Side': self.reusable_params['Side'],
            'Account': self.reusable_params['Account'],
            'ClOrdID': order_params['ClOrdID'],
            'OrderQty': order_params['OrderQty'],
            'LeavesQty': order_params['OrderQty'],
            'TimeInForce': order_params['TimeInForce'],
            'OrdType': order_params['OrdType'],
            'Price': rfq_term.response_messages_list[0].fields['OfferPx'].simple_value,
            'OrderID': send_order.response_messages_list[0].fields['OrderID'].simple_value,
            'NoParty': [
                {'PartyRole': 36, 'PartyID': 'gtwquod5', 'PartyIDSource': 'D'}
            ],
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityIDSource': 8,
                'SecurityID': 'EUR/USD',
                'SecurityExchange': 'XQFX',
                'Product': 4
            },
            'SettlCurrency': 'USD',
            'Currency': 'EUR',
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
            'Side': self.reusable_params['Side'],
            'Account': self.reusable_params['Account'],
            'SettlDate': self.reusable_params['SettlDate'],
            'TradeDate': datetime.utcnow().strftime('%Y%m%d'),
            'SettlType': self.reusable_params['SettlType'],
            'ClOrdID': order_params['ClOrdID'],
            'OrderQty': order_params['OrderQty'],
            'LeavesQty': 0,
            'TimeInForce': order_params['TimeInForce'],
            'OrdType': order_params['OrdType'],
            'Price': rfq_term.response_messages_list[0].fields['OfferPx'].simple_value,
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
            'AvgPx': rfq_term.response_messages_list[0].fields['OfferPx'].simple_value,
            'QtyType': 0,
            'LastQty': order_params['OrderQty'],
            'CumQty': order_params['OrderQty'],
            'LastPx': rfq_term.response_messages_list[0].fields['OfferPx'].simple_value,
            'OrdStatus': 2,
            'ExecType': 'F',
            'ExecID': '*',
            'TransactTime': '*',
            'LastSpotRate': 35.001,
            'OrderCapacity': 'A',
            'ExDestination': 'XQFX',
            'GrossTradeAmt': '*'
        }

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Receive ExecutionReport Filled',
                bca.filter_to_grpc('ExecutionReport', er_filled_params, ['ClOrdID', 'OrdStatus', 'ExecType']),
                send_order.checkpoint_id,
                self.case_params['TraderConnectivity'],
                self.case_id
            )
        )
        print("\n".join(self.rfq_qty_list))

    # FE open method
    def prepare_frontend(self):
        prepare_fe303(self.case_id, self.session_id, self.work_dir, self.user, self.password)

    # Check QuoteRequestBook method
    def check_qrb(self, qty, status, q_status):
        execution_id = bca.client_orderid(4)
        qrb = QuoteDetailsRequest(base=self.base_request)
        qrb.set_extraction_id(execution_id)
        qrb.set_filter(["Qty", qty])
        qrb_user = ExtractionDetail('quoteRequestBook.user', 'User')
        qrb_status = ExtractionDetail('quoteRequestBook.status', 'Status')
        qrb_quote_status = ExtractionDetail('quoteRequestBook.quotestatus', 'QuoteStatus')
        qrb.add_extraction_details([qrb_user, qrb_status, qrb_quote_status])

        request = call(self.ar_service.getQuoteRequestBookDetails, qrb.request())

        cust_verifier = Verifier(self.case_id)
        cust_verifier.set_event_name('Checking RFQ Status: ' + status + '/' + q_status)
        cust_verifier.compare_values('QRB User', 'gtwquod5', request[qrb_user.name])
        cust_verifier.compare_values('QRB Status', status, request[qrb_status.name])
        cust_verifier.compare_values('QRB QuoteStatus', q_status, request[qrb_quote_status.name])
        cust_verifier.verify()

    def reopen_fe(self):
        close_app_request = CloseApplicationRequest()
        close_app_request.set_default_params(self.base_request)
        self.common_act.closeApplication(close_app_request.build())

        open_app_req = OpenApplicationRequest()
        open_app_req.set_session_id(self.session_id)
        open_app_req.set_parent_event_id(self.case_id)
        open_app_req.set_work_dir(self.work_dir)
        open_app_req.set_application_file(Stubs.custom_config['qf_trading_fe_exec'])
        self.common_act.openApplication(open_app_req.build())

        login_details_req = LoginDetailsRequest()
        login_details_req.set_session_id(self.session_id)
        login_details_req.set_parent_event_id(self.case_id)
        login_details_req.set_username(self.user)
        login_details_req.set_password(self.password)
        login_details_req.set_main_window_name(Stubs.custom_config['qf_trading_fe_main_win_name_303'])
        login_details_req.set_login_window_name(Stubs.custom_config['qf_trading_fe_login_win_name_303'])
        self.common_act.login(login_details_req.build())
        print("reopen is done")

    def execute(self):
        try:
            # Step 1 Send RFQs via FIX
            self.send_RFQ_via_FIX()
            time.sleep(100)
            # Open FE
            self.prepare_frontend()
            # Step 2 Check RFQs in FE
            self.check_qrb(self.qty_new, 'New', "")
            self.check_qrb(self.can_qty, 'Terminated', "Canceled")
            self.check_qrb(self.term_qty, 'Terminated', "Filled")
            self.check_qrb(self.rej_qty, 'Rejected', "")
            self.check_qrb(self.exp_qty, 'Terminated', "Expired")
            # Step 3 Close and open the FE
            self.reopen_fe()
            # Step 4 Check RFQs in FE again
            self.check_qrb(self.qty_new, 'New', "")
            self.check_qrb(self.can_qty, 'Terminated', "Canceled")
            self.check_qrb(self.term_qty, 'Terminated', "Filled")
            self.check_qrb(self.rej_qty, 'Rejected', "")
            self.check_qrb(self.exp_qty, 'Terminated', "Expired")
            close_fe(self.case_id, self.session_id)
        except Exception as e:
            logging.error('Error execution', exc_info=True)
