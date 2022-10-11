import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.ManualOrderCrossRequest import ManualOrderCrossRequest
from test_framework.win_gui_wrappers.java_api_constants import SubmitRequestConst
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7515(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.price = "5"
        self.price2 = "7"
        self.last_mkt = "BAML"
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client = self.data_set.get_client_by_name("client_pt_1")
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.manual_cross_request = ManualOrderCrossRequest()
        self.rule_manager = RuleManager()
        self.result = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO orders (precondition)
        list_of_cl_ord_id = list()
        list_of_order_id = list()
        list_of_qty = ["100", "70", "30"]
        for qty in list_of_qty:
            submit_request = OrderSubmitOMS(self.data_set)
            submit_request.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                  desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                  role=SubmitRequestConst.USER_ROLE_1.value)
            submit_request.update_fields_in_component('NewOrderSingleBlock',
                                                      {'OrdCapacity': SubmitRequestConst.OrdCapacity_Agency.value,
                                                       'OrdQty': qty,
                                                       'AccountGroupID': self.client}
                                                      )
            if qty != "100":
                submit_request.update_fields_in_component('NewOrderSingleBlock', {'Side': 'Sell'})
            submit_request.remove_fields_from_component('NewOrderSingleBlock', ['SettlCurrency'])
            responses = self.java_api_manager.send_message_and_receive_response(submit_request)
            self.return_result(responses, ORSMessageType.OrdReply.value)
            list_of_order_id.append(self.result.get_parameter('OrdReplyBlock')['OrdID'])
            list_of_cl_ord_id.append(self.result.get_parameter('OrdReplyBlock')['ClOrdID'])
        # endregion

        # region manual cross first and second and third CO order
        self.manual_cross_request.set_default(self.data_set, list_of_order_id[0],
                                              list_of_order_id[1], self.price, list_of_qty[1])
        self.manual_cross_request.update_fields_in_component('ManualOrderCrossRequestBlock', {'LastMkt': self.last_mkt})
        self.java_api_manager.send_message(self.manual_cross_request)

        self.manual_cross_request.set_default(self.data_set, list_of_order_id[0],
                                              list_of_order_id[2], self.price, list_of_qty[2])
        self.manual_cross_request.update_fields_in_component('ManualOrderCrossRequestBlock', {'LastMkt': self.last_mkt})
        self.java_api_manager.send_message(self.manual_cross_request)

        # endregion

        # region check fix message for orders step 5

        list_of_ignore_fields = ['SecondaryOrderID', 'LastExecutionPolicy', 'TradeDate', 'SecondaryExecID',
                                 'ExDestination', 'GrossTradeAmt', 'SettlCurrency', 'Instrument', 'TimeInForce',
                                 'OrdType', "TradeReportingIndicator", 'SettlDate', 'Side', 'HandlInst', 'OrderQtyData',
                                 'SecondaryExecID',
                                 'ExecID', 'LastQty', 'TransactTime',
                                 'AvgPx', 'QuodTradeQualifier', 'BookID', 'Currency',
                                 'PositionEffect', 'TrdType', 'LeavesQty', 'NoParty',
                                 'CumQty', 'LastPx', 'LastCapacity', 'tag5120', 'LastMkt', 'OrderCapacity', 'QtyType',
                                 'ExecBroker', 'Price', 'QtyType', 'OrderCapacity', 'OrderID']
        change_parameters = None
        for cl_ord_id in list_of_cl_ord_id:
            change_parameters = {
                "ExecType": "F", "OrdStatus": "2", "Account": self.client, "ClOrdID": cl_ord_id,
                'TrdSubType': '37', 'VenueType': 'O'
            }
            self.check_execution_reports(change_parameters, list_of_ignore_fields)
        change_parameters['OrdStatus'] = '1'
        change_parameters['ClOrdID'] = list_of_cl_ord_id[0]
        self.check_execution_reports(change_parameters, list_of_ignore_fields)
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response

    def check_execution_reports(self, change_parameters, list_of_ignore_fields):
        fix_execution_report = FixMessageExecutionReportOMS(self.data_set, change_parameters)
        self.fix_verifier.check_fix_message_fix_standard(fix_execution_report, ignored_fields=list_of_ignore_fields)
