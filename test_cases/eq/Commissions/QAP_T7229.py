import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    OrderReplyConst,
    JavaApiFields,
    CommissionAmountTypeConst,
    CommissionBasisConst,
)
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7229(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declaration
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.client = self.data_set.get_client_by_name("client_com_1")  # CLIENT_COMM_1
        self.currency = self.data_set.get_currency_by_name("currency_3")  # GBp
        self.comm_currency = self.data_set.get_currency_by_name("currency_2")  # GBP
        self.qty = "100"
        self.price = "20"
        self.abs_amt_gbp = self.data_set.get_comm_profile_by_name("abs_amt_gbp")
        self.commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.order_submit = OrderSubmitOMS(data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        class_name = QAP_T7229
        # region Send commission
        self.commission_sender.clear_commissions()
        self.commission_sender.clear_fees()
        self.commission_sender.set_modify_client_commission_message(
            comm_profile=self.abs_amt_gbp, client=self.client
        ).change_message_params(
            {"accountGroupID": self.client, "venueID": self.data_set.get_venue_by_name("venue_2")}
        ).send_post_request()
        time.sleep(3)
        # endregion

        # region Step 1 - Create DMA order
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "OrdQty": self.qty,
                "AccountGroupID": self.client,
                "Price": self.price,
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
                "SettlCurrency": self.currency,
                "ListingList": {"ListingBlock": [{"ListingID": self.data_set.get_listing_id_by_name("listing_2")}]},
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        class_name.print_message("CREATE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply["OrdID"]
        cl_ord_id = order_reply["ClOrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value, "Currency": self.currency},
            order_reply,
            "Comparing Status and Currency of DMA order",
        )
        # endregion

        # region Step 2 - Trade DMA order and checking commissions
        self.execution_report.set_default_trade(ord_id)
        self.execution_report.update_fields_in_component(
            "ExecutionReportBlock",
            {
                "InstrumentBlock": self.data_set.get_java_api_instrument("instrument_3"),
                "LastMkt": self.data_set.get_mic_by_name("mic_2"),
                "Currency": self.currency,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        class_name.print_message("TRADE", responses)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.CommissionRate.value: "10.0",
                JavaApiFields.CommissionAmount.value: "10.0",
                JavaApiFields.CommissionCurrency.value: self.comm_currency,
                JavaApiFields.CommissionAmountType.value: CommissionAmountTypeConst.CommissionAmountType_BRK.value,
                JavaApiFields.CommissionBasis.value: CommissionBasisConst.CommissionBasis_ABS.value,
            },
            execution_report_message["ClientCommissionList"]["ClientCommissionBlock"][0],
            "Comparing Commissions, that CommissionCurrency=GBP",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
