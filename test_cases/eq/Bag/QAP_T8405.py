import logging
import os
import random
import string
from pathlib import Path
import time
import xml.etree.ElementTree as ET

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, JavaApiFields, OrderBagConst, \
    OrdTypes, OrderReplyConst, SubmitRequestConst, ExecutionReportConst
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagDissociateRequest import OrderBagDissociateRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers import DataSet

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8405(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.nos = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.nos2 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.order_submit2 = OrderSubmitOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.bs_connectivity = self.fix_env.buy_side
        self.venue_client_account = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.currency = self.data_set.get_currency_by_name('currency_1')
        self.fix_verifier_bs = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.bag_creation_request = OrderBagCreationRequest()
        self.bag_wave_request = OrderBagWaveRequest()
        self.username = self.data_set.get_recipient_by_name("recipient_user_1")
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.cancel_ord = CancelOrderRequest()
        self.bag_dissociate_request = OrderBagDissociateRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_cs.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_cs.xml"
        self.qty = 100
        self.price = 20
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.ord_sub = OrderSubmitOMS(self.data_set)
        self.ord_sub2 = OrderSubmitOMS(self.data_set)
        self.order_submit = OrderSubmitOMS(data_set)
        self.order_submit2 = OrderSubmitOMS(data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.recipient = self.environment.get_list_fe_environment()[0].user_1
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region prepare pre-precondition:
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        quod.find("cs/dummyAveragePriceBag").text = "false"
        tree.write("temp.xml")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart QUOD.CS")
        time.sleep(40)

        # region Step 1 - Create 2 CO via FIX
        qty = '100'
        price = '456'

        resp = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos)
        resp2 = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos2)
        ord_id = resp[0].get_parameter("OrderID")
        ord_id2 = resp2[0].get_parameter("OrderID")
        orders_id = [ord_id, ord_id2]
        dict_orders_id = {ord_id: ord_id, ord_id2: ord_id2}
        # endregion

        # region Step 2 - Create Bag
        bag_name = 'QAP_T8405'
        self.bag_creation_request.set_default(BagChildCreationPolicy.AVP.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagName.value: bag_name,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, order_bag_notification, 'Step 2: Verify Bag is created')
        # endregion

        # region Step 3-4: Create Slice Orders from Bag
        slice_order_id1 = self._create_slide_order(bag_order_id, qty, price, 3)
        slice_order_id2 = self._create_slide_order(bag_order_id, qty, price, 4)
        # endregion

        # region Step 5: Execute Slice Orders
        self._execute_slice_order(slice_order_id1, orders_id, price)
        self._execute_slice_order(slice_order_id2, orders_id, price)
        # endregion

        # region Step 6 - Complete Bag
        self.complete_message.set_default_complete_for_some_orders(orders_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_message, dict_orders_id)
        # endregion

        # region Step 6 - check executions
        list_of_ignored_fields = ['Quantity', 'tag5120', 'TransactTime',
                                  'AllocTransType', 'ReportedPx', 'Side',
                                  'QuodTradeQualifier', 'BookID', 'SettlDate',
                                  'AllocID', 'Currency', 'NetMoney',
                                  'TradeDate', 'RootSettlCurrAmt', 'BookingType', 'GrossTradeAmt',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'AllocInstructionMiscBlock1',
                                  'Symbol', 'SecurityID', 'ExDestination', 'VenueType',
                                  'Price', 'ExecBroker', 'QtyType', 'OrderCapacity', 'LastMkt', 'OrdType',
                                  'LastPx', 'CumQty', 'LeavesQty', 'HandlInst', 'PositionEffect', 'TimeInForce',
                                  'OrderID', 'LastQty', 'ExecID', 'OrderQtyData', 'Account', 'OrderAvgPx', 'Instrument',
                                  'GatingRuleName', 'GatingRuleCondName', 'LastExecutionPolicy', 'SecondaryOrderID',
                                  'SecondaryExecID', 'NoParty', 'Text', 'NoStrategyParameters',
                                  'SettlCurrency', 'StrategyName', 'ClOrdID', 'TradeReportingIndicator']
        execution_report1 = FixMessageExecutionReportOMS(self.data_set)
        execution_report2 = FixMessageExecutionReportOMS(self.data_set)
        execution_report1.set_default_calculated(self.nos)
        execution_report2.set_default_calculated(self.nos2)
        execution_report1.change_parameters({'AvgPx': price})
        execution_report2.change_parameters({'AvgPx': price})
        self.fix_verifier_bs.check_fix_message_fix_standard(execution_report1,
                                                            ignored_fields=list_of_ignored_fields,
                                                            direction=DataSet.DirectionEnum.FromQuod)
        self.fix_verifier_bs.check_fix_message_fix_standard(execution_report2,
                                                            ignored_fields=list_of_ignored_fields,
                                                            direction=DataSet.DirectionEnum.FromQuod)
        # endregion

    def _create_slide_order(self, bag_order_id, qty, price, step):
        client_ord_id = bca.client_orderid(9)
        slice_order_id = None
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {
                                                         'Price': price,
                                                         'ExecutionPolicy': 'DMA',
                                                         'AvgPriceType': "EA",
                                                         'ExternalCare': 'N',
                                                         'SlicedOrderBagID': bag_order_id,
                                                         'OrdQty': qty,
                                                         'InstrID': self.data_set.get_instrument_id_by_name(
                                                             "instrument_2"),
                                                         'ClOrdID': client_ord_id
                                                     })
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity, self.venue_client_account, self.exec_destination, int(price))
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, client_ord_id). \
                get_parameters()[JavaApiFields.OrdReplyBlock.value]
            slice_order_id = order_reply[JavaApiFields.OrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply, f'Step {step}: Checking that Slice Order is created')
        except Exception as E:
            logger.error(f'Exception is {E}', exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single_rule)
        return slice_order_id

    def _execute_slice_order(self, slice_order_id, orders_id, price):
        filter_dict = {slice_order_id: slice_order_id}
        for co_order_id in orders_id:
            filter_dict.update({co_order_id: co_order_id})
        exec_qty = '50'
        self.execution_report.set_default_trade(slice_order_id)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             "LastTradedQty": exec_qty,
                                                             "LastPx": price,
                                                             "OrdType": "Limit",
                                                             "Price": price,
                                                             "Currency": self.currency,
                                                             "ExecType": "Trade",
                                                             "TimeInForce": "Day",
                                                             "LeavesQty": '0',
                                                             "CumQty": exec_qty,
                                                             "AvgPrice": price,
                                                             "LastMkt": self.exec_destination,
                                                             "OrdQty": exec_qty
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report, filter_dict)

        execution_report_of_slice_order = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                                 filter_dict[slice_order_id]). \
            get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values({
            JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value
        }, execution_report_of_slice_order,
            f'Step 5: Checking TransExecStatus for Slicing Order {slice_order_id}')

    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart QUOD.CS")
        time.sleep(40)
        os.remove("temp.xml")
        self.ssh_client.close()