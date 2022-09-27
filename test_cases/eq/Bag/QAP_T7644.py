import logging
import os
import time
from pathlib import Path

from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn, OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7644(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.bag_order_book = OMSBagOrderBook(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.act_java_api = Stubs.act_java_api

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1092'
        price = '10'
        client_name = self.data_set.get_client_by_name('client_pt_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', client_name)
        client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.fix_message.change_parameter("HandlInst", '3')
        qty_of_bag = str(int(int(qty) * 2))
        orders_id = []
        name_of_bag = 'QAP_T7644'
        inbox_filter = {'ClientName': client_name}
        new_order_single_rule = trade_rule = None
        # endregion

        # region create 2 CO order
        for i in range(2):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(lookup, qty, price,
                                           filter=inbox_filter)
            self.order_book.set_filter([OrderBookColumns.qty.value, qty])
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))
        # endregion

        # region create Bag and extract values from it
        self.bag_order_book.create_bag_details([1, 2], name_of_bag=name_of_bag, price=price)
        self.bag_order_book.create_bag()
        self.__extracting_and_comparing_value_for_bag_order([OrderBagColumn.order_bag_qty.value,
                                                             OrderBagColumn.ord_bag_name.value,
                                                             OrderBagColumn.unmatched_qty.value,
                                                             OrderBagColumn.leaves_qty.value,
                                                             ],
                                                            [
                                                                qty_of_bag,
                                                                name_of_bag,
                                                                qty_of_bag,
                                                                qty_of_bag
                                                            ], False, 'creation',
                                                            )

        # endregion

        # region partially fill bag order via wave
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                client_for_rule,
                exec_destination,
                float(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            client_for_rule,
                                                                                            exec_destination,
                                                                                            float(price),
                                                                                            int(qty), delay=0)
            self.bag_order_book.set_order_bag_wave_details(tif=self.data_set.get_time_in_force('time_in_force_1'),
                                                           price=price,
                                                           qty=qty)
            self.bag_order_book.wave_bag()
        except Exception as e:
            logger.info(f'Your Exception is {e}')

        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single_rule)
            self.rule_manager.remove_rule(trade_rule)
    #     # endregion

        # region complete bag_order
        complete_bag_message = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'DFDManagementBatchBlock': {
                'DFDOrderList': {'DFDOrderBlock': [{'OrdID': orders_id[0]},
                                                        {'OrdID': orders_id[1]}]
                                 },
                'SetDoneForDay': 'Y'
            }
        }
        self.act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
            message=bca.message_to_grpc_fix_standard('Order_DFDManagementBatch',
                                                     complete_bag_message, self.java_api),
            parent_event_id=self.test_id))
        # endregion

        # extracting and comparing values after complete
        self.__extracting_and_comparing_value_for_bag_order([OrderBagColumn.order_bag_qty.value,
                                                             OrderBagColumn.ord_bag_name.value,
                                                             OrderBagColumn.unmatched_qty.value,
                                                             OrderBagColumn.leaves_qty.value
                                                             ], [
                                                                qty_of_bag,
                                                                name_of_bag,
                                                                qty,
                                                                0
                                                            ],
                                                            False, ' complete',
                                                            )
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def __extracting_and_comparing_value_for_bag_order(self, bag_column_extraction: list, expected_values: list,
                                                       return_order_bag_id: bool, action: str):
        fields = self.bag_order_book.extract_order_bag_book_details('1', bag_column_extraction)
        expected_values_bag = dict()
        order_bag_id = None
        if return_order_bag_id:
            order_bag_id = fields.pop('order_bag.' + OrderBagColumn.id.value)
            bag_column_extraction.remove(OrderBagColumn.id.value)
        for count in range(len(bag_column_extraction)):
            expected_values_bag.update({'order_bag.' + bag_column_extraction[count]: expected_values[count]})
        self.bag_order_book.compare_values(expected_values_bag,
                                           fields, f'Compare values from bag_book after {action}')
        if return_order_bag_id:
            return order_bag_id
