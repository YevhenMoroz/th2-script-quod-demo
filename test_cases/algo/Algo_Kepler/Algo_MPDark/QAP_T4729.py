import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRequestAlgo import FixMessageOrderCancelRequestAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.algo_formulas_manager import AlgoFormulasManager
from test_framework.data_sets import constants


class QAP_T4729(TestCase):
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
        # weights CHIX = 6, BATS = 4,
        self.qty = 12000
        self.inc_qty = 22000
        self.minQty = 1000
        self.weight_chix = 6
        self.weight_bats = 4
        self.qty_1_chix_child, self.qty_1_bats_child = AlgoFormulasManager.get_child_qty_on_venue_weights(self.qty, self.minQty, self.weight_chix, self.weight_bats)
        self.qty_2_chix_child, self.qty_2_bats_child = AlgoFormulasManager.get_child_qty_on_venue_weights(self.inc_qty, self.minQty, self.weight_chix, self.weight_bats)
        self.price = 20
        self.algopolicy = constants.ClientAlgoPolicy.qa_mpdark_2.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel_replace = Status.CancelReplace
        self.status_cancel = Status.Cancel
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_6")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_bats = self.data_set.get_mic_by_name("mic_4")
        self.ex_destination_chix = self.data_set.get_mic_by_name("mic_5")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account_bats = self.data_set.get_account_by_name("account_7")
        self.account_chix = self.data_set.get_account_by_name("account_8")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        # endregion

        self.pre_filter = self.data_set.get_pre_filter("pre_filer_equal_F")

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_chix, self.ex_destination_chix, self.price)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_bats, self.ex_destination_bats, self.price)
        ocr_1_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_chix, self.ex_destination_chix, True)
        ocr_2_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_bats, self.ex_destination_bats, True)
        self.rule_list = [nos_1_rule, nos_2_rule, ocr_1_rule, ocr_2_rule]
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.MP_Dark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MPDark_Kepler_params()
        self.MP_Dark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.MP_Dark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, ClientAlgoPolicyID=self.algopolicy))
        self.MP_Dark_order.add_tag(dict(MinQty=self.minQty))

        self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.MP_Dark_order, key_parameters=self.key_params_NOS_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check 1 child DMA order on venue CHIX DARKPOOL UK
        self.fix_verifier_buy.set_case_id(bca.create_event("Dark child DMA orders", self.test_id))

        self.dma_1_chix_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_1_chix_order.change_parameters(dict(Account=self.account_chix, ExDestination=self.ex_destination_chix, OrderQty=self.qty_1_chix_child))
        self.dma_1_chix_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_1_chix_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order on venue CHIX DARKPOOL UK')

        er_pending_new_dma_1_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_chix_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_1_chix_order_params.change_parameters(dict(ExDestination=self.ex_destination_chix))
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_1_chix_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order on venue CHIX DARKPOOL UK')

        er_new_dma_1_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_chix_order, self.gateway_side_buy, self.status_new)
        er_new_dma_1_chix_order_params.change_parameters(dict(ExDestination=self.ex_destination_chix))
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_1_chix_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order on venue CHIX DARKPOOL UK')
        # endregion

        # region Check 1 child DMA order on venue BATS DARKPOOL UK
        self.dma_1_bats_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_1_bats_order.change_parameters(dict(Account=self.account_bats, ExDestination=self.ex_destination_bats, OrderQty=self.qty_1_bats_child))
        self.dma_1_bats_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_1_bats_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 2 order on venue BATS DARKPOOL UK')

        er_pending_new_dma_1_bats_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_bats_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_1_bats_order_params.change_parameters(dict(ExDestination=self.ex_destination_bats))
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_1_bats_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 2 order on venue BATS DARKPOOL UK')

        er_new_dma_1_bats_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_bats_order, self.gateway_side_buy, self.status_new)
        er_new_dma_1_bats_order_params.change_parameters(dict(ExDestination=self.ex_destination_bats))
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_1_bats_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 2 order on venue BATS DARKPOOL UK')
        # endregion

        # region Modify parent MP Dark order
        case_id_2 = bca.create_event("Replace MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)

        self.MP_Dark_order_replace_params = FixMessageOrderCancelReplaceRequestAlgo(self.MP_Dark_order)
        self.MP_Dark_order_replace_params.change_parameters(dict(OrderQty=self.inc_qty))
        self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order_replace_params, case_id_2)

        time.sleep(1)

        self.fix_verifier_sell.check_fix_message(self.MP_Dark_order_replace_params, direction=self.ToQuod, message_name='Sell side OrderCancelReplaceRequest')

        er_replaced_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.MP_Dark_order_replace_params, self.gateway_side_sell, self.status_cancel_replace)
        self.fix_verifier_sell.check_fix_message(er_replaced_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell Side ExecReport Replace Request')
        # endregion

        time.sleep(3)

        # region Check that 35=F on childs are received
        self.fix_verifier_buy.set_case_id(bca.create_event("Check that 35=F on childs are received", self.test_id))
        cancel_request_dma_1_chix_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_1_chix_order)
        cancel_request_dma_1_bats_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_1_bats_order)
        self.fix_verifier_buy.check_fix_message_sequence_kepler([cancel_request_dma_1_chix_order, cancel_request_dma_1_bats_order], key_parameters_list=[None, None], direction=self.FromQuod, pre_filter=self.pre_filter)
        # endregion

        # region check cancel first dma child order
        er_cancel_dma_1_chix_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_chix_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_1_chix_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 1 order on venue CHIX DARKPOOL UK")
        # endregion

        # region check cancel second dma child order
        er_cancel_dma_1_bats_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_bats_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_1_bats_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 2 order on venue BATS DARKPOOL UK")
        # endregion

        time.sleep(1)

        # region Check 2 child DMA order on venue CHIX DARKPOOL UK
        self.fix_verifier_buy.set_case_id(bca.create_event("New Child DMA orders", self.test_id))

        self.dma_2_chix_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_2_chix_order.change_parameters(dict(Account=self.account_chix, ExDestination=self.ex_destination_chix, OrderQty=self.qty_2_chix_child))
        self.dma_2_chix_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_2_chix_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 3 order on venue CHIX DARKPOOL UK')

        er_pending_new_dma_2_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_chix_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_2_chix_order_params.change_parameters(dict(ExDestination=self.ex_destination_chix))
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_2_chix_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 3 order on venue CHIX DARKPOOL UK')

        er_new_dma_2_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_chix_order, self.gateway_side_buy, self.status_new)
        er_new_dma_2_chix_order_params.change_parameters(dict(ExDestination=self.ex_destination_chix))
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_2_chix_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 3 order on venue CHIX DARKPOOL UK')
        # endregion

        # region Check 2 child DMA order on venue BATS DARKPOOL UK
        self.dma_2_bats_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_2_bats_order.change_parameters(dict(Account=self.account_bats, ExDestination=self.ex_destination_bats, OrderQty=self.qty_2_bats_child))
        self.dma_2_bats_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_2_bats_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 4 order on venue BATS DARKPOOL UK')

        er_pending_new_dma_2_bats_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_bats_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_2_bats_order_params.change_parameters(dict(ExDestination=self.ex_destination_bats))
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_2_bats_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 4 order on venue BATS DARKPOOL UK')

        er_new_dma_2_bats_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_bats_order, self.gateway_side_buy, self.status_new)
        er_new_dma_2_bats_order_params.change_parameters(dict(ExDestination=self.ex_destination_bats))
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_2_bats_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 4 order on venue BATS DARKPOOL UK')
        # endregion

        time.sleep(2)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        cancel_request_MP_Dark_order = FixMessageOrderCancelRequest(self.MP_Dark_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_MP_Dark_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_MP_Dark_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(2)

        # region check cancel third dma child order
        er_cancel_dma_2_chix_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_chix_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_2_chix_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 3 order on venue CHIX DARKPOOL UK")
        # endregion

        # region check cancel fourth dma child order
        er_cancel_dma_2_bats_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_bats_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_2_bats_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 4 order on venue BATS DARKPOOL UK")
        # endregion

        er_cancel_mp_dark_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.MP_Dark_order_replace_params, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_mp_dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

















