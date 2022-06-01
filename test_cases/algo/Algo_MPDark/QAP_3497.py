import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants

from datetime import datetime, timedelta
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from custom.basic_custom_actions import convert_to_request, message_to_grpc
from stubs import Stubs
from test_framework.data_sets import constants

class QAP_3497(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, data_set=None, environment=None):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.fix_env1 = self.environment.get_list_fix_environment()[0]

        # region th2 components
        self.fix_manager_sell = FixManager('fix-sell-side-319-kepler', self.test_id)
        self.fix_manager_feed_handler = FixManager('fix-fh-319-kepler', self.test_id)
        self.fix_verifier_sell = FixVerifier('fix-sell-side-319-kepler', self.test_id)
        self.fix_verifier_buy = FixVerifier('fix-buy-side-319-kepler', self.test_id)
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager()
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew('fix-buy-side-319-kepler', "BATSDARK_KEPLER", "BATD", 20)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew('fix-buy-side-319-kepler', "CHIXDELTA_KEPLER", "CHID", 20)
        nos_3_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew('fix-buy-side-319-kepler', "KEPLER", "CEUD", 20) # CBOEEUDARK
        nos_1_fok_rule = rule_manager.add_NewOrdSingle_FOK('fix-buy-side-319-kepler', "KEPLER", "XPOS", False, 20) # ITG
        nos_2_fok_rule = rule_manager.add_NewOrdSingle_FOK('fix-buy-side-319-kepler', "KEPLER", "TQEM", False, 20) # TQDARKEU
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport('fix-buy-side-319-kepler', False)
        self.rule_list = [nos_1_rule, nos_2_rule, nos_3_rule, nos_1_fok_rule, nos_2_fok_rule, ocrr_rule]
        # endregion

        # TODO test steps

    # @try_except(test_id=Path(__file__).name[:-3])
    # def run_post_conditions(self):
    #     RuleManager.remove_rules(self.rule_list)