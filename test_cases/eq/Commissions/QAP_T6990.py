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
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T6990(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '6988'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.venue = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_pt_10')
        self.alloc_account = self.data_set.get_account_by_name('client_pt_10_acc_1')
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_backend.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_backend.xml"
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)
        # endregion
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set agent fees precondition
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        agent_fee_type = self.data_set.get_misc_fee_type_by_name('agent')
        commission_profile = self.data_set.get_comm_profile_by_name('abs_amt')
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
        # region create CO  and partially fill it step 1
        self.submit_request.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                   desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                   role=SubmitRequestConst.USER_ROLE_1.value)
        self.submit_request.update_fields_in_component("NewOrderSingleBlock", {
            "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            'OrdQty': self.qty, 'Currency': self.currency, 'AccountGroupID': self.client, 'Price': self.price})
        self.java_api_manager.send_message_and_receive_response(self.submit_request)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)["OrdID"]
        cl_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)["ClOrdID"]
        allocation_qty = str(int(int(self.qty) / 2))
        self.trade_request.set_default_trade(order_id, self.price, allocation_qty)
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock", {'CounterpartList': {'CounterpartBlock':
            [self.data_set.get_counterpart_id_java_api(
                'counterpart_contra_firm')]}})
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        # endregion
        # region check actually  result from step 1
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        expected_result = {"TransExecStatus": "PFL"}
        self.java_api_manager.compare_values(expected_result, exec_reply, "Compare TransExecStatus")
        # endregion
        # region step 2
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        # endregion
        # region check actually result from step 2
        ord_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        expected_result = {"TransExecStatus": "FIL"}
        self.java_api_manager.compare_values(expected_result, ord_reply, "Compare TransExecStatus 2")
        # endregion
        # region step 3
        self.complete_message.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_message)
        # endregion
        # region check actually result from step 3
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        expected_result = {"MatchStatus": "MAT", "AllocSummaryStatus": "MAG", "AllocStatus": "ACK", "AllocType": "P"}
        self.java_api_manager.compare_values(expected_result, alloc_report, "Compare Block")
        self.java_api_manager.key_is_absent("CommissionDataBlock", expected_result, "Fee is absent")
        conf_report = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
            JavaApiFields.ConfirmationReportBlock.value
        ]
        expected_result = {"AffirmStatus": "AFF", "AllocSummaryStatus": "MAG", "MatchStatus": "MAT"}
        self.java_api_manager.compare_values(expected_result, conf_report, "Compare Alloc")
        self.java_api_manager.key_is_absent("CommissionDataBlock", conf_report, "Fee is absent")

        # region check 35=8 message
        execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_message.change_parameters({"ClOrdID": cl_ord_id, "Account": self.client,
                                            'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price})
        execution_report.set_default_calculated(self.fix_message)
        execution_report.remove_parameter('Parties')
        execution_report.remove_parameter('TradeReportingIndicator')
        execution_report.change_parameters({'NoMiscFees': [{'MiscFeeAmt': '*', 'MiscFeeCurr': self.currency_post_trade,
                                                            'MiscFeeType': '12'}]})
        ignored_fields = ["SettlCurrency", "PositionEffect", "SettlType", "AvgPx", "Currency", "tag5120", "NoParty",
                          "ExecBroker", "BookID", "QuodTradeQualifier", "NoParty", "RootSettlCurrency", "Account",
                          "RootSettlCurrFxRateCalc", "RootSettlCurrFxRate", "RootSettlCurrAmt", "CommissionData",
                          "Instrument", "SettlCurrFxRate", "SettlCurrFxRateCalc", "SettlCurrAmt",
                          "AllocInstructionMiscBlock2"]
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=ignored_fields)
        # endregion

        # region step 6
        allocation_report = FixMessageAllocationInstructionReportOMS()
        allocation_report.set_default_ready_to_book(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(allocation_report, ignored_fields=ignored_fields)
        allocation_report.change_parameters({'NoAllocs': [{'AllocAccount': self.alloc_account, 'AllocQty': self.qty,
                                                           'AllocSettlCurrAmt': '*', 'AllocSettlCurrency': '*',
                                                           'SettlCurrAmt': '*', 'SettlCurrFxRate': '*',
                                                           'SettlCurrFxRateCalc': '*', 'IndividualAllocID': '*',
                                                           'AllocNetPrice': '*', 'AllocPrice': '*',
                                                           'AllocInstructionMiscBlock2': '*'}], 'AllocType': '2'})
        self.fix_verifier.check_fix_message_fix_standard(allocation_report, ignored_fields=ignored_fields)
        confirmation_report = FixMessageConfirmationReportOMS(self.data_set)
        confirmation_report.set_default_confirmation_new(self.fix_message)
        confirmation_report.change_parameters({'AllocQty': self.qty,
                                               'AllocAccount': self.alloc_account})
        self.fix_verifier.check_fix_message_fix_standard(confirmation_report, ['ClOrdID', 'OrdStatus', 'AllocAccount'],
                                                         ignored_fields=ignored_fields)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart all")
        time.sleep(120)
        os.remove("temp.xml")
