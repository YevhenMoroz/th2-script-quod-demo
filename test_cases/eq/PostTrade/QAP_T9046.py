import logging
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, ExecutionReportConst, \
    OrderReplyConst, AllocationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.BookingCancelRequest import BookingCancelRequest
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T9046(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '100'
        self.price = '20'
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.order_submit = OrderSubmitOMS(data_set)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.allocation_instruction_2 = AllocationInstructionOMS(self.data_set)
        self.order_modification_request = OrderModificationRequest()
        self.booking_cancel_request = BookingCancelRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create Care order via Java Api
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'TimeInForce': 'GTD',
            "ExpireDate": (datetime.now() + timedelta(days=2)).strftime("%Y%m%d"),
            "ExpireTime": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S"),
            'Price': self.price,
        })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        # endregion

        # region partially_filled CO order (step 2)
        exec_qty = str(int(self.qty) // 2)
        self.trade_entry_request.set_default_trade(order_id, self.price, exec_qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        execution_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report,
            'Checking that order Partially Filled (step 2)')
        exec_id = execution_report[JavaApiFields.ExecID.value]
        # endregion

        # region step 3 : Complete CO order
        self.complete_request.set_default_complete(order_id)
        self.java_api_manager.send_message(self.complete_request)

        self.allocation_instruction.set_default_book(order_id)
        gross_amt = str(float(exec_qty) * float(self.price))
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_1')
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_amt,
                                                                   'AvgPx': self.price,
                                                                   'Qty': exec_qty,
                                                                   'AccountGroupID': self.client,
                                                                   "InstrID": instrument_id,
                                                                   'ExecAllocList': {
                                                                       'ExecAllocBlock': [{'ExecQty': exec_qty,
                                                                                           'ExecID': exec_id,
                                                                                           'ExecPrice': self.price},
                                                                                          ]},
                                                               })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value}, allocation_report,
            'Checking that block created (step 3)')
        # endregion

        # region Setup ORS config step 4
        tree = ET.parse(self.local_path)
        now = datetime.now(timezone.utc) + timedelta(minutes=4)
        schedule_time = now.strftime("%H:%M")
        element = ET.fromstring(
            f"<uncomplete><nonforex><scheduled>true</scheduled><zone>UTC</zone><at>{schedule_time}</at></nonforex></uncomplete>")
        ors = tree.getroot().find("ors")
        ors.append(element)
        tree.write("temp.xml")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(240)
        # endregion

        # region step 5: Fill CO order
        self.trade_entry_request.set_default_trade(order_id, self.price, exec_qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        execution_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report,
            'Checking that order  Filled (step 5)')
        # endregion

        # region step 7 : Complete order again
        self.complete_request.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
             JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
            order_reply, 'Checking that order completed (step 6)')
        # endregion