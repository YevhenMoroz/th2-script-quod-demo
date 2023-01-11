import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiSettlementModelMessages import RestApiSettlementModelMessages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T8339(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '7777'
        self.price = '10'
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.venue = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_pt_1')
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(self.wa_connectivity, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.api_message = RestApiSettlementModelMessages(self.data_set)
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.pset = self.data_set.get_pset('pset_by_id_1')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create DMA order (step 1)
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
             'InstrID': self.instrument_id,
             "OrdQty": self.qty,
             "AccountGroupID": self.client,
             "Price": self.price})
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("Create Dma order", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply["OrdID"]
        # endregion

        # region trade DMA order (step 2)
        self.execution_report.set_default_trade(ord_id)
        self.execution_report.update_fields_in_component(
            "ExecutionReportBlock",
            {
                "Price": self.price,
                "AvgPrice": self.price,
                "LastPx": self.price,
                "OrdQty": self.qty,
                "LastTradedQty": self.qty,
                "CumQty": self.qty,
                "InstrumentBlock": self.data_set.get_java_api_instrument("instrument_2")
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message("Trade Dma order", responses)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, ExecutionReportConst.ExecType_TRD.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value, },
            execution_report_message,
            "Comparing ExecSts after Execute DMA (part of precondition)",
        )
        exec_id = execution_report_message[JavaApiFields.ExecID.value]
        # endregion

        # region book CO order (step 3)
        gross_trade_amt = float(self.qty) * float(self.price)
        self.allocation_instruction.set_default_book(ord_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
            "Qty": self.qty,
            "AvgPx": self.price,
            'GrossTradeAmt': str(gross_trade_amt),
            "InstrID": self.instrument_id,
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("Book order", responses)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.SettlLocationID.value: self.pset[1],
                                              JavaApiFields.SettlementModelID.value: self.pset[0]},
                                             allocation_report, 'Check PSET and PSET BIC (step 3 )')
        # endregion
