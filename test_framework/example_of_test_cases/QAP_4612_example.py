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
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.algo_formulas_manager import AlgoFormulasManager
from test_framework.core.test_case import TestCase


class QAP_4612_example(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, data_set=None, environment=None):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        # region th2 components
        self.fix_manager_sell = FixManager(self.environment.sell_side, self.test_id)
        self.fix_manager_feed_handler = FixManager(self.environment.feed_handler, self.test_id)
        self.fix_verifier_sell = FixVerifier(self.environment.sell_side, self.test_id)
        self.fix_verifier_buy = FixVerifier(self.environment.buy_side, self.test_id)
        # endregion

        # region order parameters
        self.tick = 0.005
        self.qty = 2000
        self.price_parent = 22
        self.price_ask = 21
        self.price_bid = 19.98
        self.price_trigger = self.price_ask + self.tick
        self.would_price_reference = 'MAN'
        self.would_price_offset = 1
        self.price_would = AlgoFormulasManager.calc_ticks_offset_minus(self.price_trigger, self.would_price_offset, self.tick)
        self.tif_ioc = 3
        #endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_fill = Status.Fill
        # endregion

        # region instrument
        self.instrument = self.data_set.get_instrument_by_name("instrument_2")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_1")
        self.account = self.data_set.get_account_by_name("account_1")
        self.s_par = '1015'
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):

        #Key parameters
        #TODO add enum
        key_params_cl = ['ClOrdID', 'OrdStatus', 'ExecType', 'OrderQty', 'Price']
        key_params = ['OrdStatus', 'ExecType', 'OrderQty', 'Price']


        # region Rule creation
        rule_manager = RuleManager()
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.environment.buy_side, self.account, self.ex_destination_1, True, self.qty, self.price_ask)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.environment.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [nos_ioc_rule, ocr_rule]
        # endregion

        now = datetime.today() - timedelta(hours=2)

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.environment.feed_handler)
        market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty)
        market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot)

        time.sleep(3)

        # endregion

        # region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        twap_would_order = FixMessageNewOrderSingleAlgo().set_TWAP_params()
        twap_would_order.add_ClordId((os.path.basename(__file__)[:-3]))
        twap_would_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price_parent))
        twap_would_order.update_fields_in_component('QuodFlatParameters', dict(StartDate2=now.strftime("%Y%m%d-%H:%M:%S"), EndDate2=(now + timedelta(minutes=4)).strftime("%Y%m%d-%H:%M:%S"),
                                                                               WouldPriceReference=self.would_price_reference, WouldPriceOffset=self.would_price_offset, TriggerPriceRed=self.price_trigger))

        self.fix_manager_sell.send_message_and_receive_response(twap_would_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(twap_would_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_twap_would_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_would_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_twap_would_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_twap_would_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_would_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_twap_would_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check First TWAP child
        self.fix_verifier_buy.set_case_id(bca.create_event("First TWAP slice", self.test_id))

        twap_1_child = FixMessageNewOrderSingleAlgo().set_DMA_params()
        twap_1_child.change_parameters(dict(OrderQty=self.qty, Price=self.price_would, TimeInForce=self.tif_ioc, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(twap_1_child, key_parameters=key_params, message_name='Buy side NewOrderSingle TWAP child')

        pending_twap_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_1_child, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_twap_1_child_params, key_parameters=key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew TWAP child')

        new_twap_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_1_child, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_twap_1_child_params, key_parameters=key_params, direction=self.ToQuod, message_name='Buy side ExecReport New TWAP child')

        fill_twap_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_1_child, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(fill_twap_1_child_params, key_parameters=key_params, direction=self.ToQuod, message_name='Buy side ExecReport Fill TWAP child')

        time.sleep(3)
        # endregion

        # region Fill Algo Order
        case_id_4 = bca.create_event("Fill Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_4)
        # Fill Order
        fill_twap_would_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_would_order, self.gateway_side_sell, self.status_fill)
        self.fix_verifier_sell.check_fix_message(fill_twap_would_order, key_parameters=key_params_cl, message_name='Sell side ExecReport Fill')
        # endregion

        @try_except(test_id=Path(__file__).name[:-3])
        def run_post_conditions():
            RuleManager.remove_rules(self.rule_list)
