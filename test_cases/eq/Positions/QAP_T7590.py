import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, PositionTransferReportConst, \
    SubscriptionRequestTypes, PosReqTypes
from test_framework.java_api_wrappers.oms.ors_messges.PositionTransferInstructionOMS import \
    PositionTransferInstructionOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.position_calculation_manager import PositionCalculationManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T7590(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pos_3')
        self.source_acc = self.data_set.get_account_by_name('client_pos_3_acc_3')
        self.destination_acc = self.data_set.get_account_by_name('client_pos_3_acc_2')
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.posit_transfer = PositionTransferInstructionOMS(self.data_set)
        self.instrument_id = self.data_set.get_instrument_id_by_name('instrument_1')
        self.request_for_position = RequestForPositions()
        self.qty = '100'
        self.price = '2'
        self.mid_px = '35'
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Create Position Transfer

        # part 1: Get Positions of source and destination account
        source_position_before = self._extract_postion_for_account(self.source_acc)
        destination_position_before = self._extract_postion_for_account(self.destination_acc)
        # end_of_part

        # part 2
        self.posit_transfer.set_default_transfer(self.source_acc, self.destination_acc, self.qty, self.price)
        self.posit_transfer.update_fields_in_component(JavaApiFields.PositionTransferInstructionBlock.value, {
            JavaApiFields.InstrID.value: self.instrument_id})
        self.java_api_manager.send_message_and_receive_response(self.posit_transfer)

        position_transfer_report = self.java_api_manager.get_last_message(ORSMessageType.PositionTransferReport.value). \
            get_parameters()[JavaApiFields.PositionTransferReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransferTransType.value: PositionTransferReportConst.TransferTransType_NEW.value},
            position_transfer_report,
            'Verify that PositionTransfer created (precondition)')
        transfer_id = position_transfer_report[JavaApiFields.PositionTransferID.value]
        source_posit_before_amend = \
            self.java_api_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                      [JavaApiFields.PositQty.value,
                                                                       self.source_acc]).get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]
        destination_position_before_amend = \
            self.java_api_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                      [JavaApiFields.PositQty.value,
                                                                       self.destination_acc]).get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]
        unrealized_pl_source_acc_before = self._get_common_unrealized_pls(self.source_acc)
        unrealized_pl_destination_acc_before = self._get_common_unrealized_pls(self.destination_acc)
        # end_of_part

        # endregion

        # region step 1-3: Amend Position Transfer
        amended_qty_to_transfer = '50'
        self.posit_transfer.set_default_amend_transfer(self.source_acc, self.destination_acc, transfer_id,
                                                       amended_qty_to_transfer,
                                                       self.price)
        self.java_api_manager.send_message_and_receive_response(self.posit_transfer)
        position_transfer_report = self.java_api_manager.get_last_message(ORSMessageType.PositionTransferReport.value). \
            get_parameters()[JavaApiFields.PositionTransferReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.QtyToTransfer.value: str(float(amended_qty_to_transfer))},
                                             position_transfer_report,
                                             'Verify that position transfer amended (step 3)')
        # endregion

        # region step 4: Check that PositQty of source account increased
        source_posit_after_amend = \
            self.java_api_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                      [JavaApiFields.PositQty.value,
                                                                       self.source_acc]).get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]
        source_posit_qty_after_amend = source_posit_after_amend[JavaApiFields.PositQty.value]
        expected_increased_qty = str(float(source_posit_qty_after_amend) -
                                     float(source_posit_before_amend[JavaApiFields.PositQty.value]))
        self.java_api_manager.compare_values({'IncreasedQty': str(float(amended_qty_to_transfer))},
                                             {'IncreasedQty': expected_increased_qty},
                                             f'Verify that for {self.source_acc} {JavaApiFields.PositQty.value} increased on {amended_qty_to_transfer} (step 4)')
        # endregion

        # region step 5 Check that unrealized_pl_common and unrealized_pl changes properly
        net_weighted_avg_px_source_acc_before = source_position_before[JavaApiFields.NetWeightedAvgPx.value]
        posit_qty_source_before_transfer = source_position_before[JavaApiFields.PositQty.value]
        calculated_net_weighted_avg_px = PositionCalculationManager.calculate_net_weighted_avg_px_for_position_transfer_source_acc(
            posit_qty_source_before_transfer, amended_qty_to_transfer, net_weighted_avg_px_source_acc_before, self.price)
        unrealized_pl_specify_expected = str(float(source_posit_qty_after_amend) * (float(self.mid_px) - float(calculated_net_weighted_avg_px)))
        unrealized_pls_actual_source_acc_after = self._get_common_unrealized_pls(self.source_acc)
        unrealized_pl_common_expected = str(float(unrealized_pl_source_acc_before[0]) - float(unrealized_pl_source_acc_before[1])+ float(unrealized_pl_specify_expected))
        self.java_api_manager.compare_values({JavaApiFields.UnrealizedPL.value: unrealized_pl_specify_expected},
                                             {JavaApiFields.UnrealizedPL.value: unrealized_pls_actual_source_acc_after[1]},
                                             f'Verify that Unrealized PL of {self.source_acc} has properly value (step 5)')
        self.java_api_manager.compare_values({JavaApiFields.UnrealizedPL.value: unrealized_pl_common_expected},
                                             {JavaApiFields.UnrealizedPL.value: unrealized_pls_actual_source_acc_after[0]},
                                             f'Verify that Total Unrealized PL of {self.source_acc} has properly value (step 5)')
        # endregion

        # region step 6: Verify that PositQty of destination account decreased
        destination_posit_after_amend = \
            self.java_api_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                      [JavaApiFields.PositQty.value,
                                                                       self.destination_acc]).get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]
        destination_posit_qty_after_amend = destination_posit_after_amend[JavaApiFields.PositQty.value]
        expected_decreased_qty = str(float(destination_position_before_amend[JavaApiFields.PositQty.value]) -
                                     float(destination_posit_qty_after_amend))
        self.java_api_manager.compare_values({'DecreasedQty': str(float(amended_qty_to_transfer))},
                                             {'DecreasedQty': expected_decreased_qty},
                                             f'Verify that for {self.destination_acc} {JavaApiFields.PositQty.value} decreased on {amended_qty_to_transfer} (step 6)')
        net_weighted_avg_px_destination_acc_before = destination_position_before[JavaApiFields.NetWeightedAvgPx.value]

        posit_qty_destination_before_transfer = destination_position_before[JavaApiFields.PositQty.value]
        expected_net_weighted_avg_px_destination = PositionCalculationManager.calculate_net_weighted_avg_px_for_position_transfer_destination_acc(posit_qty_destination_before_transfer, amended_qty_to_transfer, net_weighted_avg_px_destination_acc_before, self.price)
        self.java_api_manager.compare_values({JavaApiFields.NetWeightedAvgPx.value: expected_net_weighted_avg_px_destination},
                                             destination_posit_after_amend, f'Verify that for {self.destination_acc}, {JavaApiFields.NetWeightedAvgPx.value} calculated properly (step 6)')

        # endregion

        # region step 7: Calculate UnrealizedPl(common and for instrument) for destination account
        unrealized_pl_specify_expected = str(
            float(destination_posit_qty_after_amend) * (float(self.mid_px) - float(expected_net_weighted_avg_px_destination)))
        unrealized_pls_actual_destination_acc_after = self._get_common_unrealized_pls(self.destination_acc)
        unrealized_pl_common_expected = str(
            float(unrealized_pl_destination_acc_before[0]) - float(unrealized_pl_destination_acc_before[1]) + float(
                unrealized_pl_specify_expected))
        self.java_api_manager.compare_values({JavaApiFields.UnrealizedPL.value: unrealized_pl_specify_expected},
                                             {JavaApiFields.UnrealizedPL.value: unrealized_pls_actual_destination_acc_after[
                                                 1]},
                                             f'Verify that Unrealized PL of {self.destination_acc} has properly value (step 7)')
        self.java_api_manager.compare_values({JavaApiFields.UnrealizedPL.value: unrealized_pl_common_expected},
                                             {JavaApiFields.UnrealizedPL.value: unrealized_pls_actual_destination_acc_after[
                                                 0]},
                                             f'Verify that Total Unrealized PL of {self.destination_acc} has properly value (step 7)')
        # endregion

    def _extract_postion_for_account(self, account):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              account)
        self.java_api_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.java_api_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record

    def _get_common_unrealized_pls(self, account):
        report = self.java_api_manager.get_last_message(PKSMessageType.PositionReport.value, account). \
            get_parameters()[JavaApiFields.PositionReportBlock.value]
        unrealized_pl_common = report[JavaApiFields.SecurityAccountPLBlock.value][JavaApiFields.UnrealizedPL.value]
        unrealized_pl_specify = None
        for message in report[JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]:
            if self.instrument_id == message[JavaApiFields.InstrID.value]:
                unrealized_pl_specify = message[JavaApiFields.UnrealizedPL.value]
        return unrealized_pl_common, unrealized_pl_specify
