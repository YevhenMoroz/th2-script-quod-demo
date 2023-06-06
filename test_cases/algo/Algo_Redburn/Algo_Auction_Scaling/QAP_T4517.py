import os
import sched
import time

from pathlib import Path

import pytz

from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, TimeInForce, RBCustomTags, Reference, OrderType
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.algo_mongo_manager import AlgoMongoManager as AMM


class QAP_T4517(TestCase):
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
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])
        # endregion

        # region order parameters
        self.qty = 1_000_000
        self.price = 130
        self.parent_price = 129.9417
        self.indicative_volume = 0
        self.indicative_price = 0
        self.historical_volume = 1000000.0
        self.historical_price = 140.0
        self.last_trade_qty = 100000
        self.last_trade_price = 130

        self.percentage_volume = 10
        self.pp1_percentage = 12
        self.pp1_price = 120
        self.pp2_percentage = 30
        self.pp2_price = 110

        self.scaling_child_order_qty = '%^(1[6-9])\d{3}|20{4}|10{5}$'  # fisrt number 100000, 20000, 17-19K and any 3 number
        self.scaling_child_order_price = '%^1(20|30|1[7-9].[1-9]|17)$'  # the first number 130, 120, 117 or 119.7-117.3 with step 3

        self.check_order_sequence = False

        self.tif_atc = TimeInForce.AtTheClose.value
        self.currency_GBX = self.data_set.get_currency_by_name("currency_7")
        # endregion

        # region Child order price after currency conversion
        self.EUR_GBX_conversion_rate = 86.34  # currecny conversion rate from EUR to GBX
        self.decimal_places = 3  # the number of digits after the decimal point
        self.sats_offset = 0.001

        self.child_1_price_converted = float(AFM.calculate_price_with_currency_conversion(130, self.EUR_GBX_conversion_rate, self.decimal_places))  # 1.505
        self.child_2_price_converted = float(AFM.calculate_price_with_currency_conversion(120, self.EUR_GBX_conversion_rate, self.decimal_places))  # 1.389
        self.child_3_price_converted = float(AFM.calculate_price_with_currency_conversion(119, self.EUR_GBX_conversion_rate, self.decimal_places, self.sats_offset))    # 1.377
        self.child_4_price_converted = float(AFM.calculate_price_with_currency_conversion(118, self.EUR_GBX_conversion_rate, self.decimal_places, self.sats_offset))    # 1.365
        self.child_5_price_converted = float(AFM.calculate_price_with_currency_conversion(117, self.EUR_GBX_conversion_rate, self.decimal_places, self.sats_offset * 2))    # 1.353
        self.child_6_price_converted = float(AFM.calculate_price_with_currency_conversion(116, self.EUR_GBX_conversion_rate, self.decimal_places, self.sats_offset * 2))    # 1.341
        self.child_7_price_converted = float(AFM.calculate_price_with_currency_conversion(115, self.EUR_GBX_conversion_rate, self.decimal_places, self.sats_offset * 2))    # 1.329
        self.child_8_price_converted = float(AFM.calculate_price_with_currency_conversion(114, self.EUR_GBX_conversion_rate, self.decimal_places, self.sats_offset * 3))    # 1.317
        self.child_9_price_converted = float(AFM.calculate_price_with_currency_conversion(113, self.EUR_GBX_conversion_rate, self.decimal_places, self.sats_offset * 3))    # 1.305
        self.child_10_price_converted = float(AFM.calculate_price_with_currency_conversion(112, self.EUR_GBX_conversion_rate, self.decimal_places, self.sats_offset * 4))   # 1.293
        self.child_11_price_converted = float(AFM.calculate_price_with_currency_conversion(111, self.EUR_GBX_conversion_rate, self.decimal_places, self.sats_offset * 4))   # 1.281
        self.child_12_price_converted = float(AFM.calculate_price_with_currency_conversion(110, self.EUR_GBX_conversion_rate, self.decimal_places))     # 1.274
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.s_par = self.data_set.get_listing_id_by_name("listing_36")
        # endregion

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        self.rule_list = []

        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule_1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.child_1_price_converted)
        nos_rule_2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.child_2_price_converted)
        nos_rule_3 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.child_3_price_converted)
        nos_rule_4 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.child_4_price_converted)
        nos_rule_5 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.child_5_price_converted)
        nos_rule_6 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.child_6_price_converted)
        nos_rule_7 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.child_7_price_converted)
        nos_rule_8 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.child_8_price_converted)
        nos_rule_9 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.child_9_price_converted)
        nos_rule_10 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.child_10_price_converted)
        nos_rule_11 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.child_11_price_converted)
        nos_rule_12 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.child_12_price_converted)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1)
        cancel_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.client, self.ex_destination_1, True)
        self.rule_list = [nos_rule_1, nos_rule_2, nos_rule_3, nos_rule_4, nos_rule_5, nos_rule_6, nos_rule_7, nos_rule_8, nos_rule_9, nos_rule_10, nos_rule_11, nos_rule_12, ocr_rule, ocrr_rule, cancel_rule]
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phases = AFM.get_timestamps_for_current_phase(TradingPhases.PreClosed)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region insert data into mongoDB
        curve = AMM.get_straight_curve_for_mongo(trading_phases, volume=self.historical_volume, price=self.historical_price)
        self.db_manager.insert_many_to_mongodb_with_drop(curve, f"Q{self.s_par}")
        bca.create_event(f"Collection Q{self.s_par} is inserted", self.test_id, body=''.join([f"{volume['LastTradedTime']} - {volume['LastTradedQty']}, phase - {volume['LastAuctionPhase']}\n" for volume in curve]))
        # endregion

        # region Send MarketDate
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_MDReqID(self.s_par, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.indicative_price).set_phase(TradingPhases.PreClosed)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        # region Send MarketDate
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh().update_MDReqID(self.s_par, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.last_trade_qty).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.last_trade_price)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create Auction Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.auction_algo = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MOC_Scaling_params()
        self.auction_algo.add_ClordId((os.path.basename(__file__)[:-3]))
        self.auction_algo.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_1, Currency=self.currency_GBX))
        self.auction_algo.update_fields_in_component('QuodFlatParameters', dict(MaxParticipation=self.percentage_volume, PricePoint1Participation=self.pp1_percentage, PricePoint1Price=self.pp1_price, PricePoint2Participation=self.pp2_percentage, PricePoint2Price=self.pp2_price))
        self.fix_manager_sell.send_message_and_receive_response(self.auction_algo, case_id_1)

        time.sleep(10)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.auction_algo, key_parameters=self.key_params_cl, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_pending)
        pending_auction_order_params.change_parameters(dict(TimeInForce=self.tif_atc, Price=self.parent_price))
        self.fix_verifier_sell.check_fix_message(pending_auction_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_new)
        new_auction_order_params.change_parameters(dict(TimeInForce=self.tif_atc, Price=self.parent_price))
        self.fix_verifier_sell.check_fix_message(new_auction_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check passive child order 1
        self.case_id_2 = bca.create_event("Scaling child orders", self.test_id)
        self.fix_verifier_buy.set_case_id(bca.create_event("Check 12 Scaling child orders Buy side NewOrderSingle", self.case_id_2))

        # region  Scaling child orders
        # region Scaling child order 1
        scaling_dma_child_order_1 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        scaling_dma_child_order_1.change_parameters(dict(Account=self.account, OrderQty=self.scaling_child_order_qty, Price=self.child_1_price_converted, Instrument='*', TimeInForce=self.tif_atc, ExDestination=self.ex_destination_1))

        pending_scaling_dma_child_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_1, self.gateway_side_buy, self.status_pending)

        new_scaling_dma_child_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_1, self.gateway_side_buy, self.status_new)

        self.cancel_scaling_child_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_1, self.gateway_side_buy, self.status_cancel)
        # endregion
        
        # region Scaling child order 2
        scaling_dma_child_order_2 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        scaling_dma_child_order_2.change_parameters(dict(Account=self.account, OrderQty=self.scaling_child_order_qty, Price=self.child_2_price_converted, Instrument='*', TimeInForce=self.tif_atc, ExDestination=self.ex_destination_1))

        pending_scaling_dma_child_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_2, self.gateway_side_buy, self.status_pending)

        new_scaling_dma_child_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_2, self.gateway_side_buy, self.status_new)

        self.cancel_scaling_child_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_2, self.gateway_side_buy, self.status_cancel)
        # endregion
        
        # region Scaling child order 3
        scaling_dma_child_order_3 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        scaling_dma_child_order_3.change_parameters(dict(Account=self.account, OrderQty=self.scaling_child_order_qty, Price=self.child_3_price_converted, Instrument='*', TimeInForce=self.tif_atc, ExDestination=self.ex_destination_1))

        pending_scaling_dma_child_3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_3, self.gateway_side_buy, self.status_pending)

        new_scaling_dma_child_3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_3, self.gateway_side_buy, self.status_new)

        self.cancel_scaling_child_3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_3, self.gateway_side_buy, self.status_cancel)
        # endregion
        
        # region Scaling child order 4
        scaling_dma_child_order_4 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        scaling_dma_child_order_4.change_parameters(dict(Account=self.account, OrderQty=self.scaling_child_order_qty, Price=self.child_4_price_converted, Instrument='*', TimeInForce=self.tif_atc, ExDestination=self.ex_destination_1))

        pending_scaling_dma_child_4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_4, self.gateway_side_buy, self.status_pending)

        new_scaling_dma_child_4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_4, self.gateway_side_buy, self.status_new)

        self.cancel_scaling_child_4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_4, self.gateway_side_buy, self.status_cancel)
        # endregion
        
        # region Scaling child order 5
        scaling_dma_child_order_5 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        scaling_dma_child_order_5.change_parameters(dict(Account=self.account, OrderQty=self.scaling_child_order_qty, Price=self.child_5_price_converted, Instrument='*', TimeInForce=self.tif_atc, ExDestination=self.ex_destination_1))

        pending_scaling_dma_child_5_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_5, self.gateway_side_buy, self.status_pending)

        new_scaling_dma_child_5_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_5, self.gateway_side_buy, self.status_new)

        self.cancel_scaling_child_5_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_5, self.gateway_side_buy, self.status_cancel)
        # endregion
        
        # region Scaling child order 6
        scaling_dma_child_order_6 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        scaling_dma_child_order_6.change_parameters(dict(Account=self.account, OrderQty=self.scaling_child_order_qty, Price=self.child_6_price_converted, Instrument='*', TimeInForce=self.tif_atc, ExDestination=self.ex_destination_1))

        pending_scaling_dma_child_6_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_6, self.gateway_side_buy, self.status_pending)

        new_scaling_dma_child_6_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_6, self.gateway_side_buy, self.status_new)

        self.cancel_scaling_child_6_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_6, self.gateway_side_buy, self.status_cancel)
        # endregion
        
        # region Scaling child order 7
        scaling_dma_child_order_7 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        scaling_dma_child_order_7.change_parameters(dict(Account=self.account, OrderQty=self.scaling_child_order_qty, Price=self.child_7_price_converted, Instrument='*', TimeInForce=self.tif_atc, ExDestination=self.ex_destination_1))

        pending_scaling_dma_child_7_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_7, self.gateway_side_buy, self.status_pending)

        new_scaling_dma_child_7_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_7, self.gateway_side_buy, self.status_new)

        self.cancel_scaling_child_7_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_7, self.gateway_side_buy, self.status_cancel)
        # endregion
        
        # region Scaling child order 8
        scaling_dma_child_order_8 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        scaling_dma_child_order_8.change_parameters(dict(Account=self.account, OrderQty=self.scaling_child_order_qty, Price=self.child_8_price_converted, Instrument='*', TimeInForce=self.tif_atc, ExDestination=self.ex_destination_1))

        pending_scaling_dma_child_8_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_8, self.gateway_side_buy, self.status_pending)

        new_scaling_dma_child_8_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_8, self.gateway_side_buy, self.status_new)

        self.cancel_scaling_child_8_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_8, self.gateway_side_buy, self.status_cancel)
        # endregion
        
        # region Scaling child order 9
        scaling_dma_child_order_9 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        scaling_dma_child_order_9.change_parameters(dict(Account=self.account, OrderQty=self.scaling_child_order_qty, Price=self.child_9_price_converted, Instrument='*', TimeInForce=self.tif_atc, ExDestination=self.ex_destination_1))

        pending_scaling_dma_child_9_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_9, self.gateway_side_buy, self.status_pending)

        new_scaling_dma_child_9_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_9, self.gateway_side_buy, self.status_new)

        self.cancel_scaling_child_9_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_9, self.gateway_side_buy, self.status_cancel)
        # endregion
        
        # region Scaling child order 10
        scaling_dma_child_order_10 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        scaling_dma_child_order_10.change_parameters(dict(Account=self.account, OrderQty=self.scaling_child_order_qty, Price=self.child_10_price_converted, Instrument='*', TimeInForce=self.tif_atc, ExDestination=self.ex_destination_1))

        pending_scaling_dma_child_10_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_10, self.gateway_side_buy, self.status_pending)

        new_scaling_dma_child_10_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_10, self.gateway_side_buy, self.status_new)

        self.cancel_scaling_child_10_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_10, self.gateway_side_buy, self.status_cancel)
        # endregion
        
        # region Scaling child order 11
        scaling_dma_child_order_11 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        scaling_dma_child_order_11.change_parameters(dict(Account=self.account, OrderQty=self.scaling_child_order_qty, Price=self.child_11_price_converted, Instrument='*', TimeInForce=self.tif_atc, ExDestination=self.ex_destination_1))

        pending_scaling_dma_child_11_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_11, self.gateway_side_buy, self.status_pending)

        new_scaling_dma_child_11_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_11, self.gateway_side_buy, self.status_new)

        self.cancel_scaling_child_11_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_11, self.gateway_side_buy, self.status_cancel)
        # endregion
        
        # region Scaling child order 12
        scaling_dma_child_order_12 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        scaling_dma_child_order_12.change_parameters(dict(Account=self.account, OrderQty=self.scaling_child_order_qty, Price=self.child_12_price_converted, Instrument='*', TimeInForce=self.tif_atc, ExDestination=self.ex_destination_1))

        pending_scaling_dma_child_12_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_12, self.gateway_side_buy, self.status_pending)

        new_scaling_dma_child_12_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_12, self.gateway_side_buy, self.status_new)

        self.cancel_scaling_child_12_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(scaling_dma_child_order_12, self.gateway_side_buy, self.status_cancel)
        # endregion
        # endregion

        # region Check Scaling child orders
        self.fix_verifier_buy.check_fix_message_sequence([scaling_dma_child_order_1, scaling_dma_child_order_2, scaling_dma_child_order_3, scaling_dma_child_order_4, scaling_dma_child_order_5, scaling_dma_child_order_6, scaling_dma_child_order_7, scaling_dma_child_order_8, scaling_dma_child_order_9, scaling_dma_child_order_10, scaling_dma_child_order_11, scaling_dma_child_order_12], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 12 Scaling child orders Buy Side Pending New", self.case_id_2))
        self.fix_verifier_buy.check_fix_message_sequence([pending_scaling_dma_child_1_order_params, pending_scaling_dma_child_2_order_params, pending_scaling_dma_child_3_order_params, pending_scaling_dma_child_4_order_params, pending_scaling_dma_child_5_order_params, pending_scaling_dma_child_6_order_params, pending_scaling_dma_child_7_order_params, pending_scaling_dma_child_8_order_params, pending_scaling_dma_child_9_order_params, pending_scaling_dma_child_10_order_params, pending_scaling_dma_child_11_order_params, pending_scaling_dma_child_12_order_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 12 Scaling child orders Buy Side New", self.case_id_2))
        self.fix_verifier_buy.check_fix_message_sequence([new_scaling_dma_child_1_order_params, new_scaling_dma_child_2_order_params, new_scaling_dma_child_3_order_params, new_scaling_dma_child_4_order_params, new_scaling_dma_child_5_order_params, new_scaling_dma_child_6_order_params, new_scaling_dma_child_7_order_params, new_scaling_dma_child_8_order_params, new_scaling_dma_child_9_order_params, new_scaling_dma_child_10_order_params, new_scaling_dma_child_11_order_params, new_scaling_dma_child_12_order_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Check eliminated Algo Order
        case_id_3 = bca.create_event("Cancel parent Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        # endregion

        cancel_request_auction_order = FixMessageOrderCancelRequest(self.auction_algo)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_auction_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_auction_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(5)

        self.db_manager.drop_collection(f"Q{self.s_par}")
        bca.create_event(f"Collection QP{self.s_par} is dropped", self.test_id)

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region Check cancellation of the Scaling child orders
        self.fix_verifier_buy.set_case_id(bca.create_event("Check 12 Scaling child orders Buy Side Cancel", self.case_id_2))
        self.fix_verifier_buy.check_fix_message_sequence([self.cancel_scaling_child_1_order_params, self.cancel_scaling_child_2_order_params, self.cancel_scaling_child_3_order_params, self.cancel_scaling_child_4_order_params, self.cancel_scaling_child_5_order_params, self.cancel_scaling_child_6_order_params, self.cancel_scaling_child_7_order_params, self.cancel_scaling_child_8_order_params, self.cancel_scaling_child_9_order_params, self.cancel_scaling_child_10_order_params, self.cancel_scaling_child_11_order_params, self.cancel_scaling_child_12_order_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

        # region check cancellation parent Auction order
        cancel_auction_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_cancel)
        cancel_auction_order.change_parameters(dict(TimeInForce=self.tif_atc, Price=self.parent_price))
        self.fix_verifier_sell.check_fix_message(cancel_auction_order, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')
        # endregion
