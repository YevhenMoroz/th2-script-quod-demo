import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


# Warning! This is the manual test case. It needs to do manual checking audit trail and doesn`t include in regression script
class QAP_T4960(TestCase):
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

        # region order parameters
        self.qty = 1000
        self.price = 25
        self.traded_qty = 0
        self.dark_price = 45
        self.traded_qty = 0
        self.qty_for_md = 500
        self.price_ask = 45
        self.price_bid = 30
        self.px_for_incr = 0
        self.qty_for_incr = 0
        self.delay = 0
        self.tif_iok = constants.TimeInForce.ImmediateOrCancel.value
        self.sell = constants.OrderSide.Sell.value
        self.algopolicy = constants.ClientAlgoPolicy.qa_sorping_4.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_eliminate = Status.Eliminate
        self.status_cancel = Status.Cancel
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_8")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_quodlit1 = self.data_set.get_mic_by_name("mic_10")
        self.ex_destination_quodlit2 = self.data_set.get_mic_by_name("mic_11")
        self.ex_destination_quoddkp1 = self.data_set.get_mic_by_name("mic_14")
        self.ex_destination_quoddkp2 = self.data_set.get_mic_by_name("mic_15")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_qdl1 = self.data_set.get_listing_id_by_name("listing_4")
        self.listing_id_qdl2 = self.data_set.get_listing_id_by_name("listing_5")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_ER_eliminate_or_cancel_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_2_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quoddkp1, False, self.traded_qty, self.dark_price)
        nos_2_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quoddkp2, False, self.traded_qty, self.dark_price)
        nos_3_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, True, self.qty_for_md,  self.price_bid)
        nos_4_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit2, True, self.qty_for_md, self.price_bid)
        self.rule_list = [nos_1_ioc_rule, nos_2_ioc_rule, nos_3_ioc_rule, nos_4_ioc_rule]
        # endregion

        now = datetime.today() - timedelta(hours=3)

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        market_data_snap_shot_qdl1 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        market_data_snap_shot_qdl2 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for SORPING order
        case_id_1 = bca.create_event("Create SORPING Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.SORPING_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_SORPING_params()
        self.SORPING_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.SORPING_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Side=self.sell, ClientAlgoPolicyID=self.algopolicy))

        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.SORPING_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
