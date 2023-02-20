import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import OrderReplyConst, JavaApiFields, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7368(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.price = "20"
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.alloc_account_1 = self.data_set.get_account_by_name("client_pt_1_acc_1")  # MOClient_SA1
        self.alloc_account_2 = self.data_set.get_account_by_name("client_pt_1_acc_2")  # MOClient_SA2
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1- Create Care order with allocation accounts
        self.submit_request.set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.submit_request.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "OrdQty": self.qty,
                "AccountGroupID": self.client,
                "Price": self.price,
                "PreTradeAllocationBlock": {
                    "PreTradeAllocationList": {
                        "PreTradeAllocAccountBlock": [
                            {"AllocAccountID": self.alloc_account_1, "AllocQty": str(int(self.qty) // 2)},
                            {"AllocAccountID": self.alloc_account_2, "AllocQty": str(int(self.qty) // 2)},
                        ]
                    }
                },
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        print_message("CREATE CO", responses)

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Comparing Status of Care order",
        )
        alloc_account_block = order_reply["PreTradeAllocationBlock"]["PreTradeAllocationList"][
            "PreTradeAllocAccountBlock"
        ]
        self.__compare_alloc_accounts(alloc_account_block, str(float(self.qty) / 2), "1")
        # endregion

        # region Step 2 - Splitting Care order and checking allocation accounts for a child order
        self.submit_request.set_default_child_dma(ord_id)
        self.submit_request.update_fields_in_component("NewOrderSingleBlock", {"ExecutionPolicy": "DMA"})
        self.submit_request.remove_parameters(["CDOrdAssignInstructionsBlock"])
        self.submit_request.remove_fields_from_component("NewOrderSingleBlock", ["BookingType"])
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        print_message("Split Care order", responses)
        # endregion

        # Comparing values of Child DMA after Split
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            "OrdReplyBlock"
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
            order_reply,
            "Step 2 - Comparing Status of Child DMA after Split",
        )

        alloc_account_block = order_reply["PreTradeAllocationBlock"]["PreTradeAllocationList"][
            "PreTradeAllocAccountBlock"
        ]
        self.__compare_alloc_accounts(alloc_account_block, str(float(self.qty) / 2), "2")
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    def __compare_alloc_accounts(self, alloc_account_block, alloc_qty: str, step_number: str):
        if self.alloc_account_1 in alloc_account_block[0].values():
            self.java_api_manager.compare_values(
                {"AllocAccountID": self.alloc_account_1, "AllocQty": alloc_qty},
                alloc_account_block[0],
                f"Step {step_number} - Checking first allocation account",
            )
            self.java_api_manager.compare_values(
                {"AllocAccountID": self.alloc_account_2, "AllocQty": alloc_qty},
                alloc_account_block[1],
                f"Step {step_number} - Checking second allocation account",
            )
        else:
            self.java_api_manager.compare_values(
                {"AllocAccountID": self.alloc_account_1, "AllocQty": alloc_qty},
                alloc_account_block[1],
                f"Step {step_number} - Checking first allocation account",
            )
            self.java_api_manager.compare_values(
                {"AllocAccountID": self.alloc_account_2, "AllocQty": alloc_qty},
                alloc_account_block[0],
                f"Step {step_number} - Checking second allocation account",
            )
