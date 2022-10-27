import logging

from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.PositionTransferInstructionOMS import \
    PositionTransferInstructionOMS
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7598(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pos_3')  # MOClient
        self.security_account = self.data_set.get_account_by_name('client_pos_3_acc_3')
        self.security_account_second = self.data_set.get_account_by_name('client_pos_3_acc_2')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.posit_transfer = PositionTransferInstructionOMS(self.data_set)
        self.qty_of_order = None
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create DMA via FIX (Precondition)
        list_of_accounts = [self.security_account, self.security_account_second]
        list_of_posit_qty_before_transfer = []
        for account in list_of_accounts:
            list_of_posit_qty_before_transfer.append(self.__get_posit_qty_by_account_via_creating_order(account))
        # endregion

        # region executing of  steps 1, 2, 3, 4, 5
        self.posit_transfer.set_default_transfer(self.security_account, self.security_account_second, self.qty_of_order)
        responses = self.java_api_manager.send_message_and_receive_response(self.posit_transfer)
        print_message("After Position Transfer", responses)
        list_of_posit_qty_after_transfer = []
        for account in list_of_accounts:
            list_of_posit_qty_after_transfer.append(
                self.java_api_manager.get_last_message(ORSMessageType.PositionReport.value, account). \
                    get_parameters()[JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                    JavaApiFields.PositionBlock.value][0][JavaApiFields.PositQty.value])

        index_source_account = list_of_accounts.index(self.security_account)
        index_destination_account = list_of_accounts.index(self.security_account_second)
        list_of_expected_posit_qty = [
            float(list_of_posit_qty_before_transfer[index_source_account]) - float(self.qty_of_order),
            float(list_of_posit_qty_before_transfer[index_destination_account]) + float(self.qty_of_order)]
        self.java_api_manager.compare_values(
            {JavaApiFields.PositQty.value: list_of_expected_posit_qty[index_source_account]},
            {JavaApiFields.PositQty.value: float(list_of_posit_qty_after_transfer[index_source_account])},
            f'Comparing value of {self.security_account}')
        self.java_api_manager.compare_values(
            {JavaApiFields.PositQty.value: list_of_expected_posit_qty[index_destination_account]},
            {JavaApiFields.PositQty.value: float(list_of_posit_qty_after_transfer[index_destination_account])},
            f'Comparing value of {self.security_account_second}')

    # endregion
    def __get_posit_qty_by_account_via_creating_order(self, account):
        self.fix_message.set_default_dma_limit()
        self.qty_of_order = self.fix_message.get_parameters()['OrderQtyData']['OrderQty']
        no_allocs: dict = {'NoAllocs': [
            {
                'AllocAccount': account,
                'AllocQty': self.qty_of_order
            }
        ]}
        self.fix_message.change_parameter('PreAllocGrp', no_allocs)
        self.fix_message.change_parameters(
            {'Side': '1', 'Account': self.client, 'ClOrdID': bca.client_orderid(9)})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        cl_ord_id = response[0].get_parameters()['ClOrdID']
        order_id = response[0].get_parameters()['OrderID']

        # region trade DMA order via JavaApi (Precondition)
        self.execution_report.set_default_trade(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message(f"Trade DMA order with {account}", responses)
        return self.java_api_manager.get_last_message(ORSMessageType.PositionReport.value, account). \
            get_parameters()[JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0][JavaApiFields.PositQty.value]
