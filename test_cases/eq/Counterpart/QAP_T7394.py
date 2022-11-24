import logging
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst, \
    JavaApiPartyRoleConstants
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7394(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.price = self.fix_message.get_parameter("Price")
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.manual_execution = TradeEntryOMS(data_set=self.data_set)
        self.fix_message.change_parameters({"Account": self.client})
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.cl_ord_id = self.fix_message.get_parameter('ClOrdID')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        class_name = QAP_T7394
        # region Declaration
        # region send fix message
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        client_ord_id = response[0].get_parameter("ClOrdID")

        # endregion

        # region check order is created
        parties = {
            'NoPartyIDs': [
                self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart'),
                self.data_set.get_counterpart_id_fix('counterpart_id_regulatory_body_venue_paris'),
                self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
                self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user_2'),
                {'PartyRole': "*",
                 'PartyRoleQualifier': '*',
                 'PartyID': "*",
                 'PartyIDSource': "*"}
            ]
        }
        list_of_ignored_fields = ['SettlCurrency', 'LastExecutionPolicy', 'SecondaryOrderID', 'LastMkt', 'VenueType',
                                  'SecondaryExecID', 'MiscFeesGrp', 'CommissionData', 'SecurityDesc', 'PartyID',
                                  'PartyRoleQualifier']
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new(self.fix_message).change_parameters(
            {'Parties': parties})
        exec_report1.change_parameters({'ExecType': '0', 'OrdStatus': '0'})
        self.fix_verifier.check_fix_message_fix_standard(exec_report1,
                                                         key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'],
                                                         ignored_fields=list_of_ignored_fields)
        # endregion
        # region manual execution
        self.manual_execution.set_default_trade(order_id, self.price)
        self.manual_execution.update_fields_in_component('TradeEntryRequestBlock',
                                                         {'CounterpartList': {'CounterpartBlock':
                                                             [
                                                                 self.data_set.get_counterpart_id_java_api(
                                                                     'counterpart_executing_firm'),
                                                                 self.data_set.get_counterpart_id_java_api(
                                                                     'counterpart_contra_firm')]
                                                         }})
        responses = self.java_api_manager.send_message_and_receive_response(self.manual_execution)
        class_name.__print_message(f"{class_name}-RESPONSE AFTER MANUAL EXECUTION", responses)
        parties['NoPartyIDs'].remove({'PartyRole': "*",
                 'PartyRoleQualifier': '*',
                 'PartyID': "*",
                 'PartyIDSource': "*"})
        print(parties['NoPartyIDs'])
        parties['NoPartyIDs'].extend([self.data_set.get_counterpart_id_fix('counter_part_id_executing_firm'),
                                      self.data_set.get_counterpart_id_fix('counter_part_id_contra_firm'),
                                      self.data_set.get_counterpart_id_fix('counterpart_java_api_user')])
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(
            self.fix_message).change_parameters(
            {"Parties": parties})

        self.fix_verifier.check_fix_message_fix_standard(exec_report2, ignored_fields=list_of_ignored_fields)
        sts_of_order_after_trade = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
                JavaApiFields.OrderNotificationBlock.value][JavaApiFields.TransStatus.value]
        exec_sts = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value][JavaApiFields.TransExecStatus.value]
        self.order_book.compare_values(
            {OrderBookColumns.exec_sts.value: ExecutionReportConst.TransExecStatus_FIL.value,
             OrderBookColumns.sts.value: OrderReplyConst.TransStatus_OPN.value}, {
                OrderBookColumns.exec_sts.value: exec_sts,
                OrderBookColumns.sts.value: sts_of_order_after_trade
            }, 'Comparing values of order')
        counterparts = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value][JavaApiFields.CounterpartList.value][
            JavaApiFields.CounterpartBlock.value]
        contra_firm = self.find_counterpart(JavaApiPartyRoleConstants.PartyRole_CNF.value, counterparts)
        excuting_firm = self.find_counterpart(JavaApiPartyRoleConstants.PartyRole_EXF.value, counterparts)
        self.order_book.compare_values({'ContraFirm': contra_firm,
                                        'ExecutingFirm': excuting_firm},
                                       {'ContraFirm': JavaApiPartyRoleConstants.PartyRole_CNF.value,
                                        'ExecutingFirm': JavaApiPartyRoleConstants.PartyRole_EXF.value},
                                       'Comparing expected and actual results of ContraFirm and ExecutingFirm')
        # endregion

    @staticmethod
    def __print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())

    def find_counterpart(self, counterpart_value, counterparts_list):
        for counterpart in counterparts_list:
            if counterpart[JavaApiFields.PartyRole.value] == counterpart_value:
                return counterpart_value
            else:
                if counterpart == counterparts_list[len(counterparts_list) - 1]:
                    return 'Your conterpart is missing in repeating group'
