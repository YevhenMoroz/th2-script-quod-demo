import logging
import os
import time

from th2_grpc_act_gui_quod.common_pb2 import ScrollingOperation
from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageListStatusOMS import FixMessageListStatusOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import decorator_try_except
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from win_gui_modules.common_wrappers import GridScrollingDetails
from win_gui_modules.utils import call

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_5587(TestCase):
    def __init__(self, report_id, session_id):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__)[:-3], self.test_id)
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity
        self.ja_connectivity = SessionAliasOMS().ja_connectivity

    def qap_5587(self):
        # region Declaration
        fix_manager = FixManager(self.ss_connectivity, self.case_id)
        fix_verifier = FixVerifier(self.ss_connectivity, self.case_id)
        cl_inbox = OMSClientInbox(self.case_id, self.session_id)
        main_window = BaseMainWindow(self.case_id, self.session_id)
        basket_book = OMSBasketOrderBook(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        nol = FixMessageNewOrderListOMS().set_default_order_list()
        client = nol.get_parameters()["ListOrdGrp"]["NoOrders"][0]["Account"]
        price = nol.get_parameters()["ListOrdGrp"]["NoOrders"][0]["Price"]
        qty = nol.get_parameters()["ListOrdGrp"]["NoOrders"][0]["OrderQtyData"]["OrderQty"]
        lokup = "VETO"
        # endregion
        # region Open FE
        main_window.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region Send NewOrderList
        fix_manager.send_message_and_receive_response_fix_standard(nol)
        # endregion
        # region Set-up parameters for ListStatus
        list_status = FixMessageListStatusOMS().set_default_list_status(nol)
        # endregion
        # region Check ListStatus
        fix_verifier.check_fix_message_fix_standard(list_status)
        # endregion
        # region Accept orders
        cl_inbox.accept_order(lokup, qty, price)
        cl_inbox.accept_order(lokup, qty, price)
        # endregion
        # region Set-up parameters for ExecutionReports
        exec_report1 = FixMessageExecutionReportOMS().set_default_new_list(nol)
        exec_report2 = FixMessageExecutionReportOMS().set_default_new_list(nol, 1)
        # endregion
        # region Check ExecutionReports
        fix_verifier.check_fix_message_fix_standard(exec_report1)
        fix_verifier.check_fix_message_fix_standard(exec_report2)
        # endregion
        # region Send wave request
        basket_id = basket_book.get_basket_value("Id")
        basket_ord_id = basket_book.get_basket_orders_value(2, "Id")
        wave_list_params = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'OrderListWaveCreationRequestBlock': {
                'ParentOrdrList': {'ParentOrdrBlock': [
                    {'ParentOrdID': basket_ord_id["1"]}, {'ParentOrdID': basket_ord_id["2"]}
                ]},
                'OrderListID': basket_id,
                'PercentQtyToRelease': "1.000000000",
                'QtyPercentageProfile': "RemainingQty"
            }
        }
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                             client + "_PARIS", "XPAR",
                                                                                             int(price))
            trade_rele = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                       client + "_PARIS", "XPAR",
                                                                                       int(price), int(qty), 2)
            Stubs.act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
                message=bca.message_to_grpc_fix_standard("Order_OrderListWaveCreationRequest",
                                                         wave_list_params, self.ja_connectivity),
                parent_event_id=self.case_id))
        finally:
            time.sleep(1)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rele)
        # endregion
        # region Set-up parameters for ExecutionReports
        exec_report3 = FixMessageExecutionReportOMS().set_default_filled_list(nol)
        exec_report4 = FixMessageExecutionReportOMS().set_default_filled_list(nol, 1)
        # endregion
        # region Check ExecutionReports
        fix_verifier.check_fix_message_fix_standard(exec_report3, key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
        fix_verifier.check_fix_message_fix_standard(exec_report4, key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
        # endregion

    #@decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_5587()
