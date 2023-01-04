import logging
import os
import time
from datetime import timedelta, date
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import TimeInForces, JavaApiFields, OrderReplyConst, \
    SubmitRequestConst, BagChildCreationPolicy, OrdTypes, OrderBagConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T6931(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.order_submit = OrderSubmitOMS(data_set)
        self.bag_creation_request = OrderBagCreationRequest()
        self.bag_wave_request = OrderBagWaveRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '100'
        qty_of_bag = str(int(int(qty) * 2))
        price = '10'
        client = self.data_set.get_client_by_name('client_pt_1')
        venue_client_account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        rule_manager = RuleManager(Simulators.equity)
        orders_id = []
        name_of_bag = 'QAP_T6931'
        expire_data = str(date.today() + timedelta(days=1)).replace('-', '')
        # endregion

        # region step 1 : Create CO
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": qty,
             "AccountGroupID": client,
             "Price": price})
        for counter in range(2):
            if counter == 1:
                self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                             {
                                                                 'TimeInForce': TimeInForces.GTD.value,
                                                                 'ExpireDate': expire_data,
                                                                 "ClOrdID": bca.client_orderid(9)
                                                             })
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            orders_id.append(order_reply[JavaApiFields.OrdID.value])
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply,
                f'Checking expected and actually results for {orders_id[counter]} (step 1)')
        # endregion

        # region step 2: Create Bag
        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, name_of_bag, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagName.value: name_of_bag,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, order_bag_notification,
                                             'Checking expected and actually results (step 2)')
        # endregion

        # region step 3: Wave Bag

        # part 1: create wave
        self.bag_wave_request.set_default(bag_order_id, qty_of_bag, OrdTypes.Limit.value)
        self.bag_wave_request.update_fields_in_component('OrderBagWaveRequestBlock', {
            "Price": price
        })
        self.bag_wave_request.remove_fields_from_component('OrderBagWaveRequestBlock', ['TimeInForce'])
        new_order_single = None
        try:
            new_order_single = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                venue_client_account, exec_destination,
                float(price))
            self.java_api_manager.send_message_and_receive_response(self.bag_wave_request)
        except Exception as e:
            logger.error(f'{e}')
        finally:
            time.sleep(3)
            rule_manager.remove_rule(new_order_single)
        # end of part

        # part 2 : get child`s OrderIDs
        child_order_ids = []
        for parent_order in orders_id:
            order_notification = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value,
                                                                        parent_order).get_parameters()[
                JavaApiFields.OrderNotificationBlock.value]
            child_order_ids.append(order_notification[JavaApiFields.OrdID.value])
        # end of part

        # part step 3 : checking results
        for child_order_id in child_order_ids:
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value, child_order_id). \
                get_parameters()[JavaApiFields.OrdReplyBlock.value]

            if child_order_ids.index(child_order_id) == 1:
                self.java_api_manager.compare_values({JavaApiFields.TimeInForce.value: TimeInForces.GTD.value,
                                                      JavaApiFields.ExpireDate.value: expire_data},
                                                     order_reply,
                                                     f'Checking expected and actually result for {child_order_id} (step 3)')
            else:
                self.java_api_manager.compare_values({JavaApiFields.TimeInForce.value: TimeInForces.DAY.value},
                                                     order_reply,
                                                     f'Checking expected and actually result for {child_order_id} (step 3)')
        # end of part

        # endregion
