import logging
import os
import time
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
import xml.etree.ElementTree as ET
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T7159(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '1000'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')
        self.venue = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_com_1')
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message_cancel = FixMessageOrderCancelRequestOMS()
        self.currency_major = self.data_set.get_currency_by_name('currency_2')
        self.fix_message_execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set agent fees precondition
        new_order_single = trade_rule = order_id = cancel_rule = None
        fee_type = self.data_set.get_misc_fee_type_by_name('regulatory')
        commission_profile = self.data_set.get_comm_profile_by_name('bas_amt')
        fee = self.data_set.get_fee_by_name('fee3')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('eurex')
        self.rest_commission_sender.clear_fees()
        on_calculated_exec_scope = self.data_set.get_fee_exec_scope_by_name('on_calculated')
        self.rest_commission_sender.set_modify_fees_message(fee_type=fee_type, comm_profile=commission_profile,
                                                            fee=fee)
        self.rest_commission_sender.change_message_params(
            {'commExecScope': on_calculated_exec_scope, 'instrType': instr_type, "venueID": venue_id})
        self.rest_commission_sender.send_post_request()
        # endregion

        # region create DMA  partially and partially filled  (step 1 and step 2)
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity,
                self.venue_client_names,
                self.venue,
                float(self.price)
            )
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_names,
                                                                                            self.venue,
                                                                                            float(self.price),
                                                                                            int(int(self.qty) / 2), 0
                                                                                            )
            self.fix_message.set_default_dma_limit(instr='instrument_3')
            self.fix_message.change_parameters(
                {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price,
                 'Currency': self.currency, 'ExDestination': 'XEUR'})
            self.responses = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        except Exception as E:
            logger.error(f"Error is {E}", exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region check expected result from step 2
        expected_result = '1'
        self.__compare_ord_status(expected_result)
        # endregion

        # region step 3 cancelling order via FIX
        try:
            cancel_rule = self.rule_manager.add_OrderCancelRequest(self.bs_connectivity, self.venue_client_names,
                                                                   self.venue, True)
            self.fix_message_cancel.set_default(self.fix_message)
            self.responses = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_cancel)
        except Exception as E:
            logger.error(f"Error is {E}", exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(cancel_rule)
        # endregion

        # region check expected result from step 3
        expected_result = '4'
        self.__compare_ord_status(expected_result)
        # endregion

        # region check 35=8 150 = B message
        self.fix_message_execution_report.set_default_calculated(self.fix_message)
        self.fix_message_execution_report.remove_parameter('Parties')
        amount = str(round((1 / 1000000) * 5000, 3))
        self.fix_message_execution_report.remove_parameter('TradeReportingIndicator')
        self.fix_message_execution_report.change_parameters({'QuodTradeQualifier': '*', 'BookID': '*',
                                                             'Currency': self.currency, 'NoParty': '*',
                                                             'CommissionData': '*',
                                                             'tag5120': '*', 'SecondaryOrderID': "*", 'ExecBroker': '*',
                                                             'NoMiscFees': [{
                                                                 'MiscFeeAmt': amount,
                                                                 'MiscFeeCurr': self.currency_major,
                                                                 'MiscFeeType': '1'
                                                             }]})

        self.fix_verifier.check_fix_message_fix_standard(self.fix_message_execution_report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()

    def __compare_ord_status(self, expected_result):
        ord_status = self.responses[len(self.responses)-1].get_parameters()['OrdStatus']
        key = "OrderStatus"
        self.java_api_manager.compare_values({key:expected_result}, {key: ord_status}, f"Comparing values for step of OrdStatus for {expected_result}")
