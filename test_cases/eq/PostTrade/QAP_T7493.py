import logging
import os
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import ExecutionReportConst, JavaApiFields, OrderReplyConst, \
    AllocationInstructionConst, SubmitRequestConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7493(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.qty = str(float(200))
        self.price = str(float(10))
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_7_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration2
        client = self.data_set.get_client_by_name('client_pt_1')
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        # endregion

        # region precondition
        # create DMA order (part of precondition)
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'AccountGroupID': client,
            'OrdQty': self.qty,
            'Price': self.price})
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message('Create DMA  order', responses)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        # the end

        # trade DMA order (part of precondition)
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             "InstrumentBlock": self.data_set.get_java_api_instrument(
                                                                 "instrument_2"),
                                                             "Side": SubmitRequestConst.Side_Buy.value,
                                                             "LastTradedQty": self.qty,
                                                             "LastPx": self.price,
                                                             "OrdType": "Limit",
                                                             "Price": self.price,
                                                             "LeavesQty": self.qty,
                                                             "CumQty": self.qty,
                                                             "AvgPrice": self.price,
                                                             "LastMkt": exec_destination,
                                                             "OrdQty": self.qty
                                                         })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message('Trade DMA  order ', responses)
        # the end

        # check PostTrade Status and ExecSts (part of precondition)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                   ExecutionReportConst.ExecType_TRD.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
             JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
            order_reply,
            'Check expected and actually PostTradeStatus and DoneForDay values (part of precondition)')
        # the end
        # endregion

        # region step 1 , step 2 and step 3 step 4 and step 5
        gross_trade_amt = float(self.price) * float(self.qty)
        self.allocation_instruction.set_default_book(order_id)
        currency_for_alloc_instruction = self.data_set.get_currency_by_name('currency_4')
        first_booking_qty = str(float(self.qty) * 0.75)
        second_booking_qty = str(float(self.qty) * 0.25)
        currency = self.data_set.get_currency_by_name('currency_1')
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
            "AccountGroupID": client,
            "GrossTradeAmt": gross_trade_amt,
            'Qty': self.qty,
            'AllocationInstructionQtyList': {'AllocationInstructionQtyBlock': [{
                'BookingQty': first_booking_qty,
                'NetGrossInd': 'G',
                'BookingType': "REG",
                'SettlDate': datetime.utcnow().isoformat(),
                'GrossTradeAmt': str(float(first_booking_qty) * float(self.price)),
                'NetMoney': str(float(first_booking_qty) * float(self.price))},
                {'BookingQty': second_booking_qty,
                 'NetGrossInd': 'G',
                 'BookingType': "REG",
                 'SettlDate': datetime.utcnow().isoformat(),
                 'GrossTradeAmt': str(float(second_booking_qty) * float(self.price)),
                 'NetMoney': str(float(second_booking_qty) * float(self.price))}
            ]},
            'ExecAllocList': {
                'ExecAllocBlock': [{'ExecQty': self.qty,
                                    'ExecID': exec_id,
                                    'ExecPrice': self.price}]},
            "ComputeFeesCommissions": AllocationInstructionConst.ComputeFeesCommissions_Y.value,
            'Currency': currency_for_alloc_instruction,
            'AvgPx': self.price,
            "TradeDate": datetime.utcnow().isoformat(),
            "SettlDate": datetime.utcnow().isoformat(),
            'RootMiscFeesList': {'RootMiscFeesBlock': [{
                'RootMiscFeeType': AllocationInstructionConst.COMM_AMD_FEE_TYPE_REG.value,
                'RootMiscFeeAmt': '5',
                'RootMiscFeeCurr': currency,
                'RootMiscFeeBasis': AllocationInstructionConst.COMM_AND_FEES_BASIS_A.value,
                'RootMiscFeeRate': '5',
                'RootMiscFeeCategory': AllocationInstructionConst.RootMiscFeeCategory_OTH.value}]},
            'ClientCommissionList': {'ClientCommissionBlock': [
                {'CommissionAmountType': AllocationInstructionConst.CommissionAmountType_BRK.value,
                 'CommissionAmount': '5',
                 'CommissionAmountSubType': AllocationInstructionConst.CommissionAmountSubType_OTH.value,
                 'CommissionBasis': AllocationInstructionConst.COMM_AND_FEE_BASIS_ABS.value,
                 'CommissionCurrency': currency,
                 'CommissionRate': '5'}]}
        })

        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message('Split Booking', responses)
        list_of_records = [f"'Qty': '{first_booking_qty}'", f"'Qty': '{second_booking_qty}'"]
        list_of_qty = [first_booking_qty, second_booking_qty]
        for filter in list_of_records:
            allocation_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                                       filter).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
            self.java_api_manager.compare_values({JavaApiFields.Qty.value: list_of_qty[list_of_records.index(filter)],
                                                  JavaApiFields.AvgPrice.value: self.price,
                                                  JavaApiFields.Side.value: SubmitRequestConst.Side_B_aka_Buy.value},
                                                 allocation_report,
                                                 f'Check Qty AvgPx and Side for {list_of_records.index(filter)} block')

        # endregion
