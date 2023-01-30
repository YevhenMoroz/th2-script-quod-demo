import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.algo_formulas_manager import AlgoFormulasManager
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


class QAP_T10393(TestCase):
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
        self.qty = 1500
        self.aggressive_child_qty = 500
        self.aggressive_1st_child_traded_qty = 400
        self.aggressive_2nd_child_traded_qty = 100
        self.passive_child_qty = 1000
        self.price = 45
        self.traded_qty = 0
        self.qty_for_md = 500
        self.price_ask_qdl1 = 44
        self.price_bid = 30
        self.price_ask_qdl2 = 50
        self.price_ask_qdl3 = 50
        self.delay = 0
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.tif_gtd = constants.TimeInForce.GoodTillDate.value
        self.algopolicy = constants.ClientAlgoPolicy.qa_sorping_4.value

        now = datetime.today()
        expire_date = (now + timedelta(days=2))
        self.ExpireDate_for_sending = (now + timedelta(days=2)).strftime("%Y%m%d")
        shift = AlgoFormulasManager.make_expire_date_friday_if_it_is_on_weekend(expire_date)
        self.ExpireDate = (expire_date - timedelta(days=shift)).strftime("%Y%m%d")
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_partial_fill = Status.PartialFill
        self.status_eliminate = Status.Eliminate
        self.status_fill = Status.Fill
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
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, self.price)
        nos_trade_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, self.price, self.price, self.passive_child_qty, self.passive_child_qty, self.delay)
        nos_ioc_1_rule = rule_manager.add_NewOrdSingle_IOCTradeByOrderQty(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, True, self.price_ask_qdl1, self.price_ask_qdl1, self.aggressive_child_qty, self.aggressive_1st_child_traded_qty)
        nos_ioc_2_rule = rule_manager.add_NewOrdSingle_IOCTradeByOrderQty(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, True, self.price_ask_qdl1, self.price_ask_qdl1, self.aggressive_2nd_child_traded_qty, self.aggressive_2nd_child_traded_qty)
        self.rule_list = [nos_rule, nos_trade_rule, nos_ioc_1_rule, nos_ioc_2_rule]
        # endregion

        # region Send_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl1, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        market_data_snap_shot_qdl2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl2, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for SORPING order
        case_id_1 = bca.create_event("Create SORPING Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.SORPING_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_SORPING_params()
        self.SORPING_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.SORPING_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, ClientAlgoPolicyID=self.algopolicy, Instrument=self.instrument, TimeInForce=self.tif_gtd)).add_tag(dict(ExpireDate=self.ExpireDate))

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

        # region Check Lit aggressive child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit 1st aggressive child DMA order", self.test_id))

        self.dma_1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_params()
        self.dma_1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, OrderQty=self.aggressive_child_qty, Price=self.price_ask_qdl1, TimeInForce=self.tif_ioc))
        self.fix_verifier_buy.check_fix_message(self.dma_1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Aggressive Child DMA 1 order')

        er_pending_new_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Pending new Aggressive child DMA 1 order")

        er_new_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport New Aggressive child DMA 1 order")

        er_partialy_fill_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_partial_fill)
        self.fix_verifier_buy.check_fix_message(er_partialy_fill_dma_1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport PartialFill Aggressive child DMA 1 order")

        er_eliminate_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_eliminate)
        self.fix_verifier_buy.check_fix_message(er_eliminate_dma_1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Eliminate Aggressive child DMA 1 order")
        # endregion

        # region Check Lit passive child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit passive child DMA order", self.test_id))

        self.dma_2_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_params()
        self.dma_2_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, OrderQty=self.passive_child_qty, Price=self.price))
        self.fix_verifier_buy.check_fix_message(self.dma_2_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Passive Child DMA 2 order')

        er_pending_new_dma_2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_2_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Pending new Passive child DMA 2 order")

        er_new_dma_2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_2_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport New Passive child DMA 2 order")

        er_fill_dma_2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(er_fill_dma_2_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Fill Passive child DMA 2 order")
        # endregion

        time.sleep(2)

        # region Check Lit aggressive child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit 2nd aggressive child DMA order (sweeping)", self.test_id))

        self.dma_3_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_params()
        self.dma_3_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, OrderQty=self.aggressive_2nd_child_traded_qty, Price=self.price_ask_qdl1, TimeInForce=self.tif_ioc))
        self.fix_verifier_buy.check_fix_message(self.dma_3_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Aggressive Child DMA 3 order')

        er_pending_new_dma_3_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_3_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Pending new Aggressive child DMA 3 order")

        er_new_dma_3_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_3_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport New Aggressive child DMA 3 order")

        er_fill_dma_3_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(er_fill_dma_3_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Fill Aggressive child DMA 3 order")
        # endregion

        time.sleep(15)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
