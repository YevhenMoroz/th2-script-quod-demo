import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, PosReqTypes, \
    SubscriptionRequestTypes, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiWashBookRuleMessages import RestApiWashBookRuleMessages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7606(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value)
        self.child_order = OrderSubmitOMS(data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pos_1_venue_1')
        self.wash_book_acc = self.data_set.get_washbook_account_by_name('washbook_account_2')
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.rest_wash_book_message = RestApiWashBookRuleMessages(self.data_set)
        self.request_for_position = RequestForPositions()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # precondition: set up WashBookRule
        self.rest_wash_book_message.enable_care_wash_book_rule()
        self.rest_api_manager.send_post_request(self.rest_wash_book_message)
        # endregion

        # region step 1: create Care Order
        self.order_submit.update_fields_in_component("NewOrderSingleBlock",
                                                     {'AccountGroupID': self.data_set.get_client_by_name(
                                                         "client_pos_1"), "Side": "Sell"})
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]
        ord_id = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            "OrdNotificationBlock"]["OrdID"]

        # region step 3: get position for Security Account CareWB
        position_before_trans_for_acc_prop = self._extract_cum_values_for_acc()
        posit_qty_before_trade = position_before_trans_for_acc_prop[JavaApiFields.PositQty.value]
        cum_sell_qty_before_trade = position_before_trans_for_acc_prop[JavaApiFields.CumSellQty.value]
        # endregion

        # region step 4: create and fill child order
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
        # endregion

        # region step 5: get position for Security Account CareWB after trade
        position_after_trans_for_acc_prop = self._extract_cum_values_for_acc()
        posit_qty_after_trade = position_after_trans_for_acc_prop[JavaApiFields.PositQty.value]
        cum_sell_qty_after_trade = position_after_trans_for_acc_prop[JavaApiFields.CumSellQty.value]
        increment_cum_sell_qty = str(abs(float(cum_sell_qty_after_trade) - float(
            cum_sell_qty_before_trade)))
        decrement_posit_qty = str(abs(float(posit_qty_before_trade) - float(
            posit_qty_after_trade)))
        self.ja_manager.compare_values(
            {f'Decrement{JavaApiFields.PositQty.value}': str(float(qty)),
             f'Increment{JavaApiFields.CumSellQty.value}': str(float(qty))},
            {f'Decrement{JavaApiFields.PositQty.value}': decrement_posit_qty,
             f'Increment{JavaApiFields.CumSellQty.value}': increment_cum_sell_qty},
            f'Verifying that {JavaApiFields.PositQty.value} decreased on {qty} and {JavaApiFields.CumSellQty.value} increased on {qty} (step 5)')
        # endregion

    def _extract_cum_values_for_acc(self):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              self.wash_book_acc)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record
