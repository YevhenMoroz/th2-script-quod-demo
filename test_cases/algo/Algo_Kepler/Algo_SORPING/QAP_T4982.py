import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T4982(TestCase):
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
        self.qty = 200
        self.price = 38
        self.inc_price = 39
        self.display_qty = 50
        self.dark_price = 30
        self.traded_qty = 0
        self.qty_for_md = 1000
        self.price_ask = 44
        self.price_bid = 30
        self.px_for_incr = 0
        self.qty_for_incr = 0
        self.tif_iok = constants.TimeInForce.ImmediateOrCancel.value
        self.algopolicy = constants.ClientAlgoPolicy.qa_sorping_5.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_eliminate = Status.Eliminate
        self.status_cancel_replace = Status.CancelReplace
        self.status_cancel = Status.Cancel
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_9")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_par = self.data_set.get_mic_by_name("mic_1")
        self.ex_destination_batsdark = self.data_set.get_mic_by_name("mic_4")
        self.ex_destination_chixdark = self.data_set.get_mic_by_name("mic_5")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.account_chixdark = self.data_set.get_account_by_name("account_8")
        self.account_batsdark = self.data_set.get_account_by_name("account_7")
        self.listing_id_par = self.data_set.get_listing_id_by_name("listing_6")
        self.listing_id_trqx = self.data_set.get_listing_id_by_name("listing_15")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_ER_eliminate_or_cancel_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_2_child")
        # endregion

        self.pre_filter = self.data_set.get_pre_filter("pre_filer_equal_ER_canceled")
        self.pre_filter['ExDestination'] = (self.ex_destination_par, "EQUAL")

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager()
        nos_1_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account_batsdark, self.ex_destination_batsdark, False, self.traded_qty, self.dark_price)
        nos_2_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account_chixdark, self.ex_destination_chixdark, False, self.traded_qty, self.dark_price)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_par, self.price)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_par, self.inc_price)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_par, True)
        self.rule_list = [nos_1_ioc_rule, nos_2_ioc_rule, nos_1_rule, nos_2_rule, ocr_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        market_data_snap_shot_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_trqx = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_trqx)

        market_data_snap_shot_trqx = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_trqx)
        # endregion

        # region Send NewOrderSingle (35=D) for SORPING order
        case_id_1 = bca.create_event("Create SORPING Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.SORPING_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_SORPING_params()
        self.SORPING_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.SORPING_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ClientAlgoPolicyID=self.algopolicy)).add_tag(dict(DisplayInstruction=dict(DisplayQty=self.display_qty)))

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

        # region Check dark childs
        self.fix_verifier_buy.set_case_id(bca.create_event("Dark child DMA orders", self.test_id))

        # region Check child DMA order on venue CHIX DARK
        self.dma_chixdark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_params()
        self.dma_chixdark_order.change_parameters(dict(Account=self.account_chixdark, ExDestination=self.ex_destination_chixdark, OrderQty=self.qty, Price=self.dark_price, Instrument=self.instrument, TimeInForce=self.tif_iok))
        self.fix_verifier_buy.check_fix_message(self.dma_chixdark_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        time.sleep(2)

        er_eliminate_dma_chixdark_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chixdark_order, self.gateway_side_buy, self.status_eliminate)
        self.fix_verifier_buy.check_fix_message(er_eliminate_dma_chixdark_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Eliminate child DMA 1 order")
        # endregion

        # region Check child DMA order on venue BATS DARK
        self.dma_batsdark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_params()
        self.dma_batsdark_order.change_parameters(dict(Account=self.account_batsdark, ExDestination=self.ex_destination_batsdark, OrderQty=self.qty, Price=self.dark_price, Instrument=self.instrument, TimeInForce=self.tif_iok))
        self.fix_verifier_buy.check_fix_message(self.dma_batsdark_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 2 order')

        er_eliminate_dma_batsdark_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_batsdark_order, self.gateway_side_buy, self.status_eliminate)
        self.fix_verifier_buy.check_fix_message(er_eliminate_dma_batsdark_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Eliminate child DMA 2 order")
        # endregion
        # endregion

        # region Check Lit child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit child DMA order", self.test_id))

        self.dma_1_xpar_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_params()
        self.dma_1_xpar_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_par, OrderQty=self.display_qty, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(self.dma_1_xpar_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_1_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_xpar_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_1_xpar_order_params.change_parameters(dict(ExDestination=self.ex_destination_par))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_1_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_1_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_xpar_order, self.gateway_side_buy, self.status_new)
        er_new_dma_1_xpar_order_params.change_parameters(dict(ExDestination=self.ex_destination_par))
        self.fix_verifier_buy.check_fix_message(er_new_dma_1_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        time.sleep(5)

        # region Modify parent LitDark order
        case_id_2 = bca.create_event("Replace LitDark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)

        self.SORPING_order_replace_params = FixMessageOrderCancelReplaceRequestAlgo(self.SORPING_order)
        self.SORPING_order_replace_params.change_parameters(dict(Price=self.inc_price))
        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_order_replace_params, case_id_2)

        time.sleep(1)

        self.fix_verifier_sell.check_fix_message(self.SORPING_order_replace_params, direction=self.ToQuod, message_name='Sell side OrderCancelReplaceRequest')

        er_replaced_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.SORPING_order_replace_params, self.gateway_side_sell, self.status_cancel_replace)
        self.fix_verifier_sell.check_fix_message(er_replaced_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell Side ExecReport Replace Request')
        # endregion

        time.sleep(2)

        # region check cancel dma child order
        self.er_cancel_dma_1_xpar_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_xpar_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(self.er_cancel_dma_1_xpar_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 1 order")
        # endregion

        # region Check new Lit child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit child DMA order", self.test_id))

        self.dma_2_xpar_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_params()
        self.dma_2_xpar_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_par, OrderQty=self.display_qty, Price=self.inc_price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(self.dma_2_xpar_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 2 order')

        er_pending_new_dma_2_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_xpar_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_2_xpar_order_params.change_parameters(dict(ExDestination=self.ex_destination_par))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_2_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_2_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_xpar_order, self.gateway_side_buy, self.status_new)
        er_new_dma_2_xpar_order_params.change_parameters(dict(ExDestination=self.ex_destination_par))
        self.fix_verifier_buy.check_fix_message(er_new_dma_2_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        time.sleep(5)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_SORPING_order = FixMessageOrderCancelRequest(self.SORPING_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_SORPING_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_SORPING_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel new dma child order
        self.er_cancel_dma_2_xpar_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_xpar_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(self.er_cancel_dma_2_xpar_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 2 order")
        # endregion

        time.sleep(10)

        self.fix_verifier_buy.set_case_id(bca.create_event("Check that 2 DMA orders on qdl6 was canceled", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([self.er_cancel_dma_1_xpar_order, self.er_cancel_dma_2_xpar_order], key_parameters_list=[None, None], direction=self.ToQuod, pre_filter=self.pre_filter)

        er_cancel_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.SORPING_order_replace_params, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager()
        rule_manager.remove_rules(self.rule_list)
