import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo


# Warning! This is the manual test case. It needs to do manual and doesn`t include in regression script
class QAP_T4079(TestCase):
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
        self.dec_qty = 500
        self.price = 45
        self.qty_for_md = 1000
        self.price_ask = 40
        self.price_bid = 30
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel_replace = Status.CancelReplace
        self.status_fill = Status.Fill
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
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, self.price)
        self.rule_list = [nos_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for SORPING order
        case_id_1 = bca.create_event("Create Multilisted order and replace it", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        # region Payload
        self.Multilisted_order_1 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_Kepler_params()
        self.Multilisted_order_1.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Multilisted_order_1.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))

        self.Multilisted_order_2 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_Kepler_params()
        self.Multilisted_order_2.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Multilisted_order_2.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))

        self.Multilisted_order_3 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_Kepler_params()
        self.Multilisted_order_3.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Multilisted_order_3.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))

        self.Multilisted_order_4 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_Kepler_params()
        self.Multilisted_order_4.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Multilisted_order_4.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))

        self.Multilisted_order_5 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_Kepler_params()
        self.Multilisted_order_5.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Multilisted_order_5.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))

        self.Multilisted_order_6 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_Kepler_params()
        self.Multilisted_order_6.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Multilisted_order_6.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))

        self.Multilisted_order_7 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_Kepler_params()
        self.Multilisted_order_7.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Multilisted_order_7.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))

        self.Multilisted_order_8 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_Kepler_params()
        self.Multilisted_order_8.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Multilisted_order_8.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))

        self.Multilisted_order_9 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_Kepler_params()
        self.Multilisted_order_9.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Multilisted_order_9.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))

        self.Multilisted_order_10 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_Kepler_params()
        self.Multilisted_order_10.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Multilisted_order_10.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        # endregion

        self.Multilisted_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_Kepler_params()
        self.Multilisted_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Multilisted_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))

        self.Multilisted_order_replace_params = FixMessageOrderCancelReplaceRequestAlgo(self.Multilisted_order)
        self.Multilisted_order_replace_params.change_parameters(dict(OrderQty=self.dec_qty))

        self.fix_manager_sell.send_message(self.Multilisted_order_1)
        self.fix_manager_sell.send_message(self.Multilisted_order_2)
        self.fix_manager_sell.send_message(self.Multilisted_order_3)
        self.fix_manager_sell.send_message(self.Multilisted_order_4)
        self.fix_manager_sell.send_message(self.Multilisted_order_5)
        self.fix_manager_sell.send_message(self.Multilisted_order_6)
        self.fix_manager_sell.send_message(self.Multilisted_order_7)
        self.fix_manager_sell.send_message(self.Multilisted_order_8)
        self.fix_manager_sell.send_message(self.Multilisted_order_9)
        self.fix_manager_sell.send_message(self.Multilisted_order_10)

        self.fix_manager_sell.send_message_and_receive_response(self.Multilisted_order, case_id_1)
        self.fix_manager_sell.send_message_and_receive_response(self.Multilisted_order_replace_params, case_id_1)

        time.sleep(1)

        self.fix_verifier_sell.check_fix_message(self.Multilisted_order_replace_params, direction=self.ToQuod, message_name='Sell side OrderCancelReplaceRequest')
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.Multilisted_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_Multilisted_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Multilisted_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_Multilisted_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_Multilisted_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Multilisted_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_Multilisted_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')

        er_replaced_Multilisted_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.Multilisted_order_replace_params, self.gateway_side_sell, self.status_cancel_replace)
        self.fix_verifier_sell.check_fix_message(er_replaced_Multilisted_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell Side ExecReport Replace Request')
        # endregion

        # TODO Need edit

        # region Check Lit child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit child DMA order", self.test_id))

        self.dma_qdl1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_qdl1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, OrderQty=self.qty, Price=self.price))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_qdl1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl1_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_qdl1_order_params.change_parameters(dict(ExDestination=self.ex_destination_quodlit1))
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl1_order, self.gateway_side_buy, self.status_new)
        er_new_dma_qdl1_order_params.change_parameters(dict(ExDestination=self.ex_destination_quodlit1))
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        # region check cancel dma child order
        er_cancel_dma_qdl1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qdl1_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_qdl1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel Passive child DMA 2 order")
        # endregion

        # region check cancel parent algo order
        er_cancel_Multilisted_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Multilisted_order, self.gateway_side_sell, self.status_fill)
        self.fix_verifier_sell.check_fix_message(er_cancel_Multilisted_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
