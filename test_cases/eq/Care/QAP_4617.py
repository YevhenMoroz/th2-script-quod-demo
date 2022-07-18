import logging
import os
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, PostTradeStatuses, \
    DoneForDays
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_4015(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        self.qty = '300'
        self.qty_to_exec = "200"
        self.price = '30'
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message.change_parameter('Price', self.price)
        self.client_ord_id_filter = self.fix_message.get_parameter('ClOrdID')
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.case_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message1)



    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        # region create CO
        self.fix_manager.send_message_fix_standard(self.fix_message)
        self.client_inbox.accept_order()
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region manual exec
        self.order_book.manual_execution(qty=self.qty_to_exec, filter_dict={OrderBookColumns.order_id.value: order_id})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list({OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value})
        # endregion
        # region complete order
        self.order_book.complete_order(filter_list=[OrderBookColumns.order_id.value, order_id])
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list({OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value, OrderBookColumns.done_for_day.value: DoneForDays.yes.value})
        # endregion
        # region do split and extract error
        self.order_ticket.set_order_details()
        self.order_ticket.split_order()

    case_name = "QAP-4617"
    # region Declarations
    qty = "800"
    client = "CLIENT_FIX_CARE"
    price = "40"
    price2 = '200'
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion

    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    buy_connectivity = test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity()
    # endregion
    # region Create order via FIX
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    response = fix_message.pop('response')
    # endregion
    # region Check values in OrderBook
    eq_wrappers.accept_order('VETO', qty, price)
    order_id = eq_wrappers.get_order_id(base_request)
    eq_wrappers.manual_execution(base_request, str(int(int(qty) / 2)), price)
    eq_wrappers.complete_order(base_request)
    eq_wrappers.split_order(base_request, str(int(int(qty) / 2)), 'Limit', price)
    response = eq_wrappers.extract_error_order_ticket(base_request)
    print(response)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values('Error', "Error - [QUOD-24812] Invalid 'DoneForDay': " + order_id,
                            response['ErrorMessage'])
    verifier.verify()
