import logging
import os
import time
from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest

from custom import basic_custom_actions as bca
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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_5860(TestCase):
    def __init__(self, report_id, session_id):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__)[:-3], self.test_id)
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity
        self.dc_connectivity = SessionAliasOMS().dc_connectivity

    def qap_5860(self):
        # region Declaration
        fix_manager = FixManager(self.ss_connectivity, self.report_id)
        fix_verifier = FixVerifier(self.ss_connectivity, self.case_id)
        main_win = BaseMainWindow(self.case_id, self.session_id)
        clt_inbox = OMSClientInbox(self.case_id, self.session_id)
        client = "CLIENT_COUNTERPART"
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        # endregion
        # region Open FE
        main_win.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region create Care orders
        change_params = {'Account': client}
        nos1 = FixMessageNewOrderSingleOMS().set_default_care_limit(Instrument.FR0004186856).change_parameters(
            change_params)
        response_1 = fix_manager.send_message_and_receive_response_fix_standard(nos1)
        change_params.update({"Side": "2"})
        nos2 = FixMessageNewOrderSingleOMS().set_default_care_limit(Instrument.FR0004186856).change_parameters(
            change_params)
        time.sleep(1)
        response_2 = fix_manager.send_message_and_receive_response_fix_standard(nos2)
        ord_id_1 = response_1[0].get_parameters()['OrderID']
        ord_id_2 = response_2[0].get_parameters()['OrderID']
        qty = nos1.get_parameters()['OrderQtyData']['OrderQty']
        price = nos1.get_parameters()['Price']
        # endregion
        # # region Accept order
        clt_inbox.accept_order("EUREX", qty, price)
        clt_inbox.accept_order("EUREX", qty, price)
        # # endregion

        # region Manual cross
        manual_order_cross_params = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'ManualOrderCrossRequestBlock': {
                'ManualOrderCrossTransType': 'New',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'TradeDate': (tm(datetime.utcnow().isoformat())).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'ExecPrice': '5.000000000',
                'ExecQty': '100.000000000',
                'ListingID': '9500000043',
                'OrdID1': ord_id_1,
                'OrdID2': ord_id_2,
                'LastCapacity': 'Agency',
                'LastMkt': 'UBSG'
            }
        }

        Stubs.act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
            message=bca.message_to_grpc_fix_standard("Order_ManualOrderCrossRequest",
                                                     manual_order_cross_params, "317_java_api"),
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
                 'PartyID': "InvestmentFirm - ClCounterpart",
                 'PartyIDSource': "C"},
                {'PartyRole': "10",
                 'PartyID': "CREST",
                 'PartyIDSource': "D"},

            ]
        }
        exec_report_new = FixMessageExecutionReportOMS().set_default_new(nos2).change_parameters(
            {"Parties": parties})
        exec_report_filled = FixMessageExecutionReportOMS().set_default_filled(nos2)
        # endregion
        # region Check ExecutionReports
        fix_verifier.check_fix_message_fix_standard(exec_report_new)
        fix_verifier.check_fix_message_fix_standard(exec_report_filled)
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_5860()
