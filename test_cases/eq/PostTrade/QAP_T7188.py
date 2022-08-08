import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7188(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '8089'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.client = self.data_set.get_client('client_pt_1')
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create order via fix (step 1)

        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameters(
            {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        cl_ord_id = response[0].get_parameters()['ClOrdID']
        order_id = response[0].get_parameters()['OrderID']
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        filter_list = [OrderBookColumns.cl_ord_id.value, cl_ord_id]
        self.client_inbox.accept_order(filter=filter_dict)
        self.order_book.manual_execution(self.qty, self.price, filter_dict=filter_dict)
        # endregion

        # region check message 35=8 54=5 150 = 0
        self.execution_report.set_default_new(self.fix_message)
        self.execution_report.remove_parameter('Parties').add_tag({'QuodTradeQualifier': '*'}).add_tag(
            {'BookID': '*'}).add_tag({'NoParty': '*'}). \
            add_tag({'tag5120': '*'}).add_tag({'ExecBroker': '*'})
        self.fix_verifier.check_fix_message_fix_standard(self.execution_report)
        # endregion

        # region check messgae 35=8 54=5 150=F
        self.execution_report.set_default_filled(self.fix_message)
        self.execution_report.remove_parameter('Parties').add_tag({'QuodTradeQualifier': '*'}).add_tag(
            {'BookID': '*'}).add_tag({'NoParty': '*'}). \
            add_tag({'tag5120': '*'}).add_tag({'ExecBroker': '*'}).remove_parameter('TradeReportingIndicator'). \
            remove_parameter('LastExecutionPolicy').remove_parameter('SettlCurrency').remove_parameter(
            'SecondaryOrderID')
        self.execution_report.add_tag({'LastMkt': '*'}).add_tag({'ExecBroker': '*'}).add_tag({'VenueType': '*'}). \
            remove_parameter('SecondaryExecID').add_tag({'NoParty': '*'})
        self.fix_verifier.check_fix_message_fix_standard(self.execution_report)
        # endregion

        # region book order step 3
        self.order_book.complete_order(filter_list=filter_list)
        filter_list = [OrderBookColumns.cl_ord_id.value, cl_ord_id]
        self.middle_office.book_order()
        # endregion

        # check 35=J 54=5 626=5 message
        allocation_report = FixMessageAllocationInstructionReportOMS()
        allocation_report.set_default_ready_to_book(self.fix_message)
        allocation_report.add_tag({'tag5120': '*'}).add_tag({'RootSettlCurrAmt': '*'})
        self.fix_verifier.check_fix_message_fix_standard(allocation_report)
        # endregion

        # region allocate CO order step 4
        self.middle_office.approve_block()
        arr_allocation_param = [{"Security Account": self.alloc_account, "Alloc Qty": self.qty}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=arr_allocation_param)
        self.middle_office.allocate_block([MiddleOfficeColumns.order_id.value, order_id])
        # endregion

        # region check 35=AK message
        confirmation_message = FixMessageConfirmationReportOMS(self.data_set)
        confirmation_message.set_default_confirmation_new(self.fix_message)
        confirmation_message.add_tag({'Account': '*'}).add_tag({'tag5120': '*'}) \
            .add_tag({'AllocInstructionMiscBlock2': '*'})
        self.fix_verifier.check_fix_message_fix_standard(confirmation_message)
        # endregion

        # region check 35=J message
        allocation_report.change_parameter('AllocType', '2')
        self.fix_verifier.check_fix_message_fix_standard(allocation_report.set_default_preliminary(self.fix_message))
        # endregion