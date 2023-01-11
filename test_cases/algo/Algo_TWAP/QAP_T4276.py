import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.algo_formulas_manager import AlgoFormulasManager
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
#TODO
# wating fixes for https://support.quodfinancial.com/jira/browse/PALGO-908 and https://support.quodfinancial.com/jira/browse/PALGO-813
class QAP_T4276(TestCase):
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
        self.qty = 10000
        self.price = self.price_ask = 40 # 10
        self.price_bid = 30 # 8
        self.mid_price = int((self.price_ask+self.price_bid)/2)
        self.qty_bid = self.qty_ask = 1_000_000
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.tif_day = constants.TimeInForce.Day.value
        self.waves = 5
        self.slice1_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves)
        self.slice2_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves-1)
        self.slice3_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves-2)
        self.slice4_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves-3)
        self.slice5_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves-4)
        # self.slice1_price = self.slice2_price = self.price_bid-self.tick_size
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_reject = Status.Reject
        self.status_new = Status.New
        self.status_cancel_replace = Status.CancelReplace
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
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.s_par = self.data_set.get_listing_id_by_name("listing_1")
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
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.mid_price) # _bid-self.tick_size
        # ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(self.fix_env1.buy_side, False)
        # ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [nos_rule, ocrr_rule]
        # endregion

        now = datetime.utcnow()
        start_time_init = (now + timedelta(minutes=1)).strftime("%Y%m%d-%H:%M:%S")
        end_time_init = (now + timedelta(minutes=6)).strftime("%Y%m%d-%H:%M:%S")
        start_time_mod = (now + timedelta(minutes=3)).strftime("%Y%m%d-%H:%M:%S")
        end_time_mod = (now + timedelta(minutes=8)).strftime("%Y%m%d-%H:%M:%S")

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
        self.twap_order.add_fields_into_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='StartDate', StrategyParameterType=19, StrategyParameterValue=start_time_init), dict(StrategyParameterName='EndDate', StrategyParameterType=19, StrategyParameterValue=end_time_init),
                                                                                 dict(StrategyParameterName='Waves', StrategyParameterType='1', StrategyParameterValue=self.waves)]) # , dict(StrategyParameterName='ChildMinValue', StrategyParameterType='6', StrategyParameterValue=self.child_min_val) dict(StrategyParameterName='Aggressivity', StrategyParameterType='1', StrategyParameterValue=self.aggressivity)
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
        new_twap_order_params.change_parameter('NoParty', '*')
        self.fix_verifier_sell.check_fix_message(new_twap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion
        
        # region Send OrderCancelReplace (35=G) for TWAP order
        case_id_2 = bca.create_event("Replace TWAP Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)

        self.twap_order_replace_params = FixMessageOrderCancelReplaceRequestAlgo(nos_twap_parent)
        self.twap_order_replace_params.update_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='StartDate', StrategyParameterType=19, StrategyParameterValue=start_time_mod),
                                                                  dict(StrategyParameterName='EndDate', StrategyParameterType=19, StrategyParameterValue=end_time_mod), dict(StrategyParameterName='Waves', StrategyParameterType='1', StrategyParameterValue=self.waves)])
        # self.twap_order.add_ClordId((os.path.basename(__file__)[:-3]))
        # self.twap_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.fix_manager_sell.send_message_and_receive_response(self.twap_order_replace_params, case_id_2)

        time.sleep(242)
        # endregion
        
        # region Check child DMA order Slice 1
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order - Slice 1", self.test_id))

        slice1_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice1_order.change_parameters(dict(OrderQty=self.slice1_qty, Price=self.mid_price, Instrument='*', TimeInForce=self.tif_day)) #slice1_
        self.fix_verifier_buy.check_fix_message(slice1_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice 1')

        pending_slice1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_slice1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice 1')

        new_slice1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_slice1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice 1')
        
        eliminate_slice1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_order, self.gateway_side_buy, self.status_eliminate)
        eliminate_slice1_order.change_parameters(dict(Price=self.price, TimeInForce=self.tif_ioc, OrigClOrdID='*')).remove_parameters(['ExDestination'])
        self.fix_verifier_buy.check_fix_message(eliminate_slice1_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA Slice 1")
        # endregion

        time.sleep(61)

        # region Check child DMA order Slice 2
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order - Slice 2", self.test_id))

        slice2_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice2_order.change_parameters(dict(OrderQty=self.slice2_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day)) #slice2_
        self.fix_verifier_buy.check_fix_message(slice2_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice 2')

        pending_slice2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_slice2_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice 2')

        new_slice2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_slice2_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice 2')
                
        eliminate_slice2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_order, self.gateway_side_buy, self.status_eliminate)
        eliminate_slice2_order.change_parameters(dict(Price=self.price, TimeInForce=self.tif_ioc, OrigClOrdID='*')).remove_parameters(['ExDestination'])
        self.fix_verifier_buy.check_fix_message(eliminate_slice2_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA Slice 2")
        # endregion

        time.sleep(61)

        # region Check child DMA order Slice 3
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order - Slice 3", self.test_id))

        slice3_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice3_order.change_parameters(dict(OrderQty=self.slice3_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day)) #slice3_
        self.fix_verifier_buy.check_fix_message(slice3_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice 3')

        pending_slice3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice3_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_slice3_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice 3')

        new_slice3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice3_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_slice3_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice 3')
        
        eliminate_slice3_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice3_order, self.gateway_side_buy, self.status_eliminate)
        eliminate_slice3_order.change_parameters(dict(Price=self.price, TimeInForce=self.tif_ioc, OrigClOrdID='*')).remove_parameters(['ExDestination'])
        self.fix_verifier_buy.check_fix_message(eliminate_slice3_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA Slice 3")
        # endregion

        time.sleep(61)

        # region Check child DMA order Slice 4
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order - Slice 4", self.test_id))

        slice4_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice4_order.change_parameters(dict(OrderQty=self.slice4_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day)) #slice4_
        self.fix_verifier_buy.check_fix_message(slice4_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice 4')

        pending_slice4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice4_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_slice4_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice 4')

        new_slice4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice4_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_slice4_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice 4')
        
        eliminate_slice4_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice4_order, self.gateway_side_buy, self.status_eliminate)
        eliminate_slice4_order.change_parameters(dict(Price=self.price, TimeInForce=self.tif_ioc, OrigClOrdID='*')).remove_parameters(['ExDestination'])
        self.fix_verifier_buy.check_fix_message(eliminate_slice4_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA Slice 4")
        # endregion
        
        time.sleep(61)

        # region Check child DMA order Slice 5
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order - Slice 5", self.test_id))

        slice5_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice5_order.change_parameters(dict(OrderQty=self.slice5_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day)) #slice5_
        self.fix_verifier_buy.check_fix_message(slice5_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice 5')

        pending_slice5_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice5_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_slice5_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice 5')

        new_slice5_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice5_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_slice5_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice 5')
        
        eliminate_slice5_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice5_order, self.gateway_side_buy, self.status_eliminate)
        eliminate_slice5_order.change_parameters(dict(Price=self.price, TimeInForce=self.tif_ioc, OrigClOrdID='*')).remove_parameters(['ExDestination'])
        self.fix_verifier_buy.check_fix_message(eliminate_slice5_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA Slice 5")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        RuleManager(Simulators.algo).remove_rules(self.rule_list)

        # # region Cancel Algo Order
        # case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        # self.fix_verifier_sell.set_case_id(case_id_3)
        # cancel_request_twap_order = FixMessageOrderCancelRequest(self.twap_order)
        # 
        # self.fix_manager_sell.send_message_and_receive_response(cancel_request_twap_order, case_id_3)
        # self.fix_verifier_sell.check_fix_message(cancel_request_twap_order, direction=self.ToQuod, message_name='Sell side Cancel Request')
        # # endregion

        # region check eliminaation parent TWAP order
        eliminate_twap_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_eliminate)
        eliminate_twap_order.change_parameters(dict(NoParty='*', Price=self.price, LastMkt='*', Text='reached end time')).remove_parameter('OrigClOrdID')
        self.fix_verifier_sell.check_fix_message(eliminate_twap_order, key_parameters=self.key_params_cl,  message_name='Sell side ExecReport eliminated')
        # endregion