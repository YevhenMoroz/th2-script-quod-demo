import logging
import os
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, PostTradeStatuses
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_5002(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.qty = '40000000'
        self.price = '20'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')  # XPAR
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create DMA order via fix
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.client_for_rule,
                                                                                                  self.exec_destination,
                                                                                                  float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.client_for_rule,
                                                                                            self.exec_destination,
                                                                                            float(self.price),
                                                                                            int(self.qty),
                                                                                            delay=0)
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters(
                {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client})
            response = self.fix_manager.send_message_and_receive_response(self.fix_message)
            # get Client Order ID
            cl_ord_id = response[0].get_parameters()['ClOrdID']
        except Exception as e:
            logger.error(f'{e}', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Verifying order Post Trade Status and Done For Day
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list({OrderBookColumns.qty.value: self.qty,
                                                 OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
                                                 OrderBookColumns.done_for_day.value: 'Yes'},
                                                'Comparing values after trading')
        # endregion

        # region Split Booking
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        split_param_1 = self.order_book.create_split_booking_parameter('15000000')
        split_param_2 = self.order_book.create_split_booking_parameter('25000000')
        self.order_book.split_book([split_param_1, split_param_2])
        # endregion

        # region Verifying values after Split Booking
        self.__verify_after_mass_action_for_block(1, [MiddleOfficeColumns.sts.value,
                                                      MiddleOfficeColumns.match_status.value,
                                                      MiddleOfficeColumns.qty.value], 'Book',
                                                  {MiddleOfficeColumns.sts.value: 'ApprovalPending',
                                                   MiddleOfficeColumns.match_status.value: 'Unmatched',
                                                   MiddleOfficeColumns.qty.value: '25,000,000'})
        self.__verify_after_mass_action_for_block(2, [MiddleOfficeColumns.sts.value,
                                                      MiddleOfficeColumns.match_status.value,
                                                      MiddleOfficeColumns.qty.value], 'Book',
                                                  {MiddleOfficeColumns.sts.value: 'ApprovalPending',
                                                   MiddleOfficeColumns.match_status.value: 'Unmatched',
                                                   MiddleOfficeColumns.qty.value: '15,000,000'})
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    def __verify_after_mass_action_for_block(self, row_number: int, list_of_column: list, after_action: str,
                                             dict_of_expected_result: dict):
        value_for_first_row = self.middle_office.extract_list_of_block_fields(list_of_column, row_number=row_number)
        self.middle_office.compare_values(dict_of_expected_result, value_for_first_row,
                                          f'Checking {row_number} row of the block after {after_action}')
