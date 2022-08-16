import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, \
    AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T8118(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.client = self.data_set.get_client('client_pt_1')
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')  # MOClient1_SA1
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.qty = "100000000"
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameters({'Account': self.client, 'OrderQtyData': {'OrderQty': self.qty}})
        price = self.fix_message.get_parameter("Price")
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                          self.venue_client_names,
                                                                                          self.venue,
                                                                                          float(price),
                                                                                          int(self.qty), 1)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)

        order_id = response[0].get_parameters()['OrderID']
        self.middle_office.book_order(filter=[OrderBookColumns.order_id.value, order_id])

        self.middle_office.approve_block()
        # endregion
        # region step 1
        allocation_param = [
            {AllocationsColumns.security_acc.value: self.alloc_account, AllocationsColumns.alloc_qty.value: self.qty}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.middle_office.allocate_block(filter=[MiddleOfficeColumns.order_id.value, order_id])
        allocation_qty = self.middle_office.extract_allocate_value(AllocationsColumns.alloc_qty.value)
        self.middle_office.compare_values({AllocationsColumns.alloc_qty.value: "100,000,000"}, allocation_qty,
                                          'Comparing allocation qty')
        # endregion
