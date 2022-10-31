import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.algo_formulas_manager import AlgoFormulasManager
from test_framework.data_sets import constants


class QAP_T4730(TestCase):
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
        # weights CHIX DARKPOOL UK=20/BATS DARKPOOL UK=15/CBOE DARKPOOL EU=15/ITG=15/TQDARKEU=10/TQDARK=10/
        self.qty = 10000
        self.minQty = 1000
        self.weight_chix = 20
        self.weight_bats = 15
        self.weight_cboe = 15
        self.weight_itg = 15
        self.weight_tqdarkeu = 10
        self.weight_tqdark = 10
        self.qty_chix_child, self.qty_bats_child, self.qty_cboe_child, self.qty_itg_child, self.qty_tqdarkeu_child, self.qty_tqdark_child = AlgoFormulasManager.get_child_qty_on_venue_weights(self.qty, self.minQty, self.weight_chix, self.weight_bats, self.weight_cboe, self.weight_itg, self.weight_tqdarkeu, self.weight_tqdark)
        self.price = 20
        self.algopolicy = constants.ClientAlgoPolicy.qa_mpdark_6.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_7")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_bats = self.data_set.get_mic_by_name("mic_4")
        self.ex_destination_chix = self.data_set.get_mic_by_name("mic_5")
        self.ex_destination_cboe = self.data_set.get_mic_by_name("mic_6")
        self.ex_destination_itg = self.data_set.get_mic_by_name("mic_7")
        self.ex_destination_tqdarkeu = self.data_set.get_mic_by_name("mic_8")
        self.ex_destination_tqdark = self.data_set.get_mic_by_name("mic_9")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account_bats = self.data_set.get_account_by_name("account_7")
        self.account_chix = self.data_set.get_account_by_name("account_8")
        self.account_itg_cboe_tqdarkeu = self.data_set.get_account_by_name("account_9")
        self.account_tqdark = self.data_set.get_account_by_name("account_10")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_bats, self.ex_destination_bats, self.price)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_chix, self.ex_destination_chix, self.price)
        nos_3_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_itg_cboe_tqdarkeu, self.ex_destination_cboe, self.price)
        nos_4_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_itg_cboe_tqdarkeu, self.ex_destination_itg, self.price)
        nos_5_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_itg_cboe_tqdarkeu, self.ex_destination_tqdarkeu, self.price)
        nos_6_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_tqdark, self.ex_destination_tqdark, self.price)
        ocr_1_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_chix, self.ex_destination_chix, True)
        ocr_2_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_bats, self.ex_destination_bats, True)
        ocr_3_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_itg_cboe_tqdarkeu, self.ex_destination_cboe, True)
        ocr_4_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_itg_cboe_tqdarkeu, self.ex_destination_itg, True)
        ocr_5_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_itg_cboe_tqdarkeu, self.ex_destination_tqdarkeu, True)
        ocr_6_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_tqdark, self.ex_destination_tqdark, True)
        self.rule_list = [nos_1_rule, nos_2_rule, nos_3_rule, nos_4_rule, nos_5_rule, nos_6_rule, ocr_1_rule, ocr_2_rule, ocr_3_rule, ocr_4_rule, ocr_5_rule, ocr_6_rule]
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.MP_Dark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MPDark_params()
        self.MP_Dark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.MP_Dark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Instrument=self.instrument, ClientAlgoPolicyID=self.algopolicy))
        self.MP_Dark_order.add_tag(dict(MinQty=self.minQty))

        self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.MP_Dark_order, key_parameters=self.key_params_NOS_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check child DMA order on venue CHIX DARKPOOL UK
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA orders", self.test_id))

        self.dma_chix_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_params()
        self.dma_chix_order.change_parameters(dict(Account=self.account_chix, ExDestination=self.ex_destination_chix, OrderQty=self.qty_chix_child, Instrument=self.instrument))
        self.dma_chix_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message(self.dma_chix_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order on venue CHIX DARKPOOL UK')

        er_pending_new_dma_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chix_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_chix_order_params.change_parameters(dict(ExDestination=self.ex_destination_chix))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_chix_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order on venue CHIX DARKPOOL UK')

        er_new_dma_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chix_order, self.gateway_side_buy, self.status_new)
        er_new_dma_chix_order_params.change_parameters(dict(ExDestination=self.ex_destination_chix))
        self.fix_verifier_buy.check_fix_message(er_new_dma_chix_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order on venue CHIX DARKPOOL UK')
        # endregion

        # region Check child DMA order on venue BATS DARKPOOL UK
        self.dma_bats_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_params()
        self.dma_bats_order.change_parameters(dict(Account=self.account_bats, ExDestination=self.ex_destination_bats, OrderQty=self.qty_bats_child, Instrument=self.instrument))
        self.dma_bats_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message(self.dma_bats_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 2 order on venue BATS DARKPOOL UK')

        er_pending_new_dma_bats_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_bats_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_bats_order_params.change_parameters(dict(ExDestination=self.ex_destination_bats))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_bats_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 2 order on venue BATS DARKPOOL UK')

        er_new_dma_bats_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_bats_order, self.gateway_side_buy, self.status_new)
        er_new_dma_bats_order_params.change_parameters(dict(ExDestination=self.ex_destination_bats))
        self.fix_verifier_buy.check_fix_message(er_new_dma_bats_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 2 order on venue BATS DARKPOOL UK')
        # endregion

        # region Check child DMA order on venue CBOE DARKPOOL EU
        self.dma_cboe_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_params()
        self.dma_cboe_order.change_parameters(dict(Account=self.account_itg_cboe_tqdarkeu, ExDestination=self.ex_destination_cboe, OrderQty=self.qty_cboe_child, Instrument=self.instrument))
        self.dma_cboe_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message(self.dma_cboe_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 3 order on venue CBOE DARKPOOL EU')

        er_pending_new_dma_cboe_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_cboe_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_cboe_order_params.change_parameters(dict(ExDestination=self.ex_destination_cboe))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_cboe_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 3 order on venue CBOE DARKPOOL EU')

        er_new_dma_cboe_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_cboe_order, self.gateway_side_buy, self.status_new)
        er_new_dma_cboe_order_params.change_parameters(dict(ExDestination=self.ex_destination_cboe))
        self.fix_verifier_buy.check_fix_message(er_new_dma_cboe_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 3 order on venue CBOE DARKPOOL EU')
        # endregion

        # region Check child DMA order on venue ITG
        self.dma_itg_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_params()
        self.dma_itg_order.change_parameters(dict(Account=self.account_itg_cboe_tqdarkeu, ExDestination=self.ex_destination_itg, OrderQty=self.qty_itg_child, Instrument='*'))
        self.dma_itg_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message(self.dma_itg_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 4 order on venue ITG')

        er_pending_new_dma_itg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_itg_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_itg_order_params.change_parameters(dict(ExDestination=self.ex_destination_itg))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_itg_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 4 order on venue ITG')

        er_new_dma_itg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_itg_order, self.gateway_side_buy, self.status_new)
        er_new_dma_itg_order_params.change_parameters(dict(ExDestination=self.ex_destination_itg))
        self.fix_verifier_buy.check_fix_message(er_new_dma_itg_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 4 order on venue ITG')
        # endregion

        # region Check child DMA order on venue TURQUOISE DARKPOOL EU
        self.dma_tqdarkeu_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_params()
        self.dma_tqdarkeu_order.change_parameters(dict(Account=self.account_itg_cboe_tqdarkeu, ExDestination=self.ex_destination_tqdarkeu, OrderQty=self.qty_tqdarkeu_child, Instrument='*'))
        self.dma_tqdarkeu_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message(self.dma_tqdarkeu_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 5 order on venue TURQUOISE DARKPOOL EU')

        er_pending_new_dma_tqdarkeu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_tqdarkeu_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_tqdarkeu_order_params.change_parameters(dict(ExDestination=self.ex_destination_tqdarkeu))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_tqdarkeu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 5 order on venue TURQUOISE DARKPOOL EU')

        er_new_dma_tqdarkeu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_tqdarkeu_order, self.gateway_side_buy, self.status_new)
        er_new_dma_tqdarkeu_order_params.change_parameters(dict(ExDestination=self.ex_destination_tqdarkeu))
        self.fix_verifier_buy.check_fix_message(er_new_dma_tqdarkeu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 5 order on venue TURQUOISE DARKPOOL EU')
        # endregion

        # region Check child DMA order on venue TURQUOISE DARKPOOL UK
        self.dma_tqdark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_params()
        self.dma_tqdark_order.change_parameters(dict(Account=self.account_tqdark, ExDestination=self.ex_destination_tqdark, OrderQty=self.qty_tqdark_child, Instrument='*'))
        self.dma_tqdark_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message(self.dma_tqdark_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 6 order on venue TURQUOISE DARKPOOL UK')

        er_pending_new_dma_tqdark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_tqdark_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_tqdark_order_params.change_parameters(dict(ExDestination=self.ex_destination_tqdark))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_tqdark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 6 order on venue TURQUOISE DARKPOOL UK')

        er_new_dma_tqdark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_tqdark_order, self.gateway_side_buy, self.status_new)
        er_new_dma_tqdark_order_params.change_parameters(dict(ExDestination=self.ex_destination_tqdark))
        self.fix_verifier_buy.check_fix_message(er_new_dma_tqdark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 6 order on venue TURQUOISE DARKPOOL UK')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_MP_Dark_order = FixMessageOrderCancelRequest(self.MP_Dark_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_MP_Dark_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_MP_Dark_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel first dma child order
        er_cancel_dma_chix_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chix_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_chix_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel first DMA 1 order on venue CHIX DARKPOOL UK")
        # endregion

        # region check cancel second dma child order
        er_cancel_dma_bats_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_bats_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_bats_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 2 order on venue BATS DARKPOOL UK")
        # endregion

        # region check cancel third dma child order
        er_cancel_dma_cboe_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_cboe_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_cboe_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 3 order on venue CBOE DARKPOOL EU")
        # endregion

        # region check cancel fourth dma child order
        er_cancel_dma_itg_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_itg_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_itg_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 4 order on venue ITG")
        # endregion

        # region check cancel fifth dma child order
        er_cancel_dma_tqdarkeu_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_tqdarkeu_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_tqdarkeu_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 5 order on venue TURQUOISE DARKPOOL EU")
        # endregion
        
        # region check cancel sixth dma child order
        er_cancel_dma_tqdark_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_tqdark_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_tqdark_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 6 order on venue TURQUOISE DARKPOOL UK")
        # endregion

        er_cancel_mp_dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_mp_dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

