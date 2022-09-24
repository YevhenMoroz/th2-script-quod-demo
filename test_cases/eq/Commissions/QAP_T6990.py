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
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, PostTradeStatuses, \
    ExecSts, TradeBookColumns, SecondLevelTabs, Basis, FeeTypeForMiscFeeTab, MiddleOfficeColumns, \
    AllocationsColumns
import xml.etree.ElementTree as ET
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

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
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = os.path.abspath("test_framework\ssh_wrappers\oms_cfg_files\client_backend.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_backend.xml"
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
        self.fix_message.set_default_care_limit(instr='instrument_3')
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price,
             'Currency': self.currency, 'ExDestination': 'XEUR'})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        self.client_inbox.accept_order({OrderBookColumns.order_id.value: order_id})
        allocation_qty = str(int(int(self.qty) / 2))
        filter_list = [OrderBookColumns.order_id.value, order_id]
        filter_dict = {MiddleOfficeColumns.order_id.value: order_id}
        contra_firm = self.data_set.get_contra_firm('contra_firm_1')
        self.order_book.manual_execution(allocation_qty, price=self.price, contra_firm=contra_firm)
        # endregion

        # region check actually  result from step 1
        dict_of_extraction = {OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value}
        expected_result = {OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value}
        message = "Check values from expecter result of step 1"
        self.__check_expected_result_from_order_book(filter_list, expected_result, dict_of_extraction, message)
        # endregion

        # region step 2
        self.order_book.manual_execution(allocation_qty, price=self.price, contra_firm=contra_firm)
        # endregion

        # region check actually result from step 2
        dict_of_extraction = {OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value}
        expected_result = {OrderBookColumns.exec_sts.value: ExecSts.filled.value}
        message = message.replace('1', '2')
        self.__check_expected_result_from_order_book(filter_list, expected_result, dict_of_extraction, message)
        # endregion

        # region step 3
        self.order_book.complete_order(filter_list=filter_list)
        # endregion

        # region check actually result from step 3
        filter_list_block = [MiddleOfficeColumns.order_id.value, order_id]
        dict_of_extraction.clear()
        dict_of_extraction.update({OrderBookColumns.post_trade_status.value: OrderBookColumns.post_trade_status.value})
        expected_result = {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value}
        message = message.replace('2', '3')
        self.__check_expected_result_from_order_book(filter_list, expected_result, dict_of_extraction, message)
        expected_result.clear()
        expected_result.update({MiddleOfficeColumns.sts.value: MiddleOfficeColumns.accepted_sts.value,
                                MiddleOfficeColumns.match_status.value: MiddleOfficeColumns.matched_sts.value,
                                MiddleOfficeColumns.summary_status.value: MiddleOfficeColumns.matched_agreed_sts.value,
                                MiddleOfficeColumns.total_fees.value: ''})
        list_of_column = [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
                          MiddleOfficeColumns.summary_status.value, MiddleOfficeColumns.total_fees.value]
        self.__extract_and_check_value_from_block(list_of_column, filter_list_block, expected_result, message)
        actually_result_from_allocation = self.middle_office.extract_list_of_allocate_fields(
            [AllocationsColumns.sts.value, AllocationsColumns.match_status.value, AllocationsColumns.total_fees.value],
            filter_dict_block=filter_dict,
            clear_filter_from_block=True, allocate_number=1)
        self.middle_office.compare_values({AllocationsColumns.sts.value: AllocationsColumns.affirmed_sts.value,
                                           AllocationsColumns.match_status.value: AllocationsColumns.matced_sts.value,
                                           AllocationsColumns.total_fees.value: ''},
                                          actually_result_from_allocation,
                                          message)
        # endregion

        # region step 4
        list_of_column = [TradeBookColumns.fee_type.value, TradeBookColumns.rate.value, TradeBookColumns.basis.value,
                          TradeBookColumns.amount.value]
        rate = '1'
        filter_dict = {filter_list[0]: filter_list[1]}
        amount = str(round(int(rate) / 100, 2))
        avg_px = str(round(int(self.price) / 100, 1))
        exec_id = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                      [TradeBookColumns.exec_id.value], [3], filter_dict)[0]
        expected_result = [{TradeBookColumns.fee_type.value + '1': FeeTypeForMiscFeeTab.agent.value},
                           {TradeBookColumns.rate.value + '1': rate},
                           {TradeBookColumns.basis.value + '1': Basis.absolute.value},
                           {TradeBookColumns.amount.value + '1': amount}]
        message = message.replace('3', '4')
        self.__compare_values_of_fees(exec_id, expected_result, list_of_column, message)
        # endregion

        # region check 35=8 message step 5
        execution_report = FixMessageExecutionReportOMS(self.data_set)
        execution_report.set_default_calculated(self.fix_message)
        execution_report.remove_parameter('Parties')
        execution_report.remove_parameter('TradeReportingIndicator')
        execution_report.change_parameters({'QuodTradeQualifier': '*', 'BookID': '*',
                                            'Currency': self.currency, 'NoParty': '*', 'CommissionData': '*',
                                            'tag5120': '*', 'ExecBroker': '*',
                                            'NoMiscFees': [{
                                                'MiscFeeAmt': amount,
                                                'MiscFeeCurr': self.currency_post_trade,
                                                'MiscFeeType': '12'
                                            }]})
        self.fix_verifier.check_fix_message_fix_standard(execution_report)
        # endregion

        # region step 6
        allocation_report = FixMessageAllocationInstructionReportOMS()
        allocation_report.set_default_ready_to_book(self.fix_message)
        allocation_report.change_parameters({'AvgPx': avg_px, 'Currency': self.currency_post_trade,
                                             'tag5120': "*"})
        self.fix_verifier.check_fix_message_fix_standard(allocation_report)
        allocation_report.change_parameters({'NoAllocs': [{'AllocAccount': self.alloc_account,
                                                           'AllocQty': self.qty,
                                                           'IndividualAllocID': '*',
                                                           'AllocNetPrice': '*',
                                                           'AllocPrice': '*',
                                                           'AllocInstructionMiscBlock2': '*'
                                                           }],
                                             'AllocType': '2'})
        self.fix_verifier.check_fix_message_fix_standard(allocation_report)
        confirmation_report = FixMessageConfirmationReportOMS(self.data_set)
        confirmation_report.set_default_confirmation_new(self.fix_message)
        confirmation_report.change_parameters({'AvgPx': avg_px, 'Account': '*', 'Currency': self.currency_post_trade,
                                               'tag5120': '*', 'AllocInstructionMiscBlock2': '*'})
        confirmation_report.change_parameters({'AllocQty': self.qty,
                                               'AllocAccount': self.alloc_account})
        self.fix_verifier.check_fix_message_fix_standard(confirmation_report, ['ClOrdID', 'OrdStatus', 'AllocAccount'])
        # endregion

    def __check_expected_result_from_order_book(self, filter_list, expected_result, dict_of_extraction, message):
        self.order_book.set_filter(filter_list=filter_list)
        actual_result = self.order_book.extract_fields_list(
            dict_of_extraction)
        self.order_book.compare_values(expected_result, actual_result,
                                       message)

    def __extract_and_check_value_from_block(self, list_of_column, filter_list, expected_result, message):
        self.middle_office.clear_filter()
        actual_result = self.middle_office.extract_list_of_block_fields(list_of_column=list_of_column,
                                                                        filter_list=filter_list)
        print(actual_result)
        self.middle_office.compare_values(expected_result, actual_result, message)

    def __compare_values_of_fees(self, filter_dict, expected_result, list_of_column: list, message):
        for value in list_of_column:
            actual_result = self.trade_book.extract_sub_lvl_fields(
                [value], SecondLevelTabs.fees.value, 1, filter_dict)
            print(actual_result)
            self.order_book.compare_values(expected_result[list_of_column.index(value)], actual_result,
                                           message)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart all")
        time.sleep(120)
        os.remove("temp.xml")