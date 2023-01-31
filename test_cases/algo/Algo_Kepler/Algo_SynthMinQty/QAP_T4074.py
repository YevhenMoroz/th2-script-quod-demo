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
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T4074(TestCase):
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
        self.qty = 250
        self.min_qty = 200
        self.trade_qty = 200
        self.leaves_qty = 0
        self.price = 11
        self.qty_2_child = 50
        self.price_ask = 40
        self.price_bid = 11
        self.passive_price = 10
        self.qty_bid = 200
        self.qty_ask = 1000000
        self.delay = 1000
        self.tif_fok = constants.TimeInForce.FillOrKill.value
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_fill = Status.Fill
        self.status_partial_fill = Status.PartialFill
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
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_qdl1 = self.data_set.get_listing_id_by_name("listing_4")
        self.listing_id_qdl2 = self.data_set.get_listing_id_by_name("listing_5")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_ER_fill_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_Reject_Eliminate_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        # The delay parameter needs for updating MD in time
        nos_fok_rule = rule_manager.add_NewOrdSingle_FOK(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, True, self.price, self.delay)
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit2, True, self.qty_2_child, self.price)
        self.rule_list = [nos_fok_rule, nos_ioc_rule]
        # endregion

        now = datetime.today() - timedelta(hours=3)

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for synthMinQty_order order
        case_id_1 = bca.create_event("Create synthMinQty_order Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.synthMinQty_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_SynthMinQty_params()
        self.synthMinQty_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.synthMinQty_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, MinQty=self.min_qty))

        self.fix_manager_sell.send_message_and_receive_response(self.synthMinQty_order, case_id_1)

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.passive_price, MDEntrySize=self.qty_bid)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)
        # endregion

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.synthMinQty_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_synthMinQty_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.synthMinQty_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_synthMinQty_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_synthMinQty_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.synthMinQty_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_synthMinQty_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check 1 child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Phase 1: Aggressive child DMA order", self.test_id))

        self.dma_qdl1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_ChildMinQty_params()
        self.dma_qdl1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, OrderQty=self.trade_qty, Price=self.price, TimeInForce=self.tif_fok))
        self.fix_verifier_buy.check_fix_message(self.dma_qdl1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Aggressive Child DMA 1 order')

        er_pending_new_dma_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Aggressive Child DMA 1 order')

        er_new_dma_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl1_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Aggressive Child DMA 1 order')
        # endregion

        # region Check Fill
        self.fix_verifier_buy.set_case_id(bca.create_event("Fill 1 child Order", self.test_id))

        # region check fill first dma child order
        er_fill_dma_qdl1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl1_order, self.gateway_side_buy, self.status_fill)
        er_fill_dma_qdl1_order.change_parameters(dict(CumQty=self.trade_qty, LeavesQty=0, LastQty=self.trade_qty, LastPx=self.price))
        self.fix_verifier_buy.check_fix_message(er_fill_dma_qdl1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Fill Aggressive DMA 1 order")
        # endregion

        # region Check 2 child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Phase 2: Aggressive child DMA order", self.test_id))

        self.dma_qdl2_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_ChildMinQty_params()
        self.dma_qdl2_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit2, OrderQty=self.qty_2_child, Price=self.price, TimeInForce=self.tif_ioc))
        self.fix_verifier_buy.check_fix_message(self.dma_qdl2_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Aggressive Child DMA 2 order')

        er_pending_new_dma_qdl2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl2_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_qdl2_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Aggressive Child DMA 2 order')

        er_new_dma_qdl2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl2_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_qdl2_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Aggressive Child DMA 2 order')
        # endregion

        # region Check Fill
        self.fix_verifier_buy.set_case_id(bca.create_event("Fill 2 child Order", self.test_id))

        # region check fill second dma child order
        er_fill_dma_qdl2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl2_order, self.gateway_side_buy, self.status_fill)
        er_fill_dma_qdl2_order.change_parameters(dict(CumQty=self.qty_2_child, LeavesQty=0, LastQty=self.qty_2_child, LastPx=self.price))
        self.fix_verifier_buy.check_fix_message(er_fill_dma_qdl2_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Fill Aggressive DMA 2 order")
        # endregion

        time.sleep(1)

        self.fix_verifier_sell.set_case_id(bca.create_event("Fill Algo Order", self.test_id))
        er_fill_synthMinQty_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.synthMinQty_order, self.gateway_side_sell, self.status_fill)
        er_fill_synthMinQty_order.change_parameters(dict(LastPx=self.price, CumQty=self.qty, LeavesQty=self.leaves_qty, LastQty=self.qty_2_child))
        self.fix_verifier_sell.check_fix_message(er_fill_synthMinQty_order, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Fill')
        # endregion

        time.sleep(3)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
