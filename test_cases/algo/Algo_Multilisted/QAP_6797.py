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
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.algo_formulas_manager import AlgoFormulasManager
from test_framework.core.test_case import TestCase


class QAP_6797(TestCase):
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
        self.qty = 150
        self.price = 17
        self.qty_agr_child = 100
        self.price_agr_child = 15
        self.traded_qty = 0
        self.qty_passive_child = 25
        self.price_ask_trqx = 20
        self.price_ask_paris = 15
        self.price_bid = 14.95
        self.qty_ask_trqx = 100
        self.qty_ask_paris = 100
        self.qty_bid = 100
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_eliminate = Status.Eliminate
        self.status_cancel = Status.Cancel
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
        self.ex_destination_trqx = self.data_set.get_mic_by_name("mic_2")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account_xpar = self.data_set.get_account_by_name("account_2")
        self.account_trqx = self.data_set.get_account_by_name("account_5")
        self.listing_id_par = self.data_set.get_listing_id_by_name("listing_2")
        self.listing_id_trqx = self.data_set.get_listing_id_by_name("listing_3")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        # rule_manager = RuleManager()
        # nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, False, self.traded_qty, self.price_agr_child)
        # nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, self.price)
        # nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, self.price)
        # ocr_1_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, True)
        # ocr_2_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, True)
        # self.rule_list = [nos_ioc_rule, nos_1_rule, nos_2_rule, ocr_1_rule, ocr_2_rule]
        # # endregion

        now = datetime.today() - timedelta(hours=3)

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
        self.multilisting_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))

        self.fix_manager_sell.send_message_and_receive_response(self.multilisting_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.multilisting_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_multilisting_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_multilisting_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Aggressive Child DMA order", self.test_id))

        dma_1_xpar_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        dma_1_xpar_order.change_parameters(dict(Account=self.account_xpar, ExDestination=self.ex_destination_xpar, OrderQty=self.qty_agr_child, Price=self.price_agr_child, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(dma_1_xpar_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_1_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_xpar_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_1_xpar_order_params.change_parameters(dict(ExDestination=self.ex_destination_xpar))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_1_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_1_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_xpar_order, self.gateway_side_buy, self.status_pending)
        er_new_dma_1_xpar_order_params.change_parameters(dict(ExDestination=self.ex_destination_xpar))
        self.fix_verifier_buy.check_fix_message(er_new_dma_1_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        # region check eliminate first dma child order
        er_eliminate_dma_1_xpar_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_xpar_order, self.gateway_side_buy, self.status_eliminate)
        self.fix_verifier_buy.check_fix_message(er_eliminate_dma_1_xpar_order, self.key_params_ER_parent, self.ToQuod, "Buy Side ExecReport Cancel first DMA 1 order")
        # endregion

        # region Check passive DMA orders
        self.fix_verifier_buy.set_case_id(bca.create_event("Passive Child DMA orders", self.test_id))

        self.dma_1_trqx_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_1_trqx_order.change_parameters(dict(Account=self.account_trqx, ExDestination=self.ex_destination_trqx, OrderQty=self.qty_passive_child, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(self.dma_1_trqx_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 2 order')

        er_pending_new_dma_1_trqx_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_trqx_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_1_trqx_order_params.change_parameters(dict(ExDestination=self.ex_destination_trqx))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_1_trqx_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 2 order')

        er_new_dma_1_trqx_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_trqx_order, self.gateway_side_buy, self.status_pending)
        er_new_dma_1_trqx_order_params.change_parameters(dict(ExDestination=self.ex_destination_trqx))
        self.fix_verifier_buy.check_fix_message(er_new_dma_1_trqx_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 2 order')

        self.dma_2_xpar_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_2_xpar_order.change_parameters(dict(Account=self.account_xpar, ExDestination=self.ex_destination_xpar, OrderQty=self.qty_passive_child, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(self.dma_2_xpar_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 3 order')

        er_pending_new_dma_2_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_xpar_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_2_xpar_order_params.change_parameters(dict(ExDestination=self.ex_destination_xpar))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_2_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 3 order')

        er_new_dma_2_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_xpar_order, self.gateway_side_buy, self.status_pending)
        er_new_dma_2_xpar_order_params.change_parameters(dict(ExDestination=self.ex_destination_xpar))
        self.fix_verifier_buy.check_fix_message(er_new_dma_2_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 3 order')
        # endregion

        time.sleep(1)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        # case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        # self.fix_verifier_sell.set_case_id(case_id_3)
        # cancel_request_multilisting_order = FixMessageOrderCancelRequest(self.multilisting_order)
        #
        # self.fix_manager_sell.send_message_and_receive_response(cancel_request_multilisting_order, case_id_3)
        # self.fix_verifier_sell.check_fix_message(cancel_request_multilisting_order, direction=self.ToQuod, message_name='Sell side Cancel Request')
        #
        # # region check cancel second dma child order
        # er_cancel_dma_1_trqx_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_trqx_order, self.gateway_side_buy, self.status_cancel)
        # self.fix_verifier_buy.check_fix_message(er_cancel_dma_1_trqx_order, self.key_params_ER_parent, self.ToQuod, "Buy Side ExecReport Cancel child DMA 2 order")
        # # endregion
        #
        # # region check cancel second dma child order
        # er_cancel_dma_2_xpar_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_xpar_order, self.gateway_side_buy, self.status_cancel)
        # self.fix_verifier_buy.check_fix_message(er_cancel_dma_2_xpar_order, self.key_params_ER_parent, self.ToQuod, "Buy Side ExecReport Cancel child DMA 3 order")
        # # endregion
        #
        # cancel_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_cancel)
        # self.fix_verifier_sell.check_fix_message(cancel_multilisting_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # # endregion

        RuleManager.remove_rules(self.rule_list)