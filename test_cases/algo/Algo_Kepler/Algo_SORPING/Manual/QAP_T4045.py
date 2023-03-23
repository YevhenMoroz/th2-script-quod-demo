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
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


# Warning! This is the manual test case. It needs to do manual and doesn`t include in regression script
class QAP_T4045(TestCase):
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
        self.price = 4
        self.price_ask_1 = 3.5
        self.price_ask_2 = 3
        self.price_bid = 2.9
        self.side = constants.OrderSide.Buy.value
        self.qty_bid = self.qty_ask = 1000000
        self.algopolicy = constants.ClientAlgoPolicy.qa_sorping_4.value
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
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_14")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_citadel = self.data_set.get_mic_by_name("mic_23")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_citadel = self.data_set.get_listing_id_by_name("listing_14")
        self.listing_id_janestreet = self.data_set.get_listing_id_by_name("listing_13")
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
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_citadel, True, self.qty, self.price_ask_2)
        self.rule_list = [nos_ioc_rule]
        # endregion

        # region Send_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_citadel = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_citadel, self.fix_env1.feed_handler)
        market_data_snap_shot_citadel.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_citadel.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_1, MDEntrySize=self.qty_ask)
        market_data_snap_shot_citadel.add_fields_into_repeating_group('NoMDEntries', [dict(MDEntryType=1, MDEntryPx=self.price_ask_2, MDEntrySize=self.qty_ask, MDEntryPositionNo=2)])
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_citadel)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_janestreet = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_janestreet, self.fix_env1.feed_handler)
        market_data_snap_shot_janestreet.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_janestreet.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_1, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_janestreet)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for SynthMinQty order
        case_id_1 = bca.create_event("Create SORPING LitDark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.SORPING_LitDark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_Kepler_params()
        self.SORPING_LitDark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.SORPING_LitDark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, Side=self.side, ClientAlgoPolicyID=self.algopolicy))

        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_LitDark_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.SORPING_LitDark_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_SORPING_LitDark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_LitDark_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_SORPING_LitDark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_SORPING_LitDark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_LitDark_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_SORPING_LitDark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.dma_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_Multiple_Emulation_Kepler_params()
        self.dma_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_citadel, OrderQty=self.qty, Price=self.price_ask_2, Instrument=self.instrument, Side=self.side, TimeInForce=self.tif_ioc))
        self.fix_verifier_buy.check_fix_message(self.dma_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        # region Check Fill
        # region check fill dma child order
        er_fill_dma_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(er_fill_dma_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Fill child DMA 1 order")
        # endregion

        # region Check Fill algo order
        er_fill_SORPING_LitDark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_LitDark_order, self.gateway_side_sell, self.status_fill)
        self.fix_verifier_sell.check_fix_message(er_fill_SORPING_LitDark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Fill')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)



