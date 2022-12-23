import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7436(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_1")
        self.price = self.fix_message.get_parameter("Price")
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.client = self.data_set.get_client_by_name('client_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.bs_connectivity = self.fix_env.buy_side
        self.new_currency = self.data_set.get_currency_by_name("currency_4")
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.mod_req = OrderModificationRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_name,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(5)
            self.rule_manager.remove_rule(nos_rule)
        ord_id = response[0].get_parameter("OrderID")
        exec_rep = self.fix_manager.get_last_message("ExecutionReport").get_parameters()
        self.fix_manager.compare_values({"Currency": self.fix_message.get_parameter("Currency")}, exec_rep,
                                        "Check instrument Currency")
        # endregion
        # region Step 2 - Change client of order
        self.mod_req.set_default(self.data_set, ord_id)
        self.mod_req.update_fields_in_component(
            "OrderModificationRequestBlock", {"BookingType": "TotalReturnSwap", "CounterpartList": {
                "CounterpartBlock": [{"PartyRole": "GIV", "CounterpartID": "200005"}]}}
        )
        try:
            rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.bs_connectivity,
                                                                               self.venue_client_name, self.mic)
            response = self.java_api_manager.send_message_and_receive_response(self.mod_req)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(5)
            self.rule_manager.remove_rule(rule)

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values({"BookingType": "TRS"}, order_reply, "Check new BookingType")
        self.java_api_manager.compare_values({"PartyRole": "GIV", "CounterpartID": "200005"},
                                        order_reply["CounterpartList"]["CounterpartBlock"][0], "Check new Counterpart")
        # endregion
