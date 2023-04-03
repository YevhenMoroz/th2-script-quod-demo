import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import PKSMessageType, ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubscriptionRequestTypes, PosReqTypes, \
    PositionTransferReportConst
from test_framework.java_api_wrappers.oms.ors_messges.PositionTransferInstructionOMS import \
    PositionTransferInstructionOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7591(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.qty_to_transfer = '100.0'
        self.price = '4'
        self.request_for_position = RequestForPositions()
        self.pos_trans = PositionTransferInstructionOMS(data_set)
        self.acc1 = self.data_set.get_account_by_name("client_pos_3_acc_3")  # "PROP"
        self.acc2 = self.data_set.get_account_by_name("client_pos_3_acc_1")  # "Facilitation"
        self._db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: remove position for Facilitation account if it exist
        out = self._db_manager.execute_query(
            f"SELECT * FROM posit WHERE accountid = '{self.acc2}' AND instrid = '{self.instrument_id}'")
        if out != ():
            self._db_manager.execute_query(
                f"DELETE FROM posit WHERE  accountid = '{self.acc2}' AND instrid = '{self.instrument_id}'")
            self._db_manager.execute_query(
                f"DELETE FROM dailyposit WHERE  accountid = '{self.acc2}' AND instrid = '{self.instrument_id}'")
            self.ssh_client.send_command('qrestart all')
            time.sleep(180)
        # endregion

        # region step  1-2 : Extract position for acc1 and acc2
        posit_acc1_before_transfer = self._extract_cum_values_for_acc(self.acc1)
        # endregion

        # region step 3-4 : Perform Position Transfer
        self.pos_trans.set_default_transfer(self.acc1, self.acc2, self.qty_to_transfer, self.price)
        self.pos_trans.update_fields_in_component("PositionTransferInstructionBlock",
                                                  {"InstrID": self.instrument_id})
        self.ja_manager.send_message_and_receive_response(self.pos_trans)

        # endregion

        # region step 5 : Check Position of Destination account:
        out = self._db_manager.execute_query(
            f"SELECT positqty FROM posit WHERE accountid = '{self.acc2}' AND instrid = '{self.instrument_id}'")
        self.ja_manager.compare_values({JavaApiFields.PositQty.value: self.qty_to_transfer},
                                       {JavaApiFields.PositQty.value: str(float(out[0][0]))},
                                       "Verifying that new record of position created and has properly Posit Qty (step 5)")
        # endregion

        # region step 6 : Check Position of Source account:
        self._check_position_transferred_in_amt_and_posit_qty(self.acc1, posit_acc1_before_transfer, False,
                                                              'step 6')
        # endregion

        # region step 7
        position_transfer_report = self.ja_manager.get_last_message(ORSMessageType.PositionTransferReport.value). \
            get_parameters()[JavaApiFields.PositionTransferReportBlock.value]
        self.ja_manager.compare_values(
            {JavaApiFields.TransferTransType.value: PositionTransferReportConst.TransferTransType_NEW.value},
            position_transfer_report,
            'Verify that PositionTransfer created (step 7)')
        # endregion

    def _extract_cum_values_for_acc(self, acc):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              acc)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record

    def _check_position_transferred_in_amt_and_posit_qty(self, account, position_for_account, is_transfer_in,
                                                         step):
        posit_qty_before = position_for_account[JavaApiFields.PositQty.value]
        currently_position = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                                 [JavaApiFields.PositQty.value,
                                                                                  account]).get_parameters() \
            [JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        posit_qty_after = currently_position[JavaApiFields.PositQty.value]
        expected_result = {JavaApiFields.PositQty.value: self.qty_to_transfer}
        values_for_check = [f'Verifying actually and expected results for {step}']
        if is_transfer_in:
            values_for_check.insert(0, {JavaApiFields.PositQty.value:
                                            str(float(posit_qty_after) - float(posit_qty_before))})
        else:
            values_for_check.insert(0, {JavaApiFields.PositQty.value:
                                            str(float(posit_qty_before) - float(posit_qty_after))})
        self.ja_manager.compare_values(expected_result, values_for_check[0], values_for_check[1])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        try:
            self._db_manager.execute_query(
                f"DELETE FROM dailyposit WHERE  accountid = '{self.acc2}' AND instrid = '{self.instrument_id}'")
            self._db_manager.execute_query(
                f"DELETE FROM posit WHERE  accountid = '{self.acc2}' AND instrid = '{self.instrument_id}'")
            self.ssh_client.send_command('qrestart all')
            time.sleep(180)
        finally:
            self._db_manager.close_connection()
