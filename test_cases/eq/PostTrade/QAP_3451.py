import logging
import os
import time
import typing
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.ReadLogVerifier import ReadLogVerifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_3411(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.middle_office = OMSMiddleOffice(self.case_id, self.session_id)
        self.read_log_conn = self.environment.get_list_read_log_environment()[0].read_log_conn

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '200'
        price = '10'
        new_price = '20'
        account_first = self.data_set.get_account_by_name('client_pt_2_acc_1')
        no_allocs: typing.Dict[str, list] = {'NoAllocs': [
            {
                'AllocAccount': account_first,
                'AllocQty': str(int(int(qty) / 2)),
            },
            {
                'AllocAccount': self.data_set.get_account_by_name('client_pt_2_acc_2'),
                'AllocQty': str(int(int(qty) / 2))
            }]}
        account = self.data_set.get_venue_client_names_by_name('client_pt_2_venue_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_2'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('PreAllocGrp', no_allocs)
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        rule_manager = RuleManager(Simulators.equity)
        read_log_verifier = ReadLogVerifier(self.read_log_conn, self.case_id)
        trade_rule = None
        new_order_single_rule = None
        # endregion

        # region Create dma order
        try:

            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, account, exec_destination, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                       account,
                                                                                       exec_destination,
                                                                                       float(price),
                                                                                       int(qty), 0)
            self.fix_manager.send_message_fix_standard(self.fix_message)
        except Exception as ex:
            logger.exception(f'{ex} - your exception')
            bca.create_event('Exception regarding rules', self.case_id, status='FAIL')

        finally:
            time.sleep(10)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)
        # endregion
        # region Check ALS logs Status New
        als_logs_params = {
            "ConfirmationID": "*",
            "ConfirmStatus": "New",
            "ClientAccountID": account_first
        }
        read_log_verifier.check_read_log_message(als_logs_params, ["ConfirmStatus"], timeout=50000)
        # endregion
        # region amend allocate
        self.middle_office.set_modify_ticket_details(is_alloc_amend=True,agreed_price=new_price)
        self.middle_office.amend_allocate()
        # endregion
        # region Check ALS logs Status Canceled
        als_logs_params = {
            "ConfirmationID": "*",
            "ConfirmStatus": "Replace",
            "ClientAccountID": account_first
        }
        read_log_verifier.check_read_log_message(als_logs_params, ["ConfirmStatus"], timeout=50000)
        # endregion
