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
from test_framework.algo_formulas_manager import AlgoFormulasManager

class QAP_T4945(TestCase):
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
        self.order_type = constants.OrderType.Limit.value
        self.qty = 200
        self.round_lot = 50
        self.waves = 4 # value assigned by the BE
        self.aggressivity = 3
        self.slice_duration = 1
        self.price_ask = 40
        self.price_bid = 30
        self.price = 1
        self.qty_bid = self.qty_ask = 1_000_000
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.tif_day = constants.TimeInForce.Day.value
        self.slice1_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves, self.round_lot)
        self.slice2_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves-1, self.round_lot)
        self.slice3_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves-2, self.round_lot)
        self.slice4_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves-3, self.round_lot)
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel_replace = Status.CancelReplace
        self.status_cancel = Status.Cancel
        self.status_eliminate = Status.Eliminate
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_28")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.s_par = self.data_set.get_listing_id_by_name("listing_50")
        # endregion

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.price)
        self.rule_list = [nos_ioc_rule]
        # endregion

        now = datetime.utcnow()
        start_time = now.strftime("%Y%m%d-%H:%M:%S")
        end_time = (now + timedelta(minutes=5)).strftime("%Y%m%d-%H:%M:%S")

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for TWAP order
        case_id_1 = bca.create_event("Create TWAP Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.twap_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_TWAP_params()
        self.twap_order.add_fields_into_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='StartDate', StrategyParameterType=19, StrategyParameterValue=start_time), dict(StrategyParameterName='EndDate', StrategyParameterType=19, StrategyParameterValue=end_time),
                                                                                 dict(StrategyParameterName='SliceDuration', StrategyParameterType='1', StrategyParameterValue=self.slice_duration), dict(StrategyParameterName='Aggressivity', StrategyParameterType='1', StrategyParameterValue=self.aggressivity)])
        self.twap_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.twap_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.fix_manager_sell.send_message_and_receive_response(self.twap_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        nos_twap_parent = self.twap_order.change_parameter('TransactTime', '*')
        self.fix_verifier_sell.check_fix_message(nos_twap_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_twap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_new)
        
        self.fix_verifier_sell.check_fix_message(new_twap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check child DMA order Slice 1
        slice1_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice1_order.change_parameters(dict(OrderQty=self.slice1_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_ioc))

        pending_slice1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_order, self.gateway_side_buy, self.status_pending)

        new_slice1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_order, self.gateway_side_buy, self.status_new)

        eliminate_slice1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_order, self.gateway_side_buy, self.status_eliminate)
        # endregion

        # region Check child DMA order Slice 2
        slice2_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice2_order.change_parameters(dict(OrderQty=self.slice2_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_ioc))

        pending_slice2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_order, self.gateway_side_buy, self.status_pending)

        new_slice2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_order, self.gateway_side_buy, self.status_new)

        eliminate_slice2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_order, self.gateway_side_buy, self.status_eliminate)
        # endregion

        # region Check child DMA order Slice 3
        slice3_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice3_order.change_parameters(dict(OrderQty=self.slice3_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_ioc))

        pending_slice3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice3_order, self.gateway_side_buy, self.status_pending)

        new_slice3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice3_order, self.gateway_side_buy, self.status_new)

        eliminate_slice3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice3_order, self.gateway_side_buy, self.status_eliminate)
        # endregion

        # region Check child DMA order Slice 4
        slice4_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice4_order.change_parameters(dict(OrderQty=self.slice4_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_ioc))

        pending_slice4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice4_order, self.gateway_side_buy, self.status_pending)

        new_slice4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice4_order, self.gateway_side_buy, self.status_new)

        eliminate_slice4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice4_order, self.gateway_side_buy, self.status_eliminate)
        # endregion

        time.sleep(300)

        # region Check that only 4 child orders are generated
        self.fix_verifier_buy.set_case_id(bca.create_event("Check sequence BuySide - Slice 1 - Slice 4", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([pending_slice1_order_params, new_slice1_order_params, eliminate_slice1_order_params,
                                                          pending_slice2_order_params, new_slice2_order_params, eliminate_slice2_order_params,
                                                          pending_slice3_order_params, new_slice3_order_params, eliminate_slice3_order_params,
                                                          pending_slice4_order_params, new_slice4_order_params, eliminate_slice4_order_params],
                                                         key_parameters_list=[None, None, None, None, None, None, None, None, None, None, None, None], direction=self.ToQuod,
                                                         pre_filter=None)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Eliminate Algo Order
        case_id_3 = bca.create_event("Eliminate Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        eliminate_twap_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_eliminate)
        eliminate_twap_order.change_parameters(dict(Text='reached end time'))
        self.fix_verifier_sell.check_fix_message(eliminate_twap_order, key_parameters=self.key_params_cl,  message_name='Sell side ExecReport Eliminated')
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
