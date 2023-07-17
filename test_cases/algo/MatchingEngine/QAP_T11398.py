import os
import sched
import time
from copy import deepcopy
from datetime import datetime, timedelta, timezone

from pathlib import Path

import pytz

from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.algo_mongo_manager import AlgoMongoManager as AMM
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, TimeInForce, FreeNotesReject
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixMessageOrderCancelReplaceRequest import FixMessageOrderCancelReplaceRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.formulas_and_calculation.trading_phase_manager import TradingPhaseManager, TimeSlot
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager


class QAP_T11398(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, data_set=None, environment=None):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.fix_env1 = self.environment.get_list_fix_environment()[0]

        # region th2 componentsMACHINE GUN KELLY
        self.fix_manager_sell = FixManager(self.fix_env1.sell_side, self.test_id)
        self.fix_manager_feed_handler = FixManager(self.fix_env1.feed_handler, self.test_id)
        self.fix_verifier_sell = FixVerifier(self.fix_env1.sell_side, self.test_id)
        self.fix_verifier_buy = FixVerifier(self.fix_env1.buy_side, self.test_id)
        # endregion

        # region order parameters
        self.qty = 1000
        self.price = 30
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        self.status_eliminate = Status.Eliminate
        self.status_reject = Status.Reject
        self.status_fill = Status.Fill
        # endregion

        self.free_notes = FreeNotesReject.CouldNotRetrieveAverageVolumeDistribution.value

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_me")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.client = self.data_set.get_client_by_name("client_3")
        self.mic = self.data_set.get_mic_by_name("mic_63")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        # endregion


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):


        case_id_1 = bca.create_event("Create DMA Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        # region Send dma order
        self.dma_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_ME_params()
        self.dma_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.dma_order.change_parameters(dict(OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.mic))
        self.fix_manager_sell.send_message_and_receive_response(fix_message=self.dma_order, case_id=case_id_1)
        # endregion


        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(fix_message=self.dma_order, key_parameters=self.key_params_NOS_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new = FixMessageExecutionReportAlgo().set_params_from_new_order_single_dma(self.dma_order, self.status_pending)
        self.fix_verifier_sell.check_fix_message(fix_message=er_pending_new, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new = FixMessageExecutionReportAlgo().set_params_from_new_order_single_dma(self.dma_order, self.status_new)
        self.fix_verifier_sell.check_fix_message(fix_message=er_new, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion


    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):

        time.sleep(3)
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Check that order is Canceled", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        time.sleep(2)

        cancel_request_dma_order = FixMessageOrderCancelRequest(self.dma_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_dma_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_dma_order, direction=self.ToQuod, message_name='Sell side Cancel Request')


        # region check cancellation parent VWAP order
        cancel_dma_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single_dma(self.dma_order, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_dma_order, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion


