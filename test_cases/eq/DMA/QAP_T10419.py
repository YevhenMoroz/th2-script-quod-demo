import logging
import time
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrdTypes, \
    OrderReplyConst

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T10419(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.new_ord_single = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_manager_sell = FixManager(self.fix_env.sell_side, self.test_id)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.rule_manager = RuleManager(Simulators.equity)
        self.execution_report_fix = FixMessageExecutionReportOMS(self.data_set)
        self.modify_message_fix = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        self.fix_verifier_buy_side = FixVerifier(self.fix_env.buy_side, self.test_id)
        self.fix_manager_buy = FixManager(self.fix_env.buy_side, self.test_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Create DMA order via FIX
        # part 1: Send NewOrderSingle
        self.new_ord_single.set_default_dma_limit()
        price = self.new_ord_single.get_parameters()['Price']
        cl_ord_id = self.new_ord_single.get_parameters()['ClOrdID']

        self.new_ord_single.change_parameters({'StopPx': price})
        qty = self.new_ord_single.get_parameters()['OrderQtyData']['OrderQty']
        self.fix_manager_sell.send_message_fix_standard(self.new_ord_single)
        time.sleep(2)
        order_id = self._received_and_check_value(cl_ord_id, OrderReplyConst.ExecType_PDO.value, 'step 1', price)
        # end_of_part

        # part 2: Check 35=D message at BuySideGateway
        list_ignored_fields = ['Account', 'TransactTime', 'Parties', 'SettlDate', 'Instrument']
        new_order_single_buy_side = deepcopy(self.new_ord_single)
        new_order_single_buy_side.change_parameters({'ClOrdID': order_id})
        self.fix_verifier_buy_side.check_fix_message_fix_standard(new_order_single_buy_side, ['ClOrdID'],
                                                                  ignored_fields=list_ignored_fields)
        # end_of_part
        # endregion

        # region step 2: Send 35=8(39=2 message)
        self.execution_report_fix.set_default_new(self.new_ord_single)
        zero_value = '0.0'
        self.execution_report_fix.remove_parameters(['Parties', "QtyType"])
        self.execution_report_fix.change_parameters({
            "Account": self.venue_client_name,
            "HandlInst": "1",
            "Side": "1",
            'Instrument': self.data_set.get_fix_instrument_by_name('instrument_1'),
            'OrderQtyData': {'OrderQty': qty},
            "TimeInForce": "0",
            "ClOrdID": order_id,
            "OrdType": "2",
            "Price": price,
            "ExecType": "0",
            "OrdStatus": "0",
            "OrderID": order_id,
            "ExecID": '2',
            "LastQty": zero_value,
            "TransactTime": datetime.utcnow().isoformat(),
            "AvgPx": zero_value,
            "LeavesQty": qty,
            "CumQty": zero_value,
            'StopPx': price,
            "LastPx": zero_value,
        })
        self.fix_manager_buy.send_message_fix_standard(self.execution_report_fix)
        time.sleep(2)
        self._received_and_check_value(cl_ord_id, OrderReplyConst.ExecType_OPN.value, 'step 2', price)
        # endregion

        # region step 3: send and check 35=G message
        self.modify_message_fix.set_default(self.new_ord_single)
        new_stop_price = str(float(price) - 1)
        self.modify_message_fix.change_parameters({'StopPx': new_stop_price})
        self.fix_manager_sell.send_message_fix_standard(self.modify_message_fix)
        list_ignored_fields.extend(['ClOrdID', 'OrderCapacity', 'OrderID', 'SettlType',
                                    'StopPx', 'Currency', 'ExDestination'])
        self.modify_message_fix.change_parameters({'OrigClOrdID': order_id})
        self.fix_verifier_buy_side.check_fix_message_fix_standard(self.modify_message_fix,
                                                                  ignored_fields=list_ignored_fields)
        # endregion

    def _received_and_check_value(self, cl_ord_id, ord_type, step, price):
        tuple_of_values = \
            self.db_manager.execute_query(
                f"SELECT ordid, ordtype, price, stopprice FROM ordr WHERE clordid='{cl_ord_id}'")[0]
        self.fix_manager_sell.compare_values({JavaApiFields.OrdType.value: OrdTypes.Limit.value,
                                              JavaApiFields.StopPrice.value: float(price),
                                              JavaApiFields.Price.value: float(price)},
                                             {JavaApiFields.OrdType.value: tuple_of_values[1],
                                              JavaApiFields.StopPrice.value: float(tuple_of_values[2]),
                                              JavaApiFields.Price.value: float(tuple_of_values[3])},
                                             f'Verify that order has properly values ({step})')
        exec_type = \
            self.db_manager.execute_query(
                f"SELECT exectype FROM ordreply WHERE transid='{tuple_of_values[0]}' AND exectype='{ord_type}'")[0][0]
        self.fix_manager_sell.compare_values({JavaApiFields.ExecType.value: ord_type}, {
            JavaApiFields.ExecType.value: exec_type}, f'Verifying status of order ({step})')
        return tuple_of_values[0]
