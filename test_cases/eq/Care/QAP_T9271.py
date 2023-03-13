import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T9271(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        self.qty = self.new_order_single.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.new_order_single.get_parameter('Price')
        self.firm_acount = self.data_set.get_account_by_name('client_pos_3_acc_3')
        self.firm = self.data_set.get_client_by_name('client_pos_3')
        self.price_to_fill = '5'
        self.price_to_replace_fill = '555'
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # STEP 1
        # region create orders
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        order_id = response[0].get_parameter("OrderID")
        # endregion

        # STEP 2
        # region do house fill
        self.trade_entry_message.set_default_trade(order_id, self.price_to_fill, self.qty)
        self.trade_entry_message.update_fields_in_component('TradeEntryRequestBlock',
                                                            {'SourceAccountID': self.firm_acount})
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        exec_id = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)[JavaApiFields.ExecID.value]
        # endregion

        # region check exec report for CLient
        ignored_list = ['GatingRuleCondName', 'GatingRuleName', 'Parties', 'QuodTradeQualifier', 'BookID',
                        'SettlCurrency', 'LastExecutionPolicy', 'TradeReportingIndicator', 'NoParty', 'tag5120',
                        'SecondaryOrderID', 'LastMkt', 'ExecBroker', 'VenueType', 'SecondaryExecID']
        self.exec_report.set_default_filled(self.new_order_single)
        self.fix_verifier_dc.check_fix_message_fix_standard(self.exec_report, ['Account', "ExecType"],
                                                            ignored_fields=ignored_list)
        # endregion

        # region check exec report for Firm
        self.exec_report.change_parameters({'Account': self.firm, 'Side': '2'})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.exec_report, ['Account', "ExecType"],
                                                            ignored_fields=ignored_list)
        # endregion

        # STEP 3
        # region amend house fill
        self.trade_entry_message.set_default_replace_execution(order_id, exec_id, self.price_to_replace_fill, self.qty)
        self.trade_entry_message.update_fields_in_component('TradeEntryRequestBlock',
                                                            {'SourceAccountID': self.firm_acount})
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        exec_id = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)[JavaApiFields.ExecID.value]
        # endregion

        # region check exec report for Firm
        ignored_list.extend(['ExecRefID'])
        self.exec_report.change_parameters({'ExecType': "G", 'Account': self.firm, 'Side': '2'})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.exec_report, ['Account', "ExecType"],
                                                            ignored_fields=ignored_list)
        # endregion

        # STEP 4
        # region cancel house fill
        self.trade_entry_message.set_default_cancel_execution(order_id, exec_id)
        self.trade_entry_message.update_fields_in_component('TradeEntryRequestBlock',
                                                            {'SourceAccountID': self.firm_acount})
        self.trade_entry_message.remove_fields_from_component('TradeEntryRequestBlock', ['TransactTime', 'LastMkt',
                                                                                         'TradeDate', 'SettlDate'])
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        # endregion

        # region check exec report for CLient
        self.exec_report.set_default_trade_cancel(self.new_order_single)
        self.fix_verifier_dc.check_fix_message_fix_standard(self.exec_report, ['Account', "ExecType", "OrdStatus"],
                                                            ignored_fields=ignored_list)
        # endregion

        # region check exec report for Firm
        self.exec_report.change_parameters({"OrdStatus": "2", 'Account': self.firm, 'Side': '2', 'ExecID': '*'})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.exec_report, ['Account', "ExecType"],
                                                            ignored_fields=ignored_list)
        # endregion
