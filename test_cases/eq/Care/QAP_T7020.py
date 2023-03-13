import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    OrderReplyConst,
    JavaApiFields,
    SubmitRequestConst,
)
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7020(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.price = "20"
        self.client = self.data_set.get_client("client_1")  # CLIENT1
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 - Create Care order
        self.submit_request.set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
            external_algo_twap=True,
        )

        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        print_message("CREATE CO", responses)

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                "ExecutionPolicy": "C",
            },
            order_reply,
            "Step 1 - Comparing Status and ExecutionPolicy of Care order",
        )
        self.java_api_manager.compare_values(
            {"AlgoType": "EXT"},
            order_reply["AlgoParametersBlock"],
            "Step 1 - Comparing AlgoType of Care order",
        )
        self.java_api_manager.compare_values(
            {"ScenarioID": "101", "VenueScenarioID": "TWAP"},
            order_reply["ExternalAlgoParametersBlock"],
            "Step 1 - Comparing Algo params of Care order",
        )
        # external_algo_param_block = order_reply["ExternalAlgoParametersBlock"]["ExternalAlgoParameterListBlock"][
        #     "ExternalAlgoParameterBlock"][0]
        # self.java_api_manager.compare_values(
        #     {"AlgoParameterName": "StrategyTag"},
        #     external_algo_param_block,
        #     "Step 1 - Comparing AlgoParameterName of Care order",
        # )
        # endregion

        # region Step 2 - Split Care order
        self.submit_request.set_default_child_dma(ord_id, external_algo_twap=True)
        self.submit_request.update_fields_in_component(
            "NewOrderSingleBlock", {"ExecutionPolicy": "DMA", "RouteList": {"RouteBlock": [{"RouteID": "24"}]}}
        )
        self.submit_request.remove_parameters(["CDOrdAssignInstructionsBlock"])
        self.submit_request.remove_fields_from_component("NewOrderSingleBlock", ["BookingType", "MaxPriceLevels"])
        self.submit_request.get_parameters()["NewOrderSingleBlock"]["ExternalAlgoParametersBlock"].pop(
            "VenueScenarioVersionValue"
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        print_message("Split Care order", responses)
        # endregion

        # Comparing values of Child DMA after Split
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            "OrdReplyBlock"
        ]
        # external_algo_param_block = order_reply["ExternalAlgoParametersBlock"]["ExternalAlgoParameterListBlock"][
        #     "ExternalAlgoParameterBlock"][0]
        # self.java_api_manager.compare_values(
        #     {"AlgoParameterName": "StrategyTag"},
        #     external_algo_param_block,
        #     "Step 2 - Comparing AlgoParameterName of Child DMA after Split",
        # )
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
            order_reply,
            "Step 2 - Comparing Status of Child DMA after Split",
        )
        self.java_api_manager.compare_values(
            {"AlgoType": "EXT"},
            order_reply["AlgoParametersBlock"],
            "Step 2 - Comparing AlgoType of Child DMA after Split",
        )
        self.java_api_manager.compare_values(
            {"ScenarioID": "101", "VenueScenarioID": "TWAP"},
            order_reply["ExternalAlgoParametersBlock"],
            "Step 2 - Comparing Algo params of Child DMA after Split",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
