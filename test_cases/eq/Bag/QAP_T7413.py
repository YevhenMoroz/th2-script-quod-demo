import logging
import os
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
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, OrderBagConst, JavaApiFields, \
    OrdTypes, ExecutionReportConst, OrderReplyConst
from test_framework.java_api_wrappers.ors_messages.ModifyBagOrderRequest import ModifyBagOrderRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn, OrderBookColumns, SecondLevelTabs, \
    ExecSts, WaveColumns
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7413(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.bag_creation_request = OrderBagCreationRequest()
        self.bag_wave_request = OrderBagWaveRequest()
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '200'
        price = '10'
        wave_price = '2'
        account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        qty_of_bag = str(int(qty) * 2)
        orders_id = []
        name_of_bag = 'QAP_T7413'
        # endregion

        # region precondition : Create CO orders
        for i in range(2):
            responses = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            orders_id.append(responses[0].get_parameters()['OrderID'])
        # endregion

        # region step 1, step 2: Created bag
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

        # region step 3, step 4:Wave bag and execute its

        # part 1: create and execute wave
        self.bag_wave_request.set_default(bag_order_id, qty_of_bag, OrdTypes.Limit.value)
        self.bag_wave_request.update_fields_in_component('OrderBagWaveRequestBlock', {
            "Price": wave_price
        })
        self.bag_wave_request.remove_fields_from_component('OrderBagWaveRequestBlock', ['TimeInForce'])
        new_order_single = trade_rule = None
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                account, exec_destination,
                float(wave_price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            account, exec_destination,
                                                                                            float(wave_price), int(qty),
                                                                                            0)
            self.java_api_manager.send_message_and_receive_response(self.bag_wave_request)
        except Exception as e:
            logger.error(f'{e}')
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single)
            self.rule_manager.remove_rule(trade_rule)
        # end of part

        # part 2:Checking wave Status
        order_bag_wave_notification = self.java_api_manager.get_last_message(ORSMessageType. \
                                                                             OrderBagWaveNotification.value). \
            get_parameters()[JavaApiFields.OrderBagWaveNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderWaveStatus.value: OrderBagConst.OrderWaveStatus_TER.value},
            order_bag_wave_notification,
            'Checking that wave has status Terminated (part of step 4)')
        # end of part

        # endregion

        # region step 5 and step 6
        for order_id in orders_id:
            execution_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value, order_id).get_parameters()[
                    JavaApiFields.ExecutionReportBlock.value]
            self.java_api_manager.compare_values({JavaApiFields.ExecPrice.value: str(float(wave_price)),
                                                  JavaApiFields.DisclosedExec.value: 'Y',
                                                  JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
                                                  JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                                 execution_report,
                                                 f'Checking Status, ExecStatus ,'
                                                 f' DiscloseExec and ExecPrice for execution of {orders_id} '
                                                 f'(part of step 4 and step 6)')
        # endregion
