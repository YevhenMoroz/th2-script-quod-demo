import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.BookingCancelRequest import BookingCancelRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7190(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = '100'
        self.price_first = '19'
        self.price_second = '19.2'
        self.price_third = '18.89'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.un_book_orders = BookingCancelRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition : Create DMA orders
        list_of_prices = [self.price_first, self.price_second, self.price_third]
        list_of_orders_ids = []
        for price in list_of_prices:
            self.order_submit.set_default_dma_limit()
            self.order_submit.update_fields_in_component(
                "NewOrderSingleBlock",
                {"OrdQty": self.qty,
                 "AccountGroupID": self.client,
                 "Price": price,
                 "ClOrdID": bca.client_orderid(9)})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value
            ]
            list_of_orders_ids.append(order_reply[JavaApiFields.OrdID.value])
        # endregion

        # region step 1 , step 2 and step 4 : Fully Filled DMA orders
        average_price_for_first_block = str((float(self.price_first) + float(self.price_third)) / 2)
        list_of_exec_id = []
        for order_id in list_of_orders_ids:
            price = list_of_prices[list_of_orders_ids.index(order_id)]
            self.execution_report.set_default_trade(order_id)
            self.execution_report.update_fields_in_component(
                "ExecutionReportBlock",
                {
                    "Price": price,
                    "AvgPrice": price,
                    "LastPx": price,
                    "OrdQty": self.qty,
                    "LastTradedQty": self.qty,
                    "CumQty": self.qty,
                },
            )
            self.java_api_manager.send_message_and_receive_response(self.execution_report)
            execution_report_message = self.java_api_manager.get_last_message(
                ORSMessageType.ExecutionReport.value, ExecutionReportConst.ExecType_TRD.value
            ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            list_of_exec_id.append(execution_report_message[JavaApiFields.ExecID.value])
            self.java_api_manager.compare_values({JavaApiFields.TransExecStatus.value:
                                                      ExecutionReportConst.TransExecStatus_FIL.value},
                                                 execution_report_message,
                                                 f'Checking expected and actually results for {order_id} '
                                                 f'(ExecSts)')
            self.java_api_manager.compare_values({JavaApiFields.PostTradeStatus.value:
                                                      OrderReplyConst.PostTradeStatus_RDY.value},
                                                 order_reply,
                                                 f'Checking expected and actually results for {order_id} '
                                                 '(PostTradeStatus)')
        # endregion

        # region step 2 : Allocate first and third order
        orders_id_block = []
        orders_id_block.append({JavaApiFields.OrdID.value: list_of_orders_ids[0]})
        orders_id_block.append({JavaApiFields.OrdID.value: list_of_orders_ids[2]})
        filter_map = {list_of_orders_ids[0]: list_of_orders_ids[0],
                      list_of_orders_ids[2]: list_of_orders_ids[2]}
        self.allocation_instruction.set_default_book(list_of_orders_ids[1])
        self.allocation_instruction.update_fields_in_component("AllocationInstructionBlock",
                                                               {'Qty': str(float(self.qty) * 2),
                                                                'AvgPx': '11',
                                                                'AccountGroupID': self.client,
                                                                'ExecAllocList': {
                                                                    'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                        'ExecID': list_of_exec_id[0],
                                                                                        'ExecPrice': list_of_prices[0]},
                                                                                       {'ExecQty': self.qty,
                                                                                        'ExecID': list_of_exec_id[2],
                                                                                        'ExecPrice': list_of_prices[2]}
                                                                                       ]},
                                                                "OrdAllocList": {"OrdAllocBlock": orders_id_block}
                                                                })
        self.allocation_instruction.remove_fields_from_component('AllocationInstructionBlock', ['AvgPx'])
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction, filter_map)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                   JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.AvgPrice.value: average_price_for_first_block},
                                             allocation_report,
                                             'Checking actually and  expected results for step 2')
        allocation_instruction = allocation_report[JavaApiFields.ClBookingRefID.value]
        # endregion

        # region step 3: Unbook orders:
        self.un_book_orders.set_default(allocation_instruction)
        self.java_api_manager.send_message_and_receive_response(self.un_book_orders)
        for order_id in orders_id_block:
            order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value,
                                                                  order_id[JavaApiFields.OrdID.value]).get_parameters()[
                JavaApiFields.OrdUpdateBlock.value]
            self.java_api_manager.compare_values({JavaApiFields.PostTradeStatus.value:
                                                      OrderReplyConst.PostTradeStatus_RDY.value,
                                                  JavaApiFields.DoneForDay.value:
                                                      OrderReplyConst.DoneForDay_YES.value},
                                                 order_update,
                                                 f'Checking expected and actually results for {order_id[JavaApiFields.OrdID.value]} (step 3)')
        # endregion

        # region step 5 :
        average_price_for_first_block = str((float(self.price_first) + float(self.price_second) + float(
            self.price_third)) / 3)
        orders_id_block.append({JavaApiFields.OrdID.value: list_of_orders_ids[1]})
        self.allocation_instruction.update_fields_in_component("AllocationInstructionBlock",
                                                               {'Qty': str(float(self.qty) * 3),
                                                                'AccountGroupID': self.client,
                                                                'ExecAllocList': {
                                                                    'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                        'ExecID': list_of_exec_id[0],
                                                                                        'ExecPrice': list_of_prices[0]},
                                                                                       {'ExecQty': self.qty,
                                                                                        'ExecID': list_of_exec_id[2],
                                                                                        'ExecPrice': list_of_prices[2]},
                                                                                       {'ExecQty': self.qty,
                                                                                        'ExecID': list_of_exec_id[1],
                                                                                        'ExecPrice': list_of_prices[1]}
                                                                                       ]},
                                                                "OrdAllocList": {"OrdAllocBlock": orders_id_block}
                                                                })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.AvgPrice.value: average_price_for_first_block},
                                             allocation_report,
                                             'Checking actually and  expected results for step 5')
        # endregion
        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
