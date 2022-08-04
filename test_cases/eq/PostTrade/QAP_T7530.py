import logging
import os
import time
from pathlib import Path

from th2_grpc_act_gui_quod.middle_office_pb2 import PanelForExtraction

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, \
    AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7530(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.case_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.middle_office = OMSMiddleOffice(self.case_id, self.session_id)

    # @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '200'
        price = '10'
        account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        rule_manager = RuleManager(Simulators.equity)
        trade_rule = None
        new_order_single_rule = None
        cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        # endregion

        # region create order
        try:
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, account, exec_destination, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side, account,
                                                                                       exec_destination, float(price),
                                                                                       int(qty), 0)
            self.fix_manager.send_message_fix_standard(self.fix_message)
        except Exception as ex:
            logger.exception(f'{ex} - your exception')

        finally:
            time.sleep(10)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)

        # endregion

        # region extract value from booking ticket (step 1)
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        post_trade_status = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        values = self.order_book.extracting_values_from_booking_ticket([PanelForExtraction.MISC],
                                                                       {OrderBookColumns.cl_ord_id.value:
                                                                            cl_ord_id})
        values = self.order_book.split_tab_misk(values)
        for count in range(1, len(values) + 1):
            self.order_book.compare_values({f'BOField{count}': f'BOC{count}'}, values[count - 1],
                                           'Comparing values of BO Fields')
        # endregion

        # region book and amend BO fields (step 2, step 3, step 4)
        self.middle_office.set_modify_ticket_details(
            bo_fields=['amendClient1', 'amendClient2', 'amendClient3', 'amendClient4', 'amendClient5'])
        fix_verifier = FixVerifier(self.fix_env.drop_copy, self.case_id)
        self.middle_office.book_order()
        fix_allocation_instruction = FixMessageAllocationInstructionReportOMS(). \
            set_default_ready_to_book(self.fix_message)
        fix_allocation_instruction.change_parameter('AllocInstructionMiscBlock1', {'BOMiscField0': 'amendClient1',
                                                                                   'BOMiscField1': 'amendClient2',
                                                                                   'BOMiscField2': 'amendClient3',
                                                                                   'BOMiscField3': 'amendClient4',
                                                                                   'BOMiscField4': 'amendClient5'})
        fix_allocation_instruction.add_tag({'tag5120': '*'})
        fix_allocation_instruction.add_tag({'RootSettlCurrFxRate': '*'})
        fix_allocation_instruction.add_tag({'RootSettlCurrAmt': '*'})
        fix_verifier.check_fix_message_fix_standard(fix_allocation_instruction)
        # endregion

        # region allocation block and check values at fix(step 5, step 6, step 7, step 8)
        self.middle_office.approve_block()
        allocation_values = [{"Security Account": self.data_set.get_account_by_name('client_pt_1_acc_2'),
                              "Alloc Qty": qty,
                              'Alloc BO Field 1': 'amendAccount1',
                              'Alloc BO Field 2': 'amendAccount2',
                              'Alloc BO Field 3': 'amendAccount3',
                              'Alloc BO Field 4': 'amendAccount4',
                              'Alloc BO Field 5': 'amendAccount5'}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_values)
        self.middle_office.allocate_block()
        fix_confirmation = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_new(self.fix_message)
        fix_confirmation.add_tag({'Account': '*'}).add_tag({'SettlCurrFxRate': '*'}).add_tag({'tag5120': '*'})
        fix_confirmation.add_tag({'AllocInstructionMiscBlock2': {'BOMiscField5': 'amendAccount1',
                                                                 'BOMiscField6': 'amendAccount2',
                                                                 'BOMiscField7': 'amendAccount3',
                                                                 'BOMiscField8': 'amendAccount4',
                                                                 'BOMiscField9': 'amendAccount5'}})
        fix_confirmation.change_parameter('AllocInstructionMiscBlock1', {'BOMiscField0': 'amendClient1',
                                                                         'BOMiscField1': 'amendClient2',
                                                                         'BOMiscField2': 'amendClient3',
                                                                         'BOMiscField3': 'amendClient4',
                                                                         'BOMiscField4': 'amendClient5'})
        fix_verifier.check_fix_message_fix_standard(fix_confirmation)
        # endregion
