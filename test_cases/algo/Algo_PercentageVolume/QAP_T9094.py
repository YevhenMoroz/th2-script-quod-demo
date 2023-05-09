import os
import time

from pathlib import Path

from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, TimeInForce, StrategyParameterType
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager


class QAP_T9094(TestCase):
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
        self.restapi_env1 = self.environment.get_list_web_admin_rest_api_environment()[0]
        # endregion

        # region order parameters
        self.qty = 1_000_000
        self.price = 30
        self.price_bid = 30
        self.price_ask = 40
        self.qty_bid = self.qty_ask = 1_000_000
        self.indicative_volume = 1_000
        self.indicative_price = 100
        self.pct = 0.1
        self.tif_day = TimeInForce.Day.value
        self.pass_child_qty = AFM.get_pov_child_qty(self.pct, self.qty_bid, self.qty)
        self.float_type = StrategyParameterType.Float.value
        self.dateformat = "time_only"
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
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_2")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.s_par = self.data_set.get_listing_id_by_name("listing_1")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile4")

        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_bid)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [nos_rule, ocr_rule]
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phases = AFM.get_timestamps_for_current_phase(TradingPhases.PreOpen, self.dateformat)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        time.sleep(5)

        # region Send MarketData LTQ PRE
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send Trading Phase PreOpen Auction", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume).update_MDReqID(self.s_par, self.fix_env1.feed_handler).set_phase(TradingPhases.PreOpen)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        # region Send MarketData Book
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot)
        # endregion

        time.sleep(3)

        # region Send NewOrderSingle (35=D) for POV order
        case_id_1 = bca.create_event("Create POV Auction Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.POV_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_params()
        self.POV_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.POV_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Instrument=self.instrument, ExDestination=self.ex_destination_1, Price=self.price))
        self.POV_order.update_repeating_group("NoStrategyParameters", [dict(StrategyParameterName='PercentageVolume', StrategyParameterType=self.float_type, StrategyParameterValue=self.pct)])
        self.fix_manager_sell.send_message_and_receive_response(self.POV_order, case_id_1)

        time.sleep(3)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.POV_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_POV_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_POV_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion
        
        time.sleep(240)

        # region Send MarketData LTQ Open
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send Trading Phase Open", self.test_id))
        market_data_incr_xpar = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incr_xpar.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price, MDEntrySize=self.indicative_volume)
        self.fix_manager_feed_handler.send_message(market_data_incr_xpar)
        # endregion

        time.sleep(10)
                
        # region Check child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))
        self.dma_1_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_1, OrderQty=self.pass_child_qty, Price=self.price_bid, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(self.dma_1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_dma_1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')

        # region Check that only one child DMA order was generated
        self.fix_verifier_buy.set_case_id(bca.create_event("Check that only one child DMA order was generated", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([self.dma_1_order], [self.key_params_ER_child], self.FromQuod)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        cancel_request_POV_order = FixMessageOrderCancelRequest(self.POV_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_POV_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_POV_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(3)

        cancel_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_POV_order_params, key_parameters=self.key_params_ER_child, message_name='Sell side ExecReport Cancel')
        # endregion

        # region check cancel dma child order
        cancel_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_dma_1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 1 order")
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase(self.dateformat)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
