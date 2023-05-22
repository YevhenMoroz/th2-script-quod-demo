import logging
import os
import time
from pathlib import Path

from pkg_resources import resource_filename
import xml.etree.ElementTree as ET
from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, \
    AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T6987(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.bs_connectivity = self.fix_env.buy_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.client_acc = self.data_set.get_account_by_name('client_counterpart_1_acc_1')
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_counterpart_1_venue_1")
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.cur = self.data_set.get_currency_by_name('currency_1')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.qty = '100'
        self.price = '20'
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.fix_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = ExecutionReportOMS(self.data_set)
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_backend.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_backend.xml"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set configuration on backend (precondition)
        tree = ET.parse(self.local_path)
        tree.getroot().find("automaticCalculatedReportEnabled").text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_book_agent_misc_fee_type_on_N')
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS QUOD.ESBUYTH2TEST")
        time.sleep(120)
        # endregion

        # region send fee
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        commission_profile_perc = self.data_set.get_comm_profile_by_name('perc_qty')
        fee_type = self.data_set.get_misc_fee_type_by_name('agent')
        fee_charge_type = self.data_set.get_misc_fee_type_by_name('local_comm')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('paris')
        params = {'miscFeeCategory': fee_charge_type, 'instrType': instr_type, "venueID": venue_id}

        self.rest_commission_sender.set_modify_fees_message(comm_profile=commission_profile_perc,
                                                            fee_type=fee_type)
        self.rest_commission_sender.change_message_params(params)
        self.rest_commission_sender.send_post_request()
        # endregion

        # region create Algo order (precondition)
        qty_to_display = str(float(self.qty) / 2)
        self.order_submit.set_default_iceberg_limit()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'DisplayInstructionBlock': {'DisplayQty': qty_to_display, 'DisplayMethod': "Initial"}, 'OrdQty': self.qty,
            "Price": self.price, 'AccountGroupID': self.client, 'PreTradeAllocationBlock': {
                'PreTradeAllocationList': {'PreTradeAllocAccountBlock': [
                    {'AllocAccountID': self.client_acc,
                     'AllocQty': self.qty}]}}})
        nos_rule = None
        trade_rule1 = None
        trade_rule2 = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity,
                self.client_for_rule,
                self.mic,
                int(self.price))
            trade_rule1 = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.client_for_rule,
                                                                                            self.mic,
                                                                                            int(self.price),
                                                                                            int(int(self.qty) / 2), 2)
            trade_rule2 = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.client_for_rule,
                                                                                            self.mic,
                                                                                            int(self.price),
                                                                                            int(int(self.qty) / 2), 2)
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule1)
            self.rule_manager.remove_rule(trade_rule2)
        # endregion

        # region check calculated execution (step 3)
        fee_list = {JavaApiFields.MiscFeeType.value: ExecutionReportConst.MiscFeeType_AGE.value,
                    JavaApiFields.MiscFeeAmt.value: '5.0',
                    JavaApiFields.MiscFeeCurr.value: self.cur,
                    JavaApiFields.MiscFeeBasis.value: ExecutionReportConst.MiscFeeBasis_A.value,
                    JavaApiFields.MiscFeeRate.value: '5.0'}
        calc_exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                  ExecutionReportConst.ExecType_CAL.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.MiscFeesList.value: {
            JavaApiFields.MiscFeesBlock.value: [
                fee_list]}, JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            calc_exec_report, 'Check Agent fee in the Calculated report (step 3)')
        cl_ord_id = calc_exec_report[JavaApiFields.ClOrdID.value]
        ord_id = calc_exec_report[JavaApiFields.OrdID.value]
        # endregion

        # region check 35=8 (39=B) (step 4)
        ignored_list = ['ExecID', 'M_PreAllocGrp', 'GatingRuleCondName', 'OrderQtyData', 'LastQty', 'GatingRuleName',
                        'TransactTime', 'DisplayInstruction', 'Side', 'AvgPx', 'QuodTradeQualifier', 'BookID',
                        'SettlCurrency', 'SettlDate', 'Currency', 'TimeInForce', 'PositionEffect', 'HandlInst',
                        'NoParty', 'CumQty', 'OrdType', 'LeavesQty',
                        'LastPx', 'LastPx', 'tag5120', 'OrderCapacity', 'QtyType', 'Price', 'ExecBroker',
                        'TargetStrategy', 'Instrument', 'ExDestination', 'GrossTradeAmt', 'CommissionData', 'SecondaryOrderID']
        params = {"Account": self.client, "ExecType": "B",
                  "OrdStatus": "B", "ClOrdID": cl_ord_id, 'OrderID': ord_id,
                  'NoMiscFees': {'NoMiscFees': [{'MiscFeeAmt': '5', 'MiscFeeCurr': self.cur, 'MiscFeeType': '12'}]}}
        fix_execution_report = FixMessageExecutionReportOMS(self.data_set, params)
        self.fix_verifier.check_fix_message_fix_standard(fix_execution_report, ignored_fields=ignored_list)
        # endregion

        # region check allocation (step 5)
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                              AllocationReportConst.AllocStatus_ACK.value).get_parameters()
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocationReportBlock.value: JavaApiFields.RootMiscFeesList.value},
            alloc_report, 'Check Agent fee is absent in the Allocation report (step 5)',
            VerificationMethod.NOT_CONTAINS)
        alloc_block = alloc_report[JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value},
            alloc_block, 'Check block status (step 5)')
        # endregion

        # region check confirmation (step 6)
        conf_report = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()
        self.java_api_manager.compare_values(
            {JavaApiFields.ConfirmationReportBlock.value: JavaApiFields.RootMiscFeesList.value},
            conf_report, 'Check Agent fee is absent in the Confirmation report (step 6)',
            VerificationMethod.NOT_CONTAINS)
        conf_block = conf_report[JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value},
            conf_block, 'Check block status (step 6)')
        # endregion

        # region check 35=J (626=5) (step 7)
        alloc_ignored_list = ['Account', 'TransactTime', 'Side', 'AvgPx', 'QuodTradeQualifier', 'BookID',
                              'SettlDate', 'AllocID', 'Currency', 'NetMoney', 'TradeDate', 'NoParty',
                              'RootSettlCurrency', 'AllocInstructionMiscBlock1', 'Quantity', 'ExecAllocGrp', 'tag5120',
                              'AllocTransType',
                              'ReportedPx', 'RootSettlCurrAmt', 'GrossTradeAmt', 'NoAllocs', 'Instrument']
        params = {'NoOrders': [{
            'ClOrdID': "*",
            'OrderID':ord_id,
            'OrderAvgPx': self.price,
        }], 'Account': self.client, 'BookingType': '0', 'AllocType': '5', 'NoRootMiscFeesList': '#'}
        alloc_instr_report = FixMessageAllocationInstructionReportOMS(params)
        self.fix_verifier.check_fix_message_fix_standard(alloc_instr_report, key_parameters=['AllocType', 'NoOrders'],
                                                         ignored_fields=alloc_ignored_list)
        # endregion

        # region check 35=J (626=2) (step 7)
        params = {'AllocType': '2'}
        alloc_instr_report.change_parameters(params)
        self.fix_verifier.check_fix_message_fix_standard(alloc_instr_report, key_parameters=['AllocType', 'NoOrders'],
                                                         ignored_fields=alloc_ignored_list)
        # endregion

        # region check 35=AK (step 7)
        conf_ignored_list = ['AllocQty', 'TransactTime', 'Side', 'AvgPx', 'QuodTradeQualifier', 'BookID',
                             'SettlCurrency', 'SettlDate', 'AllocID', 'Currency', 'NetMoney', 'MatchStatus',
                             'TradeDate', 'NoParty',
                             'SettlCurrAmt', 'AllocInstructionMiscBlock1', 'tag11245', 'tag5120', 'CpctyConfGrp',
                             'ReportedPx',
                             'Instrument', 'GrossTradeAmt', 'ConfirmID']
        params = {'ConfirmTransType': "0",
                  'NoOrders': [{
                      'ClOrdID': '*',
                      'OrderID': ord_id,
                      'OrderAvgPx': self.price,
                  }], 'AllocAccount': self.client_acc, 'ConfirmType': '2',
                  'ConfirmStatus': '1', 'NoMiscFees': '#'}
        conf_report = FixMessageConfirmationReportOMS(self.data_set, params)
        self.fix_verifier.check_fix_message_fix_standard(conf_report, ignored_fields=conf_ignored_list)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command('~/quod/script/site_scripts/change_book_agent_misc_fee_type_on_N')
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS QUOD.ESBUYTH2TEST")
        time.sleep(120)
        os.remove("temp.xml")
        self.ssh_client.close()
