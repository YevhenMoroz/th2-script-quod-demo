import os
import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers import DataSet
from test_framework.algo_formulas_manager import AlgoFormulasManager
from test_framework.core.test_case import TestCase
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T4303(TestCase):
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

        self.ats = 10000
        self.qty = 100000
        self.waves = 4
        self.qty_twap_1 = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves)
        self.qty_nav = AlgoFormulasManager.get_twap_nav_child_qty(self.qty, self.waves, self.ats)
        self.nav_limit_price_reference = DataSet.Reference.Limit.value
        self.price = 29.995
        self.price_nav = 30

        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name('account_2')
        self.s_par = self.data_set.get_listing_id_by_name('listing_36')

        # Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_1')
        self.key_params = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_2')

        # Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_1')
        self.key_params = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_2') #TIF off
        self.key_params_mkt = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_3')


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
        self.status_eliminate = Status.Eliminate
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        self.text_reject_navigator_limit_price = DataSet.FreeNotesReject.MissNavigatorLimitPrice.value
        self.text_reject_navigator_limit_price_reference = DataSet.FreeNotesReject.MissNavigatorLimitPriceReference.value


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingle_Market(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, 0)
        nos_rule1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_nav)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [nos_rule, nos_rule1, ocr_rule]

        # region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.twap_nav_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_TWAP_Navigator_params()
        self.twap_nav_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.twap_nav_order.remove_parameter('Price')
        self.twap_nav_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, OrdType=1))
        self.twap_nav_order.update_fields_in_component('QuodFlatParameters', dict(NavigatorLimitPrice=self.price_nav, Waves=self.waves, NavigatorLimitPriceReference=self.nav_limit_price_reference))

        self.fix_manager_sell.send_message_and_receive_response(self.twap_nav_order, case_id_1)

        time.sleep(3)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.twap_nav_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_nav_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_twap_nav_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_nav_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_twap_nav_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check Buy side
        # Check First TWAP child
        self.fix_verifier_buy.set_case_id(bca.create_event("First TWAP slice", self.test_id))

        self.twap_child = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.twap_child.change_parameters(dict(OrderQty=self.qty_twap_1, OrdType=1))
        self.twap_child.remove_parameter('Price')
        self.fix_verifier_buy.check_fix_message(self.twap_child, key_parameters=self.key_params_mkt, message_name='Buy side NewOrderSingle TWAP child')

        pending_twap_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_child, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_twap_child_params, key_parameters=self.key_params_mkt, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew TWAP child')

        new_twap_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_child, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_twap_child_params, key_parameters=self.key_params_mkt, direction=self.ToQuod, message_name='Buy side ExecReport New TWAP child')

        # Check First Navigator child
        self.nav_child_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.nav_child_1.change_parameters(dict(OrderQty=self.qty_nav, Price=self.price_nav))
        self.fix_verifier_buy.check_fix_message(self.nav_child_1, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Navigator')

        pending_nav_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.nav_child_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_nav_child_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Navigator')

        new_nav_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.nav_child_1, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_nav_child_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Navigator')
        # endregion


    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_4 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_4)
        # Cancel Order
        cancel_request_twap_nav_order = FixMessageOrderCancelRequest(self.twap_nav_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_twap_nav_order, case_id_4)
        self.fix_verifier_sell.check_fix_message(cancel_request_twap_nav_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        cancel_twap_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_child, self.gateway_side_buy, self.status_eliminate)
        self.fix_verifier_buy.check_fix_message(cancel_twap_child_params, key_parameters=self.key_params_mkt, direction=self.ToQuod, message_name='Buy side ExecReport Cancel TWAP child')

        cancel_nav_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.nav_child_1, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_nav_child_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Navigator')

        cancel_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_nav_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_twap_nav_order_params, key_parameters=self.key_params, message_name='Sell side ExecReport Cancel')
        # endregion