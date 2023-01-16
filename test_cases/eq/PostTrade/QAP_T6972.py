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
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst, \
    SubmitRequestConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.UnMatchRequest import UnMatchRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T6972(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.client = self.data_set.get_client('client_pt_1')
        self.position_account = self.data_set.get_account_by_name('client_pos_3_acc_4')
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.response = None
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.unmatching_request = UnMatchRequest()
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition
        tree = ET.parse(self.local_path)
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_2")
        tree.getroot().find("ors/FrontToBack/enforceParentPrice").text = 'false'
        tree.write("temp.xml")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(70)
        # endregion

        # region create order via fix (step 1)
        qty = '1500'
        price = '33.8'
        split_qty_for_child = str(float(qty) / 3)
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'AccountGroupID': self.client,
            'OrdQty': qty,
            'Price': price,
        })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Check expected and actually result form step 1')
        ord_id = order_reply[JavaApiFields.OrdID.value]
        # endregion

        # region split CO order(step 2)
        # part 1 : Create Child Dma order
        qty_of_first_child_dma_order = '10'
        self.order_submit.set_default_child_dma(ord_id)
        child_order_first_price = '32.7'
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'OrdQty': qty_of_first_child_dma_order,
            'Price': child_order_first_price,
            "ClOrdID": bca.client_orderid(9),
            'ExecutionPolicy': 'DMA'
        })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply_id_child = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id_first_child_dma_order = order_reply_id_child[JavaApiFields.OrdID.value]
        # endregion

        # region  step 3
        filter_for_message = {'OrdIdParent': ord_id,
                              'OrdIdChild': order_id_first_child_dma_order}
        self.execution_report.set_default_trade(order_id_first_child_dma_order)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             "OrdQty": qty_of_first_child_dma_order,
                                                             "Side": "Buy",
                                                             "LastTradedQty": qty_of_first_child_dma_order,
                                                             "LastPx": child_order_first_price,
                                                             "OrdType": "Limit",
                                                             "Price": child_order_first_price,
                                                             "Currency": "EUR",
                                                             "ExecType": "Trade",
                                                             "TimeInForce": "Day",
                                                             "LeavesQty": "0.0",
                                                             "CumQty": qty_of_first_child_dma_order,
                                                             "AvgPrice": child_order_first_price
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report, filter_for_message)
        execution_report_of_care_order = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                   f"'{JavaApiFields.OrdID.value}': '{ord_id}'").get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        execution_report_of_dma_order = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                               f"'{JavaApiFields.OrdID.value}': "
                                                                               f"'{order_id_first_child_dma_order}'").get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report_of_care_order[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_TER.value},
            execution_report_of_dma_order, 'Check expected and actually result from step 3')
        # endregion

        # region step 4 - Unmatch and Transfer
        self.unmatching_request.set_default(self.data_set, exec_id, qty_of_first_child_dma_order)
        self.unmatching_request.set_default_unmatch_and_transfer(self.position_account)
        self.java_api_manager.send_message_and_receive_response(self.unmatching_request)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value},
                                             execution_report, 'Check expected and actually result from step 4')
        # endregion

        # region step 5
        order_ids_child_list = []
        list_of_child_prices = ['34', '33.8', '34.2']
        for price_of_child_order in list_of_child_prices:
            self.order_submit.set_default_child_dma(ord_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                'OrdQty': split_qty_for_child,
                'Price': price_of_child_order,
                "ClOrdID": bca.client_orderid(9),
                'ExecutionPolicy': 'DMA'
            })
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply_id_child = \
                self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
            order_ids_child_list.append(order_reply_id_child[JavaApiFields.OrdID.value])
        # endregion

        # region expected result from 6 step
        list_of_execution_ids = []
        for child_order_id in order_ids_child_list:
            child_price = list_of_child_prices[order_ids_child_list.index(child_order_id)]
            self.execution_report.set_default_trade(child_order_id)
            self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                             {
                                                                 "OrdQty": split_qty_for_child,
                                                                 "Side": "Buy",
                                                                 "LastTradedQty": split_qty_for_child,
                                                                 "LastPx": child_price,
                                                                 "OrdType": "Limit",
                                                                 "Price": child_price,
                                                                 "Currency": "EUR",
                                                                 "ExecType": "Trade",
                                                                 "TimeInForce": "Day",
                                                                 "LeavesQty": "0.0",
                                                                 "CumQty": split_qty_for_child,
                                                                 "AvgPrice": child_price
                                                             })
            self.java_api_manager.send_message_and_receive_response(self.execution_report)
            execution_report_of_dma_order = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                    JavaApiFields.ExecutionReportBlock.value]
            list_of_execution_ids.append(execution_report_of_dma_order[JavaApiFields.ExecID.value])
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_TER.value},
                execution_report_of_dma_order,
                f'Check expected and actually result from step 6 for {child_order_id} order')
        # endregion

        # region step 7 : Complete order
        self.complete_message.set_default_complete(ord_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_message)
        order_reply_message = self.java_api_manager.get_last_message(
            ORSMessageType.OrdReply.value).get_parameters()[JavaApiFields.OrdReplyBlock.value]
        avg_price = order_reply_message[JavaApiFields.AvgPrice.value]
        self.java_api_manager.compare_values({JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
                                              JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value},
                                             order_reply_message,
                                             'Check expected and actually result from step 7')
        # endregion

        # region step 8 : Check that AvgPrice is correct
        self.allocation_instruction.set_default_book(ord_id)
        gross_trade_amt = float(avg_price) * float(qty)
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {"Qty": qty,
                                                                "AvgPx": avg_price,
                                                                'GrossTradeAmt': str(gross_trade_amt),
                                                                "SettlCurrAmt": str(gross_trade_amt),
                                                                })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.AvgPrice.value: avg_price},
                                             allocation_report, f'Check that {JavaApiFields.AvgPrice.value} is correct')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        os.remove("temp.xml")
        self.ssh_client.close()
        time.sleep(70)
