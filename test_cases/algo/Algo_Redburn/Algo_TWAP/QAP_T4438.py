import os
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.constants import GatewaySide, Status, DirectionEnum
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.core.test_case import TestCase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T4438(TestCase):
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
    
        #order param
        self.avt = 10000     # average volume traded per minute
        self.ast = self.avt * 5   # 5 average traded
        self.qty = 100000
        self.waves = 5
        self.qty_twap_1 = int(self.qty / self.waves)
        self.first_reserve = max(self.ast, int(self.qty * (1 - 1)))
        self.reserve = max(self.first_reserve, int(self.qty_twap_1))
        self.qty_nav = self.qty - self.reserve
        self.price = 29.995
        self.price_nav = 30
        self.slice_duration = 2
        self.navigator_max_slice_size = 10000

        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name('account_2')
        self.s_par = self.data_set.get_listing_id_by_name('listing_36')

        # Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_1')
        self.key_params = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_2')

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel_replace = Status.CancelReplace
        self.status_cancel = Status.Cancel
        self.status_reject = Status.Reject
        self.status_fill = Status.Fill
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        self.text_reject_navigator_limit_price = DataSet.FreeNotesReject.MissNavigatorLimitPrice.value

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):

        #TODO test not done

        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price)
        nos_trade = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_nav, self.price_nav, self.navigator_max_slice_size, self.navigator_max_slice_size, 0)
        nos_rule1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_nav)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(self.fix_env1.buy_side, False)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [nos_rule, nos_trade, nos_rule1, ocrr_rule, ocr_rule]

        now = datetime.utcnow()

        # Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot)


        # region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        twap_nav_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_TWAP_Navigator_params()
        twap_nav_order.add_ClordId((os.path.basename(__file__)[:-3]))
        twap_nav_order.change_parameters(dict(Account=self.client, OrderQty=self.qty))
        twap_nav_order.update_fields_in_component('QuodFlatParameters', dict(Waves=self.waves, NavigatorLimitPrice=self.price_nav, SliceDuration=self.slice_duration, NavigatorMaxSliceSize=self.navigator_max_slice_size, EndDate2=(now + timedelta(minutes=10)).strftime("%Y%m%d-%H:%M:%S")))

        self.fix_manager_sell.send_message_and_receive_response(twap_nav_order, case_id_1)


        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(twap_nav_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_nav_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_twap_nav_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_nav_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_twap_nav_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # Check First TWAP child
        self.fix_verifier_buy.set_case_id(bca.create_event("First TWAP slice", self.test_id))

        twap_1_child = FixMessageNewOrderSingleAlgo().set_DMA_params()
        twap_1_child.change_parameters(dict(OrderQty=self.qty_twap_1, Price=self.price))
        self.fix_verifier_buy.check_fix_message(twap_1_child, key_parameters=self.key_params, message_name='Buy side NewOrderSingle TWAP child')

        pending_twap_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_1_child, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_twap_1_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew TWAP child')

        new_twap_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_1_child, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_twap_1_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New TWAP child')

        # Check First Navigator child
        nav_1_child = FixMessageNewOrderSingleAlgo().set_DMA_params()
        nav_1_child.change_parameters(dict(OrderQty=self.navigator_max_slice_size, Price=self.price_nav))
        self.fix_verifier_buy.check_fix_message(nav_1_child, key_parameters=self.key_params, message_name='Buy side NewOrderSingle First Navigator')

        pending_nav_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_1_child, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_nav_1_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew First Navigator child')

        new_nav_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_1_child, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_nav_1_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New First Navigator child')

        fill_nav_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_1_child, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(fill_nav_1_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Fill First Navigator child')

        # Check Second Navigator child
        self.fix_verifier_buy.set_case_id(bca.create_event("Second Navigator child", self.test_id))

        nav_2_child = FixMessageNewOrderSingleAlgo().set_DMA_params()
        nav_2_child.change_parameters(dict(OrderQty=self.navigator_max_slice_size, Price=self.price_nav))
        self.fix_verifier_buy.check_fix_message(nav_1_child, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Second Navigator')

        pending_nav_2_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_2_child, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_nav_2_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Second Navigator')

        new_nav_2_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_2_child, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_nav_2_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Second Navigator')

        fill_nav_2_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_2_child, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(fill_nav_2_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Fill Second Navigator child')
        # endregion

        # region Cancel Algo Order
        case_id_4 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_4)
        # Cancel Order
        cancel_request_twap_nav_order = FixMessageOrderCancelRequest(twap_nav_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_twap_nav_order, case_id_4)
        self.fix_verifier_sell.check_fix_message(cancel_request_twap_nav_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # Cancel TWAP child
        cancel_twap_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_1_child, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_twap_1_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Navigator')

        cancel_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_nav_order, self.gateway_side_sell, self.status_cancel)
        cancel_twap_nav_order_params.change_parameters(dict(AvgPx=self.price_nav, CumQty='*'))
        self.fix_verifier_sell.check_fix_message(cancel_twap_nav_order_params, key_parameters=self.key_params, message_name='Sell side ExecReport Cancel')
        # endregion
        
    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        time.sleep(3)

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
    
