import time
import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, BasketMessagesConst, \
    OrdListNotificationConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderListOMS import FixNewOrderListOMS
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCreationRequest import OrderListWaveCreationRequest
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageListStatusOMS import FixMessageListStatusOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.fix_wrappers import DataSet

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

class QAP_T7199(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.ord_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.message_list = FixMessageNewOrderListOMS(self.data_set).set_default_order_list()
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.route_id = self.data_set.get_route_id_by_name('route_1')
        self.new_price = "456"
        self.create_wave_request = OrderListWaveCreationRequest()
        self.bs_connectivity = self.fix_env.buy_side
        # self.rule_client = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")
        self.rule_client = self.data_set.get_venue_client_names_by_name("client_co_1_venue_1")
        self.mic = self.data_set.get_mic_by_name("mic_1")
        # self.price = '20'
        # self.qty = '100'
        self.price1 = "50"
        self.qty1 = "100"
        self.price2 = "60"
        self.qty2 = "150"
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])
        self.fix_verifier_bs = FixVerifier(self.bs_connectivity, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region - Step 1 - Send NewOrderList
        self.message_list.base_parameters["ListOrdGrp"]["NoOrders"][0]["Side"]='2'
        self.message_list.base_parameters["ListOrdGrp"]["NoOrders"][0]["Price"]='50'
        self.message_list.base_parameters["ListOrdGrp"]["NoOrders"][1]["Side"]='1'
        self.message_list.base_parameters["ListOrdGrp"]["NoOrders"][1]["OrderQtyData"]={'OrderQty': "150"}
        self.message_list.base_parameters["ListOrdGrp"]["NoOrders"][1]["PreAllocGrp"]['NoAllocs'][0]['AllocQty']='150'
        self.message_list.base_parameters["ListOrdGrp"]["NoOrders"][1]["Price"]='60'
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.message_list)
        list_id = response[0].get_parameters()['ListID']
        ord_id1 = response[1].get_parameters()['OrderID']
        ord_id2 = response[2].get_parameters()['OrderID']
        # endregion

        # region - Step 1 - Check ListStatus
        ignore_field = ['Text']
        list_status = FixMessageListStatusOMS().set_default_list_status(self.message_list)
        self.fix_verifier.check_fix_message_fix_standard(list_status, ignored_fields=ignore_field)
        # endregion

        # region - Step 2 - Set-up parameters for ExecutionReports
        list_of_ignored_fields = ['SettlDate', 'SettlType', 'Account', 'GatingRuleCondName', 'GatingRuleName', 'Text']
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new_list(self.message_list)
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_new_list(self.message_list, 1)
        # endregion

        # region - Step 2 - Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(exec_report1, ignored_fields=list_of_ignored_fields)
        self.fix_verifier.check_fix_message_fix_standard(exec_report2, ignored_fields=list_of_ignored_fields)
        # endregion

        # regin - Step 3 - Wave Basket
        order_list_query = self.db_manager.execute_query(f"SELECT orderlistid from orderlist o where o.listid = '{list_id}'")
        order_list_id = order_list_query[0][0]
        self.create_wave_request.set_default(order_list_id, [ord_id1, ord_id2])
        route_params = {"RouteID": self.route_id}
        self.create_wave_request.update_fields_in_component('OrderListWaveCreationRequestBlock', route_params)
        try:
            nos_rule1 = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.rule_client,
                                                                                                  self.mic,
                                                                                                  int(self.price1))
            trade_rule1 = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.rule_client,
                                                                                            self.mic,
                                                                                            float(self.price1),
                                                                                            int(self.qty1), 2)
            nos_rule2 = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.rule_client,
                                                                                                  self.mic,
                                                                                                  int(self.price2))
            trade_rule2 = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.rule_client,
                                                                                            self.mic,
                                                                                            float(self.price2),
                                                                                            int(self.qty2), 2)
            self.java_api_manager.send_message_and_receive_response(self.create_wave_request)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule1)
            self.rule_manager.remove_rule(trade_rule1)
            self.rule_manager.remove_rule(nos_rule2)
            self.rule_manager.remove_rule(trade_rule2)
        list_wave_notif = self.java_api_manager.get_last_message(ORSMessageType.OrderListWaveNotification.value)
        wave_notif_block = list_wave_notif.get_parameter(JavaApiFields.OrderListWaveNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderListWaveStatus.value: OrdListNotificationConst.OrderListWaveStatus_TER.value,
             JavaApiFields.PercentQtyToRelease.value: '1.0', JavaApiFields.RouteID.value: str(self.route_id)}, {
                JavaApiFields.OrderListWaveStatus.value:
                    wave_notif_block[
                        JavaApiFields.OrderListWaveStatus.value],
                JavaApiFields.PercentQtyToRelease.value:
                    wave_notif_block[
                        JavaApiFields.PercentQtyToRelease.value], JavaApiFields.RouteID.value: wave_notif_block[
                    JavaApiFields.RouteID.value]},
            "Step 3 - Check Wave values")
        # endregion
        # region - Step 3 - Check ExecutionReports
        change_parameters3 = {
            'OrderID': ord_id1,
        }
        change_parameters4 = {
            'OrderID': ord_id2,
        }
        list_of_ignored_fields = ['Quantity', 'tag5120', 'TransactTime',
                                  'AllocTransType', 'ReportedPx', 'AvgPx',
                                  'QuodTradeQualifier', 'BookID', 'SettlDate',
                                  'AllocID', 'Currency', 'NetMoney',
                                  'TradeDate', 'RootSettlCurrAmt', 'BookingType', 'GrossTradeAmt',
                                  'IndividualAllocID', 'AllocNetPrice', 'AllocPrice', 'AllocInstructionMiscBlock1',
                                  'Symbol', 'SecurityID', 'ExDestination', 'VenueType', 'ExecBroker', 'QtyType',
                                  'OrderCapacity', 'LastMkt',
                                  'LastPx', 'CumQty', 'LeavesQty', 'HandlInst', 'PositionEffect', 'TimeInForce',
                                  'LastQty', 'ExecID', 'Account', 'OrderAvgPx', 'Instrument',
                                  'GatingRuleName', 'GatingRuleCondName', 'LastExecutionPolicy', 'SecondaryOrderID',
                                  'SecondaryExecID', 'NoParty', 'Text', 'NoStrategyParameters',
                                  'SettlCurrency', 'StrategyName', 'ClOrdID', 'ReplyReceivedTime', 'ExpireDate', 'Parties', 'TradeReportingIndicator'
                                  ]
        exec_report3 = FixMessageExecutionReportOMS(self.data_set, change_parameters3)
        exec_report3.change_parameters(
            {'OrderQtyData': {'OrderQty': "100"}, 'OrdStatus': '2', 'OrdType': '2', 'Price': '50', 'Side': '2',
             "ExecType": "F"})
        exec_report4 = FixMessageExecutionReportOMS(self.data_set, change_parameters4)
        exec_report4.change_parameters(
            {'OrderQtyData': {'OrderQty': "150"}, 'OrdStatus': '2', 'OrdType': '2', 'Price': '60', 'Side': '1',
             "ExecType": "F"})
        self.fix_verifier.check_fix_message_fix_standard(exec_report3,
                                                            key_parameters=['OrderID', 'ExecType'],
                                                            ignored_fields=list_of_ignored_fields,
                                                            direction=DataSet.DirectionEnum.FromQuod)
        self.fix_verifier.check_fix_message_fix_standard(exec_report4,
                                                            key_parameters=['OrderID', 'ExecType'],
                                                            ignored_fields=list_of_ignored_fields,
                                                            direction=DataSet.DirectionEnum.FromQuod)
        # endregion