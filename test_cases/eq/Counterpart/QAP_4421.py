import logging
import os
import time

from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.DataSet import Instrument
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import decorator_try_except
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP4421(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__)[:-3], self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity
        self.dc_connectivity = SessionAliasOMS().dc_connectivity

    def qap_4421(self):
        # region Declaration
        fix_manager = FixManager(self.ss_connectivity, self.report_id)
        fix_verifier = FixVerifier(self.ss_connectivity, self.case_id)
        ord_book = OMSOrderBook(self.case_id, self.session_id)
        main_win = BaseMainWindow(self.case_id, self.session_id)
        ord_ticket = OMSOrderTicket(self.case_id, self.session_id)
        clt_inbox = OMSClientInbox(self.case_id, self.session_id)
        client = "CLIENT_COUNTERPART"
        alloc_acc = "CLIENT_COUNTERPART_SA1"
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        # endregion
        # region Open FE
        main_win.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region create Care order
        change_params = {'Account': client,
                         'ExDestination': 'XEUR',
                         'PreAllocGrp': {
                             'NoAllocs': [{
                                 'AllocAccount': alloc_acc,
                                 'AllocQty': "100"}]}, }
        nos = FixMessageNewOrderSingleOMS().set_default_care_limit(Instrument.ISI1).change_parameters(change_params)
        fix_manager.send_message_and_receive_response_fix_standard(nos)
        cl_ord_id = nos.get_parameters()['ClOrdID']
        qty = nos.get_parameters()['OrderQtyData']['OrderQty']
        price = nos.get_parameters()['Price']
        # endregion
        # region Accept order
        clt_inbox.accept_order("EUREX", qty, price)
        # endregion
        # region Split
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                             client + "_EUREX", "XEUR",
                                                                                             20)
            trade_rele = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                       client + "_EUREX", "XEUR", 20,
                                                                                       100, 2)
            ord_ticket.split_order(['ClOrdID', cl_ord_id])

        finally:
            time.sleep(1)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rele)
        # endregion
        # region Un-match
        exec_id = ord_book.extract_2lvl_fields("Executions", ["ExecID"], [1])
        exec_id = exec_id[0]['ExecID']
        order_un_match_detail = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'UnMatchRequestBlock': {
                'UnMatchingList': {'UnMatchingBlock': [
                    {'VirtualExecID': exec_id, 'UnMatchingQty': qty, 'SourceAccountID': "CareWB",
                     'PositionType': "N"}
                ]},
                'DestinationAccountID': 'PROP'
            }
        }

        Stubs.act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
            message=bca.message_to_grpc_fix_standard("Order_UnMatchRequest",
                                                     order_un_match_detail, self.ss_connectivity),
            parent_event_id=self.case_id))
        # endregion
        # region Set-up parameters for ExecutionReports
        parties = {
            'NoPartyIDs': [
                {'PartyRole': "28",
                 'PartyID': "CustodianUser",
                 'PartyIDSource': "C"},
                {'PartyRole': "66",
                 'PartyID': "MarketMaker - TH2Route",
                 'PartyIDSource': "C"},
                {'PartyRole': "67",
                 'PartyID': "InvestmentFirm - ClCounterpart_SA1",
                 'PartyIDSource': "C"}

            ]
        }
        exec_report = FixMessageExecutionReportOMS().set_default_filled(nos).change_parameters(
            {"Parties": parties})
        # endregion
        # region Check ExecutionReports
        fix_verifier.check_fix_message_fix_standard(exec_report)
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_4421()
