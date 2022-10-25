import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T8432(TestCase):
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
        self.qty = 100
        self.price = 45
        self.traded_qty = 0
        self.price_ask_trqx = 50
        self.price_ask_paris = 40
        self.price_bid = 14.95
        self.qty_ask_trqx = 100
        self.qty_ask_paris = 100
        self.qty_bid = 100
        self.tif_fok = constants.TimeInForce.FillOrKill.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_eliminate = Status.Eliminate
        self.status_fill = Status.Fill
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_5")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_xpar = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account_xpar = self.data_set.get_account_by_name("account_2")
        self.listing_id_par = self.data_set.get_listing_id_by_name("listing_2")
        self.listing_id_trqx = self.data_set.get_listing_id_by_name("listing_3")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_ER_eliminate_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_2_Eliminate_child")
        # endregion

        self.pre_filter_1 = self.data_set.get_pre_filter("pre_filer_equal_D")

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        self.nos_fok_1_rule = rule_manager.add_NewOrdSingle_FOK(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, False, self.price_ask_paris, 4000)
        # endregion

        # region Send_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_paris, MDEntrySize=self.qty_ask_paris)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_trqx = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_trqx, MDEntrySize=self.qty_ask_trqx)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_trqx)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for Multilisting order
        case_id_1 = bca.create_event("Create Multilisting Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.multilisting_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_params()
        self.multilisting_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.multilisting_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, TimeInForce=self.tif_fok))

        self.fix_manager_sell.send_message_and_receive_response(self.multilisting_order, case_id_1)

        time.sleep(2)

        rule_manager.remove_rule(self.nos_fok_1_rule)
        nos_fok_2_rule = rule_manager.add_NewOrdSingle_FOK(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, True, self.price_ask_paris, 5000)
        self.rule_list = [nos_fok_2_rule]
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.multilisting_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_multilisting_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_multilisting_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region 1st child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Aggressive Child DMA order", self.test_id))

        dma_1_xpar_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        dma_1_xpar_order.change_parameters(dict(Account=self.account_xpar, ExDestination=self.ex_destination_xpar, OrderQty=self.qty, Price=self.price_ask_paris, Instrument=self.instrument, TimeInForce=self.tif_fok))

        er_pending_new_dma_1_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_xpar_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_1_xpar_order_params.change_parameters(dict(ExDestination=self.ex_destination_xpar))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_1_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Passive Child DMA 2 order')

        er_new_dma_1_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_xpar_order, self.gateway_side_buy, self.status_pending)
        er_new_dma_1_xpar_order_params.change_parameters(dict(ExDestination=self.ex_destination_xpar))
        self.fix_verifier_buy.check_fix_message(er_new_dma_1_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Passive Child DMA 2 order')

        er_eliminate_dma_1_xpar_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_xpar_order, self.gateway_side_buy, self.status_eliminate)
        self.fix_verifier_buy.check_fix_message(er_eliminate_dma_1_xpar_order, self.key_params_ER_eliminate_child, self.ToQuod, "Buy Side ExecReport Eliminate Aggressive Child DMA 1 order")
        # endregion
        
        # region Check 2nd child DMA order
        dma_2_xpar_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        dma_2_xpar_order.change_parameters(dict(Account=self.account_xpar, ExDestination=self.ex_destination_xpar, OrderQty=self.qty, Price=self.price_ask_paris, Instrument=self.instrument, TimeInForce=self.tif_fok))

        er_pending_new_dma_2_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_2_xpar_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_2_xpar_order_params.change_parameters(dict(ExDestination=self.ex_destination_xpar))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_2_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Passive Child DMA 2 order')

        er_new_dma_2_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_2_xpar_order, self.gateway_side_buy, self.status_pending)
        er_new_dma_2_xpar_order_params.change_parameters(dict(ExDestination=self.ex_destination_xpar))
        self.fix_verifier_buy.check_fix_message(er_new_dma_2_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Passive Child DMA 2 order')

        time.sleep(5)

        er_fill_dma_2_xpar_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_2_xpar_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(er_fill_dma_2_xpar_order, self.key_params_ER_eliminate_child, self.ToQuod, "Buy Side ExecReport Fill Aggressive Child DMA 1 order")
        # endregion

        # region Check Fill Multilisted algo order
        er_fill_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_fill)
        self.fix_verifier_sell.check_fix_message(er_fill_multilisting_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Fill')
        # endregion

        # region Check there are no any new child orders after the full fill parent order
        self.fix_verifier_buy.set_case_id(bca.create_event("Check there are no new childs after terminated parent algo order", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([dma_1_xpar_order, dma_2_xpar_order], key_parameters_list=[None, None], direction=self.FromQuod, pre_filter=self.pre_filter_1)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)