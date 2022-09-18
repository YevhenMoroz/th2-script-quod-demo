import logging
import os
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
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


class QAP_T7035(TestCase):
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
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.currency_major = self.data_set.get_currency_by_name('currency_2')
        self.fix_message_execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = os.path.abspath("test_framework\ssh_wrappers\oms_cfg_files\client_backend.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_backend.xml"
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set agent fees precondition
        new_order_single = trade_rule = order_id = cancel_rule = None
        agent_fee_type = self.data_set.get_misc_fee_type_by_name('regulatory')
        commission_profile = self.data_set.get_comm_profile_by_name('bas_amt')
        fee = self.data_set.get_fee_by_name('fee3')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('eurex')
        self.rest_commission_sender.clear_commissions()
        on_calculated_exec_scope = self.data_set.get_fee_exec_scope_by_name('on_calculated')
        self.rest_commission_sender.set_modify_fees_message(fee_type=agent_fee_type, comm_profile=commission_profile,
                                                            fee=fee)
        self.rest_commission_sender.change_message_params(
            {'commExecScope': on_calculated_exec_scope, 'instrType': instr_type, "venueID": venue_id})
        self.rest_commission_sender.send_post_request()
        # endregion

        # region set configuration on backend (precondition)
        tree = ET.parse(self.local_path)
        element = ET.fromstring("<automaticCalculatedReportEnabled>true</automaticCalculatedReportEnabled>")
        quod = tree.getroot()
        quod.append(element)
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart all")
        time.sleep(120)
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
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameters()['OrderID']
        except Exception as E:
            logger.error(f"Error is {E}", exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single)
            self.rule_manager.remove_rule(trade_rule)
            filter_list = [OrderBookColumns.order_id.value, order_id]
        # endregion

        # region check expected result from step 2
        self.order_book.set_filter(filter_list)
        values = self.order_book.extract_fields_list({OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value})
        self.order_book.compare_values({OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value}, values,
                                       'Comparing values after partially filled')
        # endregion

        # region step 3 cancelling order via FIX
        try:
            cancel_rule = self.rule_manager.add_OrderCancelRequest(self.bs_connectivity, self.venue_client_names,
                                                                   self.venue, True)
            self.order_book.cancel_order(filter_list=filter_list)
        except Exception as E:
            logger.error(f"Error is {E}", exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(cancel_rule)
        # endregion

        # region check expected result from step 3
        self.order_book.set_filter(filter_list)
        values = self.order_book.extract_fields_list(
            {OrderBookColumns.sts.value: OrderBookColumns.sts.value})
        self.order_book.compare_values({OrderBookColumns.sts.value: ExecSts.cancelled.value}, values,
                                       'Comparing values after cancel')
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
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart all")
        os.remove("temp.xml")
