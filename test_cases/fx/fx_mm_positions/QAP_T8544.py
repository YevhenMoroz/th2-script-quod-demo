import time
from datetime import datetime
from pathlib import Path

from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest

from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.oms_data_set.oms_data_set import OmsDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.DataSet import DirectionEnum

from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.RequestForFXPositions import RequestForFXPositions
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from custom import basic_custom_actions as bca
from test_framework.rest_api_wrappers.forex.RestApiPriceCleansingStaleRatesMessages import \
    RestApiPriceCleansingStaleRatesMessages
from test_framework.win_gui_wrappers.forex.rates_tile import RatesTile


class QAP_T8544(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.position_request = RequestForFXPositions(data_set=self.data_set)
        self.act_java_api = Stubs.act_java_api


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.position_request.set_default_params()
        # self.position_request.change_subject("CLIENT1")
        self.java_api_manager.send_message(self.position_request)

        self.sleep(10)
        self.position_request.set_unsubscribe()
        self.java_api_manager.send_message(self.position_request)
        # params_for_request = {
        #         "SEND_SUBJECT": "QUOD.CLIENT1_1.POSIT",
        #         "REPLY_SUBJECT": "QUOD.POSIT.CLIENT1_1",
        #         "RequestForFXPositionsBlock": {
        #             # "ClientPosReqID": "1234561",
        #             "PosReqType": "Positions",
        #             "AccountID": "CLIENT1",
        #             "Currency": "USD",
        #             "SubscriptionRequestType": "Subscribe",
        #         }
        #
        # }
        # #
        # self.act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
        #     message=bca.message_to_grpc('Order_RequestForFXPositions', params_for_request, self.java_api_env)))

        # ja_connectivity = "314_java_api"
        # ja_manager = JavaApiManager(ja_connectivity, bca.create_event(Path(__file__).name[:-3]))
        # ord_submit = OrderSubmitOMS(OmsDataSet()).set_default_dma_market()
        # ja_manager.send_message(ord_submit)
