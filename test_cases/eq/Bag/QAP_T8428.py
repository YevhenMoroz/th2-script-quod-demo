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
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.java_api_wrappers.ors_messages.OrderActionRequest import OrderActionRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagDissociateRequest import OrderBagDissociateRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest
from test_framework.java_api_wrappers.ors_messages.TradeEntryBatchRequest import TradeEntryBatchRequest
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers import DataSet

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8428(TestCase):
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
        self.trade_entry_batch_request = TradeEntryBatchRequest()
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.order_action_request = OrderActionRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Pre-precondition:
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        quod.find("cs/dummyAveragePriceBag").text = "false"
        tree.write("temp.xml")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart QUOD.CS")
        time.sleep(40)
        # endregion

        # region Step 1 - Create 2 CO via FIX
        resp = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos)
        resp2 = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos2)
        ord_id = resp[0].get_parameter("OrderID")
        ord_id2 = resp2[0].get_parameter("OrderID")
        orders_id = [ord_id, ord_id2]
        dict_orders_id = {ord_id: ord_id, ord_id2: ord_id2}
        # endregion

        # region Step 2 - Create Bag
        bag_name = 'QAP_T8428'
        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagName.value: bag_name,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, order_bag_notification, 'Step 2: Verify bag is created')
        # endregion

        # region Step 3 - Partially Fill 1st Care Order
        trd_qty = int(self.qty) // 2
        self.trade_entry_request.set_default_trade(ord_id, exec_price=self.price, exec_qty=trd_qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        execution_report_co_order1 = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value). \
            get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report_co_order1, 'Step 3: Checking execution for 1st Care Order')
        # endregion

        # region Step 4 - Fully fill 1st Care Order
        trd_qty = int(self.qty) // 2
        self.trade_entry_request.set_default_trade(ord_id, exec_price=self.price, exec_qty=trd_qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        execution_report_co_order2 = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value). \
            get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            execution_report_co_order2, 'Step 4: Checking execution for 1st Care Order')
        # endregion

        # region Step 5 - Complete Bag
        self.complete_message.set_default_complete_for_some_orders(orders_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_message, dict_orders_id)
        for order_id in orders_id:
            order_reply = \
                self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, order_id).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
                 JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
                order_reply,
                f'Step 5: Checking Order {order_id} PostTradeStatus and DoneForDay')

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
                                  'SecondaryExecID', 'NoParty', 'Text', 'NoStrategyParameters', 'Parties', 'TradeReportingIndicator',
                                  'SettlCurrency', 'StrategyName']
        execution_report1 = FixMessageExecutionReportOMS(self.data_set)
        execution_report2 = FixMessageExecutionReportOMS(self.data_set)
        execution_report1.set_default_calculated(self.nos)
        execution_report2.set_default_new(self.nos2)
        execution_report1.change_parameters({'AvgPx': self.price})
        self.fix_verifier.check_fix_message_fix_standard(execution_report1,
                                                            ignored_fields=list_of_ignored_fields,
                                                            direction=DataSet.DirectionEnum.FromQuod)
        self.fix_verifier.check_fix_message_fix_standard(execution_report2,
                                                            ignored_fields=list_of_ignored_fields,
                                                            direction=DataSet.DirectionEnum.FromQuod)

        # endregion


    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart QUOD.CS")
        time.sleep(40)
        os.remove("temp.xml")
        self.ssh_client.close()