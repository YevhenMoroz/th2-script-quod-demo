import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, \
    OrdTypes, ExecutionReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T9035(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = environment.get_list_fix_environment()[0]
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.venue = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_com_1')
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')  # MOClient_EUREX
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_backend.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_backend.xml"
        self.qty = '9035'
        self.price = '10'
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: set vat_fees fees
        # part 1: set up vat fees
        self.rest_commission_sender.clear_fees()
        agent_fee_type = self.data_set.get_misc_fee_type_by_name('value_added_tax')
        commission_profile = self.data_set.get_comm_profile_by_name('amt_plus_client')
        fee = self.data_set.get_fee_by_name('fee3')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('eurex')
        self.rest_commission_sender.set_modify_fees_message(comm_profile=commission_profile, fee=fee,
                                                            fee_type=agent_fee_type)
        self.rest_commission_sender.change_message_params({
            'venueID': venue_id,
            'instrType': instr_type,
            'miscFeeCategory': self.data_set.get_charges_type('charges')
        })
        self.rest_commission_sender.send_post_request()
        # end_of_part

        # part 2: Set Configuration for backend.xml
        tree = ET.parse(self.local_path)
        tree.getroot().find("execVATCommissionsEnable").text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart all")
        time.sleep(180)
        # end_of_part
        # endregion

        # region step 1: Create DMA order
        order_id = None
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                self.venue_client_names,
                self.venue,
                float(self.price))
            self.fix_message.set_default_dma_limit(instr='instrument_3')
            self.fix_message.change_parameters(
                {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price,
                 'Currency': self.currency, 'ExDestination': 'XEUR'})
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            execution_report_new = self.fix_manager.get_last_message('ExecutionReport').get_parameters()
            order_id = execution_report_new['OrderID']
            self.java_api_manager.compare_values({'ExecType': '0'}, execution_report_new,
                                                 'Verify that order created (step 1)')
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(new_order_single)
        # endregion

        # region step 2: Trade DMA order
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                         {
                                                             JavaApiFields.InstrumentBlock.value: self.data_set.get_java_api_instrument(
                                                                 "instrument_2"),
                                                             JavaApiFields.Side.value: SubmitRequestConst.Side_Buy.value,
                                                             JavaApiFields.LastTradedQty.value: self.qty,
                                                             JavaApiFields.LastPx.value: self.price,
                                                             JavaApiFields.OrdType.value: OrdTypes.Limit.value,
                                                             JavaApiFields.Price.value: self.price,
                                                             JavaApiFields.LeavesQty.value: self.qty,
                                                             JavaApiFields.CumQty.value: self.qty,
                                                             JavaApiFields.AvgPrice.value: self.price,
                                                             JavaApiFields.LastMkt.value: self.venue,
                                                             JavaApiFields.OrdQty.value: self.qty
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        exec_price = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value, ExecutionReportConst.ExecType_TRD.value).get_parameters()[JavaApiFields.ExecutionReportBlock.value][JavaApiFields.ExecPrice.value]
        fee_amt = str(float(exec_price) * (0.5 / 10000) * float(self.qty))
        list_ignored_fields = ['GatingRuleName', 'GatingRuleCondName',
                               'SettlCurrency', 'Currency', 'LastMkt',
                               'CommissionData']
        execution_report = FixMessageExecutionReportOMS(self.data_set)
        execution_report.set_default_filled(self.fix_message)
        execution_report.change_parameters({
            'MiscFeesGrp': {'NoMiscFees': [{'MiscFeeAmt': fee_amt, 'MiscFeeCurr': 'GBP', 'MiscFeeType': '22'}]}
        })
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_ignored_fields)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart all")
        time.sleep(180)
        os.remove("temp.xml")
        self.ssh_client.close()
