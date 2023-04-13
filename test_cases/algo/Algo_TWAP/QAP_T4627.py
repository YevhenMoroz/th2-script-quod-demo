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
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager

class QAP_T4627(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, data_set=None, environment=None):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.fix_env1 = self.environment.get_list_fix_environment()[0]
        self.restapi_env1 = self.environment.get_list_web_admin_rest_api_environment()[0]

        # region th2 components
        self.fix_manager_sell = FixManager(self.fix_env1.sell_side, self.test_id)
        self.fix_manager_feed_handler = FixManager(self.fix_env1.feed_handler, self.test_id)
        self.fix_verifier_sell = FixVerifier(self.fix_env1.sell_side, self.test_id)
        self.fix_verifier_buy = FixVerifier(self.fix_env1.buy_side, self.test_id)
        self.rest_api_manager = RestApiAlgoManager(session_alias='rest_wa310columbia')
        # self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa)
        # endregion

        # region order parameters
        # self.tick_size = 0.005
        self.algo_policy_id = "Test Modification TWAP Algo Policy"
        self.aggressivity = 2
        self.order_type = constants.OrderType.Limit.value
        self.qty = 1000
        self.price = self.price_ask = 1
        self.price_bid = 0.8
        # self.mid_price = int((self.price_ask + self.price_bid)/2)
        self.qty_bid = self.qty_ask = 1_000_000
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.tif_day = constants.TimeInForce.Day.value
        self.waves_1 = 5
        self.waves_2 = 4
        self.slice1_1_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves_1)
        self.slice1_2_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves_1-1)
        self.slice1_3_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves_1-2)
        self.slice1_4_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves_1-3)
        self.slice1_5_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves_1-4)
        self.slice2_1_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves_2)
        self.slice2_2_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves_2-1)
        self.slice2_3_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves_2-2)
        self.slice2_4_qty = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves_2-3)
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
        #TODO RestAPI review

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region initialize strategy
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify strategy", self.test_id))
        self.rest_api_manager.modify_strategy_parameter(self.algo_policy_id, "Waves", str(self.waves_1))
        # endregion

        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price) # _bid-self.tick_size
        # ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(self.fix_env1.buy_side, False)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, 40, 0)
        self.rule_list = [nos_rule, ocr_rule, ocrr_rule, ioc_rule]
        # endregion

        now = datetime.utcnow()
        start_time = now.strftime("%Y%m%d-%H:%M:%S")
        end_time = (now + timedelta(minutes=6)).strftime("%Y%m%d-%H:%M:%S")

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle1 (35=D) for TWAP order 1
        case_id_1 = bca.create_event("Create TWAP Order 1", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.twap_order1 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_TWAP_params()
        self.twap_order1.add_fields_into_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='StartDate', StrategyParameterType=19, StrategyParameterValue=start_time),
                                                                                 dict(StrategyParameterName='EndDate', StrategyParameterType=19, StrategyParameterValue=end_time)])
        # self.twap_order1.add_tag(dict())
        self.twap_order1.add_ClordId((os.path.basename(__file__)[:-3]))
        self.twap_order1.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ClientAlgoPolicyID=self.algo_policy_id))
        self.fix_manager_sell.send_message_and_receive_response(self.twap_order1, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        nos_twap_parent1 = self.twap_order1.change_parameter('TransactTime', '*')
        self.fix_verifier_sell.check_fix_message(nos_twap_parent1, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_twap_order1_params1 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order1, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_twap_order1_params1, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_twap_order1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order1, self.gateway_side_sell, self.status_new)
        new_twap_order1_params.change_parameter('NoParty', '*').remove_parameter('SecondaryAlgoPolicyID')
        # new_twap_order1_params.update_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='Waves', StrategyParameterType='1', StrategyParameterValue=self.waves_1),
        #                                                       dict(StrategyParameterName='Aggressivity', StrategyParameterType='1', StrategyParameterValue=self.aggressivity)])
        self.fix_verifier_sell.check_fix_message(new_twap_order1_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion
        
        time.sleep(65)
       
        # region Check child DMA order Slice1_1
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order - Slice1_1", self.test_id))

        slice1_1_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice1_1_order.change_parameters(dict(OrderQty=self.slice1_1_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day)) #slice1_1_
        self.fix_verifier_buy.check_fix_message(slice1_1_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice1_1')

        pending_slice1_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_slice1_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice1_1')

        new_slice1_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_slice1_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice1_1')
        
        eliminate_slice1_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_1_order, self.gateway_side_buy, self.status_eliminate)
        eliminate_slice1_1_order.change_parameters(dict(Price=self.price, TimeInForce=self.tif_ioc, OrigClOrdID='*')).remove_parameters(['ExDestination'])
        self.fix_verifier_buy.check_fix_message(eliminate_slice1_1_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA Slice1_1")
        # endregion

        time.sleep(75)

        # region Check child DMA order Slice1_2
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order - Slice1_2", self.test_id))

        slice1_2_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice1_2_order.change_parameters(dict(OrderQty=self.slice1_2_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day)) #slice1_2_
        self.fix_verifier_buy.check_fix_message(slice1_2_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice1_2')

        pending_slice1_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_2_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_slice1_2_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice1_2')

        new_slice1_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_2_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_slice1_2_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice1_2')
                
        eliminate_slice1_2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_2_order, self.gateway_side_buy, self.status_eliminate)
        eliminate_slice1_2_order.change_parameters(dict(Price=self.price, TimeInForce=self.tif_ioc, OrigClOrdID='*')).remove_parameters(['ExDestination'])
        self.fix_verifier_buy.check_fix_message(eliminate_slice1_2_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA Slice1_2")
        # endregion

        time.sleep(75)

        # region Check child DMA order Slice1_3
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order - Slice1_3", self.test_id))

        slice1_3_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice1_3_order.change_parameters(dict(OrderQty=self.slice1_3_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day)) #slice1_3_
        self.fix_verifier_buy.check_fix_message(slice1_3_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice1_3')

        pending_slice1_3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_3_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_slice1_3_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice1_3')

        new_slice1_3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_3_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_slice1_3_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice1_3')
        
        eliminate_slice1_3_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_3_order, self.gateway_side_buy, self.status_eliminate)
        eliminate_slice1_3_order.change_parameters(dict(Price=self.price, TimeInForce=self.tif_ioc, OrigClOrdID='*')).remove_parameters(['ExDestination'])
        self.fix_verifier_buy.check_fix_message(eliminate_slice1_3_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA Slice1_3")
        # endregion

        time.sleep(75)

        # region Check child DMA order Slice1_4
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order - Slice1_4", self.test_id))

        slice1_4_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice1_4_order.change_parameters(dict(OrderQty=self.slice1_4_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day)) #slice1_4_
        self.fix_verifier_buy.check_fix_message(slice1_4_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice1_4')

        pending_slice1_4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_4_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_slice1_4_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice1_4')

        new_slice1_4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_4_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_slice1_4_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice1_4')
        
        eliminate_slice1_4_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_4_order, self.gateway_side_buy, self.status_eliminate)
        eliminate_slice1_4_order.change_parameters(dict(Price=self.price, TimeInForce=self.tif_ioc, OrigClOrdID='*')).remove_parameters(['ExDestination'])
        self.fix_verifier_buy.check_fix_message(eliminate_slice1_4_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA Slice1_4")
        # endregion
        
        time.sleep(75)

        # region Check child DMA order Slice1_5
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order - Slice1_5", self.test_id))

        slice1_5_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice1_5_order.change_parameters(dict(OrderQty=self.slice1_5_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day)) #slice1_5_
        self.fix_verifier_buy.check_fix_message(slice1_5_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice1_5')

        pending_slice1_5_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_5_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_slice1_5_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice1_5')

        new_slice1_5_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_5_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_slice1_5_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice1_5')
        
        eliminate_slice1_5_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice1_5_order, self.gateway_side_buy, self.status_eliminate)
        eliminate_slice1_5_order.change_parameters(dict(Price=self.price, TimeInForce=self.tif_ioc, OrigClOrdID='*')).remove_parameters(['ExDestination'])
        self.fix_verifier_buy.check_fix_message(eliminate_slice1_5_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA Slice1_5")
        # endregion
        
        # region change strategy
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify strategy", self.test_id))
        self.rest_api_manager.modify_strategy_parameter(self.algo_policy_id, "Waves", str(self.waves_2))
        # endregion

        now = datetime.utcnow()
        start_time = now.strftime("%Y%m%d-%H:%M:%S")
        end_time = (now + timedelta(minutes=6)).strftime("%Y%m%d-%H:%M:%S")

        # region Send NewOrderSingle1 (35=D) for TWAP order 2
        case_id_1 = bca.create_event("Create TWAP Order 2", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.twap_order2 = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_TWAP_params()
        self.twap_order2.add_fields_into_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='StartDate', StrategyParameterType=19, StrategyParameterValue=start_time),
                                                                                 dict(StrategyParameterName='EndDate', StrategyParameterType=19, StrategyParameterValue=end_time)])
        # self.twap_order2.add_tag(dict())
        self.twap_order2.add_ClordId((os.path.basename(__file__)[:-3]))
        self.twap_order2.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ClientAlgoPolicyID=self.algo_policy_id))
        self.fix_manager_sell.send_message_and_receive_response(self.twap_order2, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        nos_twap_parent2 = self.twap_order2.change_parameter('TransactTime', '*')
        self.fix_verifier_sell.check_fix_message(nos_twap_parent2, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_twap_order2_params1 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order2, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_twap_order2_params1, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_twap_order2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order2, self.gateway_side_sell, self.status_new)
        new_twap_order2_params.change_parameter('NoParty', '*')
        new_twap_order2_params.update_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='Waves', StrategyParameterType='1', StrategyParameterValue=self.waves_2),
                                                              dict(StrategyParameterName='Aggressivity', StrategyParameterType='1', StrategyParameterValue=self.aggressivity)])
        self.fix_verifier_sell.check_fix_message(new_twap_order2_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion
        
        time.sleep(75)
        
        # region Check child DMA order Slice2_1
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order - Slice2_1", self.test_id))

        slice2_1_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice2_1_order.change_parameters(dict(OrderQty=self.slice2_1_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day)) #slice2_1_
        self.fix_verifier_buy.check_fix_message(slice2_1_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice2_1')

        pending_slice2_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_slice2_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice2_1')

        new_slice2_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_slice2_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice2_1')
                
        eliminate_slice2_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_1_order, self.gateway_side_buy, self.status_eliminate)
        eliminate_slice2_1_order.change_parameters(dict(Price=self.price, TimeInForce=self.tif_ioc, OrigClOrdID='*')).remove_parameters(['ExDestination'])
        self.fix_verifier_buy.check_fix_message(eliminate_slice2_1_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA Slice2_1")
        # endregion

        # region Check child DMA order Slice2_2
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order - Slice2_2", self.test_id))

        slice2_2_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice2_2_order.change_parameters(dict(OrderQty=self.slice2_2_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day)) #slice2_2_
        self.fix_verifier_buy.check_fix_message(slice2_2_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice2_2')

        pending_slice2_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_2_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_slice2_2_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice2_2')

        new_slice2_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_2_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_slice2_2_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice2_2')
                
        eliminate_slice2_2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_2_order, self.gateway_side_buy, self.status_eliminate)
        eliminate_slice2_2_order.change_parameters(dict(Price=self.price, TimeInForce=self.tif_ioc, OrigClOrdID='*')).remove_parameters(['ExDestination'])
        self.fix_verifier_buy.check_fix_message(eliminate_slice2_2_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA Slice2_2")
        # endregion

        time.sleep(75)

        # region Check child DMA order Slice2_3
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order - Slice2_3", self.test_id))

        slice2_3_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice2_3_order.change_parameters(dict(OrderQty=self.slice2_3_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day)) #slice2_3_
        self.fix_verifier_buy.check_fix_message(slice2_3_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice2_3')

        pending_slice2_3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_3_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_slice2_3_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice2_3')

        new_slice2_3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_3_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_slice2_3_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice2_3')
        
        eliminate_slice2_3_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_3_order, self.gateway_side_buy, self.status_eliminate)
        eliminate_slice2_3_order.change_parameters(dict(Price=self.price, TimeInForce=self.tif_ioc, OrigClOrdID='*')).remove_parameters(['ExDestination'])
        self.fix_verifier_buy.check_fix_message(eliminate_slice2_3_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA Slice2_3")
        # endregion

        time.sleep(75)

        # region Check child DMA order Slice2_4
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order - Slice2_4", self.test_id))

        slice2_4_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        slice2_4_order.change_parameters(dict(OrderQty=self.slice2_4_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day)) #slice2_4_
        self.fix_verifier_buy.check_fix_message(slice2_4_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice2_4')

        pending_slice2_4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_4_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_slice2_4_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice2_4')

        new_slice2_4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_4_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_slice2_4_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice2_4')
        
        eliminate_slice2_4_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(slice2_4_order, self.gateway_side_buy, self.status_eliminate)
        eliminate_slice2_4_order.change_parameters(dict(Price=self.price, TimeInForce=self.tif_ioc, OrigClOrdID='*')).remove_parameters(['ExDestination'])
        self.fix_verifier_buy.check_fix_message(eliminate_slice2_4_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA Slice2_4")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # # region Cancel Algo Order
        # case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        # self.fix_verifier_sell.set_case_id(case_id_3)
        # cancel_request_twap_order = FixMessageOrderCancelRequest(self.twap_order)
        # 
        # self.fix_manager_sell.send_message_and_receive_response(cancel_request_twap_order, case_id_3)
        # self.fix_verifier_sell.check_fix_message(cancel_request_twap_order, direction=self.ToQuod, message_name='Sell side Cancel Request')
        # # endregion

        # region check elimination parent TWAP order 1
        eliminate_twap_order1 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order1, self.gateway_side_sell, self.status_eliminate)
        eliminate_twap_order1.change_parameter('NoParty', '*')
        self.fix_verifier_sell.check_fix_message(eliminate_twap_order1, key_parameters=self.key_params_cl,  message_name='Sell side ExecReport eliminated')
        # endregion
        
        # region check elimination parent TWAP order 2
        eliminate_twap_order2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order2, self.gateway_side_sell, self.status_eliminate)
        eliminate_twap_order2.change_parameter('NoParty', '*')
        self.fix_verifier_sell.check_fix_message(eliminate_twap_order2, key_parameters=self.key_params_cl,  message_name='Sell side ExecReport eliminated')
        # endregion
        
        # region revert strategy
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify strategy", self.test_id))
        self.rest_api_manager.modify_strategy_parameter(self.algo_policy_id, "Waves", str(self.waves_1))
        # endregion

        RuleManager(Simulators.algo).remove_rules(self.rule_list)