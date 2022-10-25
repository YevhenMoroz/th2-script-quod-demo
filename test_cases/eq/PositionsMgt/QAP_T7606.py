import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7606(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            self.data_set.get_recipient_by_name("recipient_user_1"), "1")
        self.child_order = OrderSubmitOMS(data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pos_1_venue_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.order_submit.update_fields_in_component("NewOrderSingleBlock",
                                                     {'AccountGroupID': self.data_set.get_client_by_name(
                                                         "client_pos_1"), "Side": "Sell"})
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]
        posit_qty = \
            self.ja_manager.get_last_message(ORSMessageType.PositionReport.value).get_parameter("PositionReportBlock")[
                "PositionList"]["PositionBlock"][0]["PositQty"]
        cum_sell_qty = \
            self.ja_manager.get_last_message(ORSMessageType.PositionReport.value).get_parameter("PositionReportBlock")[
                "PositionList"]["PositionBlock"][0]["CumSellQty"]
        ord_id = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            "OrdNotificationBlock"]["OrdID"]
        self.child_order.set_default_child_dma(ord_id)
        self.child_order.update_fields_in_component("NewOrderSingleBlock",
                                                    {'AccountGroupID': self.data_set.get_client_by_name(
                                                        "client_pos_1"), "Side": "Sell"})
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(
                self.fix_env.buy_side,
                self.client_for_rule,
                self.exec_destination,
                float(price),
                int(qty), 1)
            self.ja_manager.send_message_and_receive_response(self.child_order)
        except Exception as e:
            logger.info(f'Your Exception is {e}')
        # endregion
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(new_order_single_rule)

        posit_qty2 = \
            self.ja_manager.get_last_message(ORSMessageType.PositionReport.value).get_parameter("PositionReportBlock")[
                "PositionList"]["PositionBlock"][0]["PositQty"]
        cum_sell_qty2 = \
            self.ja_manager.get_last_message(ORSMessageType.PositionReport.value).get_parameter("PositionReportBlock")[
                "PositionList"]["PositionBlock"][0]["CumSellQty"]
        self.ja_manager.compare_values(
            {"PositQty": str(float(posit_qty) - float(qty)), "CumSellQty": str(float(cum_sell_qty) + float(qty))},
            {"PositQty": posit_qty2, "CumSellQty": cum_sell_qty2}, "compare posit")
