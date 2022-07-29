import logging
import time
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, \
    SecondLevelTabs, PostTradeStatuses, MiddleOfficeColumns, DoneForDays, AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_child_order_book import OMSChildOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_4998(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client = self.data_set.get_client_by_name("client_pt_1")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")
        self.rule_manager = RuleManager(Simulators.equity)
        self.price = self.fix_message.get_parameter("Price")
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message.change_parameters({"Account": self.client})
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.child_book = OMSChildOrderBook(self.test_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.all_acc = self.data_set.get_account_by_name('client_pt_1_acc_1')


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region send fix message
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        care_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept order
        self.client_inbox.accept_order()
        # endregion
        # region check order is created
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(exec_report1)
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, int(self.price),
                                                                                            int(self.qty), 2)
            self.order_ticket.set_order_details(qty=self.qty)
            self.order_ticket.split_order([OrderBookColumns.order_id.value, care_id])
            # dma_id = self.order_book.extract_2lvl_fields(
            #     SecondLevelTabs.child_tab.value, [OrderBookColumns.order_id.value], [1],
            #     {OrderBookColumns.cl_ord_id.value: self.cl_ord_id})
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        # region check orders details
        self.order_book.set_filter([OrderBookColumns.order_id.value, care_id]).check_second_lvl_fields_list(
            {OrderBookColumns.sts.value: ExecSts.terminated.value, OrderBookColumns.cum_qty.value: self.qty})
        self.order_book.set_filter([OrderBookColumns.order_id.value, care_id]).check_order_fields_list(
            {OrderBookColumns.unmatched_qty.value: "0", OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # endregion
        # region complete order
        self.order_book.complete_order(filter_list=[OrderBookColumns.order_id.value, care_id])
        self.order_book.set_filter([OrderBookColumns.order_id.value, care_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value, OrderBookColumns.done_for_day.value: DoneForDays.yes.value})
        # endregion
        # region book order
        self.mid_office.book_order([OrderBookColumns.order_id.value, care_id])
        self.order_book.set_filter([OrderBookColumns.order_id.value, care_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value})
        self.order_book.set_filter([OrderBookColumns.order_id.value, care_id]).check_second_lvl_fields_list(
            {OrderBookColumns.post_trade_status.value: ""})
        self.__check_value_middle_office(MiddleOfficeColumns.sts.value, {"Status": MiddleOfficeColumns.appr_pending_sts.value}, [MiddleOfficeColumns.order_id.value, care_id])
        # endregion
        # region approve and allocate order
        self.mid_office.approve_block()
        param = [{"Security Account": self.all_acc, "Alloc Qty": self.qty}]
        self.mid_office.set_modify_ticket_details(is_alloc_amend=True, arr_allocation_param=param)
        self.mid_office.allocate_block([MiddleOfficeColumns.order_id.value, care_id])
        self.__check_value_middle_office(MiddleOfficeColumns.sts.value,
                                         {"Status": MiddleOfficeColumns.accepted_sts.value},
                                         [MiddleOfficeColumns.order_id.value, care_id])
        self.__check_value_middle_office(MiddleOfficeColumns.match_status.value,
                                         {"Match Status": MiddleOfficeColumns.matched_sts.value},
                                         [MiddleOfficeColumns.order_id.value, care_id])
        self.__check_value_middle_office(MiddleOfficeColumns.summary_status.value,
                                         {"Summary Status": MiddleOfficeColumns.matched_agreed_sts.value},
                                         [MiddleOfficeColumns.order_id.value, care_id])
        # endregion
        # region unallocate order
        self.mid_office.unallocate_order([MiddleOfficeColumns.order_id.value, care_id])
        self.__check_value_middle_office(MiddleOfficeColumns.sts.value,
                                         {"Status": MiddleOfficeColumns.accepted_sts.value},
                                         [MiddleOfficeColumns.order_id.value, care_id])
        self.__check_value_middle_office(MiddleOfficeColumns.match_status.value,
                                         {"Match Status": MiddleOfficeColumns.matched_sts.value},
                                         [MiddleOfficeColumns.order_id.value, care_id])
        self.__check_allocate_state([AllocationsColumns.sts.value, AllocationsColumns.match_status.value], AllocationsColumns.affirmed_sts.value,  {MiddleOfficeColumns.order_id.value: care_id})
        self.__check_allocate_state([AllocationsColumns.sts.value, AllocationsColumns.match_status.value],
                                    AllocationsColumns.affirmed_sts.value,
                                    {MiddleOfficeColumns.order_id.value: care_id})
        # endregion
        # region unbook order
        self.mid_office.un_book_order([OrderBookColumns.order_id.value, care_id])
        self.__check_value_middle_office(MiddleOfficeColumns.sts.value,
                                         {"Status": MiddleOfficeColumns.cancelled_sts.value},
                                         [MiddleOfficeColumns.order_id.value, care_id])
        self.__check_value_middle_office(MiddleOfficeColumns.match_status.value,
                                         {"Match Status": MiddleOfficeColumns.unmatched_sts.value},
                                         [MiddleOfficeColumns.order_id.value, care_id])
        self.order_book.set_filter([OrderBookColumns.order_id.value, care_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
             OrderBookColumns.done_for_day.value: DoneForDays.yes.value})
        # endregion
        # region uncomplete order
        self.order_book.un_complete_order(1, [OrderBookColumns.order_id.value, care_id])
        self.order_book.set_filter([OrderBookColumns.order_id.value, care_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: "",
             OrderBookColumns.done_for_day.value: ""})
        # endregion
        # region unmatch and transfer
        self.order_book.unmatch_and_transfer("Facilitation", {OrderBookColumns.cl_ord_id.value: self.cl_ord_id})
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.unmatched_qty.value: self.qty})
        # endregion
        # region check Check ExecType
        exec_type = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                        [OrderBookColumns.exec_type.value], [2],
                                                        {OrderBookColumns.cl_ord_id.value: self.cl_ord_id})
        self.order_book.compare_values({"ExecType": ExecSts.trade_cancel.value}, exec_type[0], "Check ExecType")
        # endregion
        # region check exec reports
        exec_report3 = FixMessageExecutionReportOMS(self.data_set).set_default_trade_cancel(self.fix_message)
        exec_report3.change_parameters({"ReplyReceivedTime": "*", "LastMkt": self.mic})
        exec_report3.remove_parameter('SettlCurrency')
        self.fix_verifier.check_fix_message_fix_standard(exec_report3)
        exec_report4 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(exec_report4)
        # endregion


    def __check_value_middle_office(self, field_name:str, expected_value:dict, filter_list:list = None):
        acc_res = self.mid_office.extract_block_field(field_name, filter_list)
        self.mid_office.compare_values(expected_value, acc_res,
                                           "Check middle office fields")

    def __check_allocate_state(self, fields_list:list, exp_res:str, filter:dict=None):
        act_res = self.mid_office.extract_list_of_allocate_fields(fields_list, filter_dict_block=filter)
        self.mid_office.compare_values({fields_list[0]: exp_res}, {fields_list[0]: act_res[fields_list[0]]}, 'Compare allocate values')
