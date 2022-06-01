import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase


class QAP_3526(TestCase):
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
        # weights CHIXDELTA=40/BATSDARK=20/ITG=40
        self.qty = 10000
        self.minQty = 7000
        self.qty_1_2_3_child = 10000
        self.price = 20
        self.reason = 99
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_reject = Status.Reject
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
        self.ex_destination_itg = self.data_set.get_mic_by_name("mic_7")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account_bats = self.data_set.get_account_by_name("account_7")
        self.account_chix = self.data_set.get_account_by_name("account_8")
        self.account_itg_cboe_tqdarkeu = self.data_set.get_account_by_name("account_9")
        # endregion

        # region Key parameters
        self.key_params_with_cl_ord_id = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_without_cl_ord_id = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        self.key_params_with_cl_ord_id_and_ex_destination = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_mp_dark_child")
        self.verifier_key_parameters_with_only_cl_ord_id = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager()
        nos_1_reject_rule = rule_manager.add_NewOrderSingle_ExecutionReport_RejectWithReason(self.fix_env1.buy_side, self.account_bats, self.ex_destination_bats, self.price, self.reason)
        nos_2_reject_rule = rule_manager.add_NewOrderSingle_ExecutionReport_RejectWithReason(self.fix_env1.buy_side, self.account_chix, self.ex_destination_chix, self.price, self.reason)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_itg_cboe_tqdarkeu, self.ex_destination_itg, self.price)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_itg_cboe_tqdarkeu, self.ex_destination_itg, True)
        self.rule_list = [nos_1_reject_rule, nos_2_reject_rule, nos_1_rule, ocr_rule]
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.MP_Dark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MPDark_params()
        self.MP_Dark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.MP_Dark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.MP_Dark_order.add_tag(dict(MinQty=self.minQty))

        self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.MP_Dark_order, key_parameters=self.verifier_key_parameters_with_only_cl_ord_id, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_pending)
        er_pending_new_MP_Dark_order_params.add_tag(dict(MinQty=self.minQty))
        er_pending_new_MP_Dark_order_params.remove_parameter('NoStrategyParameters')
        self.fix_verifier_sell.check_fix_message(er_pending_new_MP_Dark_order_params, key_parameters=self.key_params_with_cl_ord_id, message_name='Sell side ExecReport PendingNew')

        er_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_new)
        er_new_MP_Dark_order_params.add_tag(dict(MinQty=self.minQty))
        er_new_MP_Dark_order_params.remove_parameter('NoStrategyParameters')

        self.fix_verifier_sell.check_fix_message(er_new_MP_Dark_order_params, key_parameters=self.key_params_with_cl_ord_id, message_name='Sell side ExecReport New')
        # endregion

        # region Check child DMA order on venue CHIX DARKPOOL UK
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.dma_chix_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_chix_order.change_parameters(dict(Account=self.account_chix, ExDestination=self.ex_destination_chix, OrderQty=self.qty_1_2_3_child, Price=self.price, Instrument=self.instrument))
        self.dma_chix_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message(self.dma_chix_order, key_parameters=self.key_params_with_cl_ord_id_and_ex_destination, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chix_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_chix_order_params.change_parameters(dict(ExDestination=self.ex_destination_chix))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_chix_order_params, key_parameters=self.key_params_with_cl_ord_id_and_ex_destination, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chix_order, self.gateway_side_buy, self.status_pending)
        er_new_dma_chix_order_params.change_parameters(dict(ExDestination=self.ex_destination_chix))
        self.fix_verifier_buy.check_fix_message(er_new_dma_chix_order_params, key_parameters=self.key_params_with_cl_ord_id_and_ex_destination, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        # TODO check: it`s work or no?

        # region check reject first dma child order
        er_reject_dma_chix_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chix_order, self.gateway_side_buy, self.status_reject)
        self.fix_verifier_buy.check_fix_message(er_reject_dma_chix_order, self.key_params_with_cl_ord_id_and_ex_destination, self.ToQuod, "Buy Side ExecReport Reject child DMA 1 order")
        # endregion

        # region Check child DMA order on venue BATS DARKPOOL UK
        self.dma_bats_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_bats_order.change_parameters(dict(ccount=self.account_bats, ExDestination=self.ex_destination_bats, OrderQty=self.qty_1_2_3_child, Price=self.price, Instrument=self.instrument))
        self.dma_bats_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message(self.dma_bats_order, key_parameters=self.key_params_with_cl_ord_id_and_ex_destination, message_name='Buy side NewOrderSingle Child DMA 2 order')

        time.sleep(2)

        er_pending_new_dma_bats_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_bats_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_bats_order_params.change_parameters(dict(ExDestination=self.ex_destination_bats))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_bats_order_params, key_parameters=self.key_params_with_cl_ord_id_and_ex_destination, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 2 order')

        er_new_dma_bats_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_bats_order, self.gateway_side_buy, self.status_new)
        er_new_dma_bats_order_params.change_parameters(dict(ExDestination=self.ex_destination_bats))
        self.fix_verifier_buy.check_fix_message(er_new_dma_bats_order_params, key_parameters=self.key_params_with_cl_ord_id_and_ex_destination, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 2 order')
        # endregion

        # region check reject second dma child order
        er_reject_dma_bats_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_bats_order, self.gateway_side_buy, self.status_reject)
        self.fix_verifier_buy.check_fix_message(er_reject_dma_bats_order, self.key_params_with_cl_ord_id_and_ex_destination, self.ToQuod, "Buy Side ExecReport Reject child DMA 2 order")
        # endregion

        # region Check child DMA order on venue ITG
        self.dma_itg_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_itg_order.change_parameters(dict(Account=self.account_itg_cboe_tqdarkeu, ExDestination=self.ex_destination_itg, OrderQty=self.qty_1_2_3_child, Price=self.price, Instrument=self.instrument))
        self.dma_itg_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message(self.dma_itg_order, key_parameters=self.key_params_with_cl_ord_id_and_ex_destination, message_name='Buy side NewOrderSingle Child DMA 3 order')

        time.sleep(2)

        er_pending_new_dma_itg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_itg_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_itg_order_params.change_parameters(dict(ExDestination=self.ex_destination_itg))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_itg_order_params, key_parameters=self.key_params_with_cl_ord_id_and_ex_destination, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 3 order')

        er_new_dma_itg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_itg_order, self.gateway_side_buy, self.status_new)
        er_new_dma_itg_order_params.change_parameters(dict(ExDestination=self.ex_destination_itg))
        self.fix_verifier_buy.check_fix_message(er_new_dma_itg_order_params, key_parameters=self.key_params_with_cl_ord_id_and_ex_destination, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 3 order')
        # endregion


    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_MP_Dark_order = FixMessageOrderCancelRequest(self.MP_Dark_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_MP_Dark_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_MP_Dark_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel third dma child order
        er_cancel_dma_itg_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_itg_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_itg_order, self.key_params_with_cl_ord_id_and_ex_destination, self.ToQuod, "Buy Side ExecReport Cancel child DMA 3 order")
        # endregion

        er_cancel_mp_dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_cancel)
        er_cancel_mp_dark_order_params.remove_parameter('NoStrategyParameters')
        self.fix_verifier_sell.check_fix_message(er_cancel_mp_dark_order_params, key_parameters=self.key_params_without_cl_ord_id, message_name='Sell side ExecReport Cancel')

        RuleManager.remove_rules(self.rule_list)
















