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
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, PostTradeStatuses, \
    MiddleOfficeColumns, AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@try_except(test_id=Path(__file__).name[:-3])
class QAP_5881(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.client = self.data_set.get_client_by_name("client_pt_2")
        self.client_acc = self.data_set.get_account_by_name("client_pt_2_acc_1")
        self.case_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        self.fix_message.change_parameters({'Account': self.client, "OrderQtyData":{'OrderQty':self.qty}, "Price": self.price})
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.trades = OMSTradesBook(self.case_id, self.session_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.case_id, self.data_set)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.case_id)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_pt_2_venue_1")
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.client_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.case_id, self.session_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # endregion
        # region send commission
        self.rest_commission_sender.clear_commissions()
        # endregion
        # region create order
        order_id = self.__send_fix_orders()
        # endregion
        # region book order
        self.mid_office.set_modify_ticket_details(remove_comm=True, remove_fee=True)
        self.mid_office.book_order([OrderBookColumns.order_id.value, order_id])
        self.__verify_commissions()
        # endregion
        # region approve and allocate block
        self.mid_office.approve_block()
        allocation_values = [{"Security Account": self.client_acc,
                              "Alloc Qty": self.qty}]
        self.mid_office.set_modify_ticket_details(arr_allocation_param=allocation_values)
        self.mid_office.allocate_block()
        self.__check_allocation(AllocationsColumns.sts.value, AllocationsColumns.affirmed_sts.value, "Check allocation status")
        self.__check_allocation(AllocationsColumns.match_status.value, AllocationsColumns.matced_sts.value,
                                "Check allocation match status")
        self.__check_allocation(AllocationsColumns.total_fees.value, "0.03",
                                "Check allocation total fees")
        # endregion
        # region check confirmation message
        conf_report = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_new(
            self.fix_message)
        conf_report.change_parameters({'Account': self.client, "tag5120": "*", 'AllocInstructionMiscBlock2':"*", "MiscFeeType":"22"})
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def __send_fix_orders(self):
        nos_rule = None
        trade_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, int(self.price),
                                                                                            int(self.qty), 2)
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = self.response[0].get_parameter("OrderID")
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        return order_id


    @try_except(test_id=Path(__file__).name[:-3])
    def __verify_commissions(self):
        # region check booked order
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value})
        # endregion
        # region check total fees
        total_fees = self.mid_office.extract_block_field(MiddleOfficeColumns.total_fees.value)
        self.mid_office.compare_values({MiddleOfficeColumns.total_fees.value: ''}, total_fees, "Check Total Fees")
        # endregion
        # region check total fees
        total_comm = self.mid_office.extract_block_field(MiddleOfficeColumns.client_comm.value)
        self.mid_office.compare_values({MiddleOfficeColumns.client_comm.value: ''}, total_comm,
                                       "Check Total Comm")


    def __check_allocation(self, column:str, expected:str, name_of_varification:str):
        acc_res = self.mid_office.extract_allocate_value(column)
        self.mid_office.compare_values({column: expected}, acc_res,
                                          name_of_varification)



def execute(report_id, session_id):
    case_name = "QAP-5881"
    qty = "100"
    price = "10"
    client = "CLIENT_COMM_1"
    case_id = create_event(case_name, report_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    middle_office = OMSMiddleOffice(case_id, session_id)
    open_fe(session_id, report_id, case_id, work_dir, username)
    no_allocs: dict = {"NoAllocs": [{
        'AllocAccount': "CLIENT_COMM_1_SA4",
        'AllocQty': qty
    }]}
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(Connectivity.Ganymede_317_bs.value,
                                                                             client + '_PARIS', "XPAR", float(price))
        fix_manager = FixManager(Connectivity.Ganymede_317_ss.value, report_id)
        new_order_single1 = FixMessageNewOrderSingleOMS().set_default_dma_limit().add_ClordId(
            (os.path.basename(__file__)[:-3])).change_parameters(
            {'OrderQtyData': {'OrderQty': qty}, "Price": price, "Account": client, 'PreAllocGrp': no_allocs})
        new_order_single2 = FixMessageNewOrderSingleOMS().set_default_dma_limit().add_ClordId(
            (os.path.basename(__file__)[:-3])).change_parameters(
            {'OrderQtyData': {'OrderQty': qty}, "Price": price, "Account": client, 'PreAllocGrp': no_allocs,
             "Side": "2"})
        fix_manager.send_message_and_receive_response(new_order_single1)
        fix_manager.send_message_and_receive_response(new_order_single2)
    finally:
        time.sleep(2)
        rule_manager.remove_rule(nos_rule)

    middle_office.book_order()
    middle_office.approve_block()
    middle_office.allocate_block()
    middle_office.set_modify_ticket_details(is_alloc_amend=True, comm_rate="1.555", toggle_manual=True,
                                            remove_comm=True,
                                            comm_basis="Absolute")
    middle_office.amend_allocate()
    expected_value = middle_office.extract_allocate_value("Client Comm")
    middle_office.compare_values({"Client Comm": "1.555"}, expected_value,
                                 event_name='Compare commissions')
