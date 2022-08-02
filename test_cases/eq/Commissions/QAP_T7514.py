import logging
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, \
    SecondLevelTabs, PostTradeStatuses, MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7514(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client = self.data_set.get_client_by_name("client_pt_1")
        self.client_for_conf = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")
        self.price = "10"
        self.qty = "300"
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message.change_parameters(
            {"Account": self.client, 'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price})
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.all_acc = self.data_set.get_account_by_name('client_pt_1_acc_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region send fix message
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept order
        self.client_inbox.accept_order()
        # endregion
        # region manual exec order
        self.order_book.manual_execution(qty=self.qty, price=self.price,
                                         filter_dict={OrderBookColumns.cl_ord_id.value: self.cl_ord_id})
        exec_id = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                      [OrderBookColumns.exec_id.value], [1],
                                                      {OrderBookColumns.cl_ord_id.value: self.cl_ord_id})
        # endregion
        # region check exec
        execution_report = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message)
        execution_report.change_parameters(
            {'MiscFeesGrp': "*",  'CommissionData': "*", 'VenueType': "*", 'LastMkt': "*",
             "Account": self.client_for_conf})
        execution_report.remove_parameters(['SettlCurrency', 'LastExecutionPolicy', 'SecondaryOrderID', 'SecondaryExecID'])
        self.fix_verifier.check_fix_message_fix_standard(execution_report)
        # endregion
        # region complete order
        self.order_book.complete_order(filter_list=[OrderBookColumns.cl_ord_id.value, self.cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value})
        # endregion
        # region book order
        self.mid_office.set_modify_ticket_details(comm_basis="Absolute", comm_rate="100", toggle_manual=True)
        self.mid_office.book_order([OrderBookColumns.cl_ord_id.value, self.cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value})
        # endregion
        # region approve and allocate order
        self.mid_office.approve_block()
        param = [{"Security Account": self.all_acc, "Alloc Qty": self.qty}]
        self.mid_office.set_modify_ticket_details(is_alloc_amend=True, arr_allocation_param=param)
        self.mid_office.allocate_block([MiddleOfficeColumns.order_id.value, order_id])
        # endregion
        # region Check Conf report
        conf_report = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_new(
            self.fix_message)
        conf_report.change_parameters(
            {"CommissionData": {"Commission": "100", "CommissionType": "3", "CommCurrency": "EUR"}, "NoMiscFees": "*",
             "tag5120": "*", "AllocInstructionMiscBlock2": "*", "Account": self.client})
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report)
        # endregion
