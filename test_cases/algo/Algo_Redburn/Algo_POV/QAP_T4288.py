import os
import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.core.test_case import TestCase
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.data_sets import constants

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T4288(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, data_set=None, environment=None):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.fix_env1 = self.environment.get_list_fix_environment()[0]

        # region th2 components
        self.fix_manager_sell = FixManager(self.fix_env1.sell_side, self.test_id)
        self.fix_manager_feed_handler = FixManager(self.fix_env1.feed_handler, self.test_id)
        self.fix_verifier_sell = FixVerifier(self.fix_env1.sell_side, self.test_id)
        self.fix_verifier_buy = FixVerifier(self.fix_env1.buy_side, self.test_id)
        # endregion

        self.qty = 100000
        self.percentage_volume = 120

        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name('account_2')
        self.s_par = self.data_set.get_listing_id_by_name('listing_36')

        # Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_1')
        self.key_params = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_2')

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel_replace = Status.CancelReplace
        self.status_cancel = Status.Cancel
        self.status_reject = Status.Reject
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        self.text_reject_invalid_percentage_of_volume = constants.FreeNotesReject.PricePoint2ParticipationMustBeEqualOrHigherThenPricePoint2Participation.value

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snapshot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        self.fix_manager_feed_handler.send_message(market_data_snapshot)

        time.sleep(3)

        # region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        pov_scaling_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_Scaling_params()
        pov_scaling_order.add_ClordId((os.path.basename(__file__)[:-3]))
        pov_scaling_order.change_parameters(dict(Account=self.client, OrderQty=self.qty))
        pov_scaling_order.update_fields_in_component('QuodFlatParameters', dict(MaxPercentageVolume=self.percentage_volume))

        self.fix_manager_sell.send_message_and_receive_response(pov_scaling_order, case_id_1)

        time.sleep(3)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(pov_scaling_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_pov_scaling_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(pov_scaling_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_pov_scaling_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew Parent')

        reject_moc_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(pov_scaling_order, self.gateway_side_sell, self.status_reject)
        reject_moc_order_params.change_parameters(dict(Text=self.text_reject_invalid_percentage_of_volume))
        self.fix_verifier_sell.check_fix_message(reject_moc_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Reject')

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        pass
