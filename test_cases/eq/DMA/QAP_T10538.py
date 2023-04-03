import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from custom import basic_custom_actions as bca, basic_custom_actions
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    OrderReplyConst,
    JavaApiFields,
)
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T10538(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "100"
        self.price = "20"
        self.client = self.data_set.get_client("client_1")  # CLIENT1
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.settl_date = (datetime.now()).strftime("%Y-%m-%dT%H:%M")
        self.modification_request = OrderModificationRequest()
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_1_venue_1")  # XPAR_CLIENT1

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 - Create 2 DMA orders
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client_names, self.venue, float(self.price)
            )
            # Create 1st DMA order
            self.order_submit.set_default_dma_limit()
            self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"SettlDate": self.settl_date})
            responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
            print_message("CREATE 1st DMA order", responses)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value
            ]
            ord_id_1st = order_reply["OrdID"]
            cl_ord_id_1st = order_reply["ClOrdID"]
            settl_date_expected = (datetime.now()).strftime("%Y-%m-%dT12:00")
            self.java_api_manager.compare_values(
                {
                    JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                    "SettlDate": settl_date_expected,
                },
                order_reply,
                "Step 1 - Checking Status and SettlDate(today) of 1st DMA order",
            )
            self.java_api_manager.key_is_absent(
                "SettlType", order_reply, "Step 1 - Checking that SettlType is empty for 1st order"
            )

            # Create 2nd DMA order
            self.order_submit.update_fields_in_component(
                "NewOrderSingleBlock", {"ClOrdID": basic_custom_actions.client_orderid(9)}
            )
            responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
            print_message("CREATE 2nd DMA order", responses)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value
            ]
            ord_id_2nd = order_reply["OrdID"]
            cl_ord_id_2nd = order_reply["ClOrdID"]
            self.java_api_manager.compare_values(
                {
                    JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                    "SettlDate": settl_date_expected,
                },
                order_reply,
                "Step 1 - Checking Status and SettlDate(today) of 2nd DMA order",
            )
            self.java_api_manager.key_is_absent(
                "SettlType", order_reply, "Step 1 - Checking that SettlType is empty for 2nd order"
            )
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region Step 2 - Mass Modify SettlType
        try:
            modification_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(
                self.fix_env.buy_side, self.venue_client_names, self.venue, True
            )
            self.__send_modif_request(ord_id_1st, "1st")
            self.__send_modif_request(ord_id_2nd, "2nd")
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(modification_rule)

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    def __send_modif_request(self, ord_id: str, number_of_order: str):
        self.modification_request.set_default(self.data_set, ord_id)
        settl_date_new = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M")
        self.modification_request.update_fields_in_component(
            "OrderModificationRequestBlock", {"SettlDate": settl_date_new, "SettlType": "TP2"}
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.modification_request)
        print_message(f"Mass Modify {number_of_order} order", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        settl_date_expected = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT12:00")
        self.java_api_manager.compare_values(
            {"SettlDate": settl_date_expected, "SettlType": "TP2"},
            order_reply,
            f"Step 2 - Checking that SettlType, SettlDate(today+2) of {number_of_order} order after Mass Modify",
        )
