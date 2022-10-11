import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, PostTradeStatuses, \
    MiddleOfficeColumns, AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7149(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.client_acc = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_3")
        self.qty = self.fix_message.get_parameter("OrderQtyData")['OrderQty']
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.price = self.fix_message.get_parameter("Price")
        self.trades = OMSTradesBook(self.test_id, self.session_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.comm = self.data_set.get_commission_by_name("commission1")
        self.comm_profile = self.data_set.get_comm_profile_by_name("abs_amt_2")
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.comm_rate = "1.55"
        self.comm_basis = self.data_set.get_commission_basis('comm_basis_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(commission=self.comm,
                                                                         account=self.client_acc,
                                                                         comm_profile=self.comm_profile).send_post_request()
        # endregion
        # region send order
        self.__send_fix_orders()
        # endregion
        # region Check ExecutionReports
        self.exec_report.set_default_filled(self.fix_message)
        self.exec_report.change_parameters(
            {'Currency': self.cur, 'SecondaryOrderID': '*', 'Text': '*', 'LastMkt': '*',
             "ReplyReceivedTime": "*"})
        self.exec_report.remove_parameter('SettlCurrency')
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report)
        # endregion
        # region book order
        self.mid_office.book_order([OrderBookColumns.order_id.value, self.order_id])
        self.order_book.set_filter([OrderBookColumns.order_id.value, self.order_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value})
        # endregion
        # region approve and alllocate block
        self.mid_office.approve_block()
        param = [{AllocationsColumns.security_acc.value: self.client_acc,
                  AllocationsColumns.alloc_qty.value: self.qty}]
        self.mid_office.set_modify_ticket_details(is_alloc_amend=True, arr_allocation_param=param)
        self.mid_office.allocate_block([MiddleOfficeColumns.order_id.value, self.order_id])
        # endregion
        # region check allocation commission 1
        conf_report = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_new(
            self.fix_message)
        comm_data_1 = {"CommissionType": '3', "Commission": "0",
                       "CommCurrency": self.com_cur}
        conf_report.change_parameters(
            {"AllocQty": self.qty, "Account": self.client, "AllocAccount": self.client_acc, "AvgPx": "*",
             "Currency": "*", "tag5120": "*",
             "CommissionData": comm_data_1, 'NoOrders': [{'ClOrdID': self.cl_order_id, "OrderID": self.order_id}]})
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report, ["OrderID"])
        # endregion
        # region amend allocation
        self.mid_office.set_modify_ticket_details(is_alloc_amend=True, comm_rate=self.comm_rate, toggle_manual=True,
                                                  remove_comm=True, comm_basis=self.comm_basis)
        self.mid_office.amend_allocate([OrderBookColumns.order_id.value, self.order_id])
        # endregion
        # region check amended allocation commission
        comm_data_2 = {"CommissionType": '3', "Commission": self.comm_rate,
                       "CommCurrency": self.com_cur}
        conf_report2 = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_replace(self.fix_message)
        conf_report2.change_parameters(
            {"AllocQty": self.qty, "Account": self.client, "AllocAccount": self.client_acc, "AvgPx": "*",
             "Currency": "*", "tag5120": "*", "CommissionData": comm_data_2,
             'NoOrders': [{'ClOrdID': self.cl_order_id, "OrderID": self.order_id}]})
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report2, ["OrderID", "ConfirmTransType"])
        # endregion

    def __send_fix_orders(self):
        try:
            nos_rule = self.rule_manager. \
                add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(self.bs_connectivity,
                                                                         self.client_for_rule,
                                                                         self.mic,
                                                                         float(self.price), float(self.price),
                                                                         int(self.qty), int(self.qty), 1)
            self.fix_message.change_parameters(
                {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
                 "ExDestination": self.mic,
                 "Currency": self.data_set.get_currency_by_name("currency_3")})
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            self.order_id = self.response[0].get_parameter("OrderID")
            self.cl_order_id = self.response[0].get_parameter("ClOrdID")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
