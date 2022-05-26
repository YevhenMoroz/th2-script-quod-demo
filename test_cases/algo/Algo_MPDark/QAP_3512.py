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
from test_framework.data_sets import constants


class QAP_3512(TestCase):
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
        # weights CHIXDELTA=6, ITG=6, BATSDARK=4, ITG=3, CBOEEUDARK=2, LIQUIDNETEU=1
        self.qty = 100000
        self.minQty = 20000
        self.qty_child = 20000 
        self.price = 20
        self.tif_fok = constants.TimeInForce.FillOrKill.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        self.status_eliminate = Status.Eliminate
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
        self.ex_destination_cboe = self.data_set.get_mic_by_name("mic_6")
        self.ex_destination_itg = self.data_set.get_mic_by_name("mic_7")
        self.ex_destination_tqdarkeu = self.data_set.get_mic_by_name("mic_8")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account_bats = self.data_set.get_account_by_name("account_7")
        self.account_chix = self.data_set.get_account_by_name("account_8")
        self.account_itg_cboe_tqdarkeu = self.data_set.get_account_by_name("account_9")
        self.s_bats = self.data_set.get_listing_id_by_name("listing_4")
        self.s_chix = self.data_set.get_listing_id_by_name("listing_5")
        self.s_cboe = self.data_set.get_listing_id_by_name("listing_6")
        self.s_itg = self.data_set.get_listing_id_by_name("listing_7")
        self.s_tqdarkeu = self.data_set.get_listing_id_by_name("listing_8")
        # endregion

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        # TODO edit rule for itg, tqdarkeu (TIF=Day), add cancel
        rule_manager = RuleManager()
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_bats, self.ex_destination_bats, self.price)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_chix, self.ex_destination_chix, self.price)
        nos_3_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_itg_cboe_tqdarkeu, self.ex_destination_cboe, self.price)
        nos_1_fok_rule = rule_manager.add_NewOrdSingle_FOK(self.fix_env1.buy_side, self.account_itg_cboe_tqdarkeu, self.ex_destination_itg, False, self.price)
        nos_2_fok_rule = rule_manager.add_NewOrdSingle_FOK(self.fix_env1.buy_side, self.account_itg_cboe_tqdarkeu, self.ex_destination_tqdarkeu, False, self.price)
        ocr_1_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_chix, self.ex_destination_chix, True)
        ocr_2_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_bats, self.ex_destination_bats, True)
        ocr_3_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_itg_cboe_tqdarkeu, self.ex_destination_cboe, True)
        self.rule_list = [nos_1_rule, nos_2_rule, nos_3_rule, nos_1_fok_rule, nos_2_fok_rule, ocr_1_rule, ocr_2_rule, ocr_3_rule]
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
        self.fix_verifier_sell.check_fix_message(self.MP_Dark_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_pending)
        pending_MP_Dark_order_params.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_sell.check_fix_message(pending_MP_Dark_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_new)
        new_MP_Dark_order_params.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_sell.check_fix_message(new_MP_Dark_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # TODO Need check order of child orders and statuses

        # region Check child DMA order on venue BATS DARKPOOL UK
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.dma_1_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_1_order.change_parameters(dict(OrderQty=self.qty_child, Price=self.price, Instrument=self.instrument))
        self.dma_1_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message(self.dma_1_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA 1 order')

        pending_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        new_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_dma_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        # region Check child DMA order on venue CHIX DARKPOOL UK
        self.dma_2_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_2_order.change_parameters(dict(OrderQty=self.qty_child, Price=self.price, Instrument=self.instrument))
        self.dma_2_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message(self.dma_2_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA 2 order')

        time.sleep(2)

        pending_dma_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_2_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 2 order')

        new_dma_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_dma_2_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 2 order')
        # endregion

        # region Check child DMA order on venue CBOE DARKPOOL EU
        self.dma_3_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_3_order.change_parameters(dict(OrderQty=self.qty_child, Price=self.price, Instrument=self.instrument))
        self.dma_3_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message(self.dma_3_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA 3 order')

        time.sleep(2)

        pending_dma_3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_3_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 3 order')

        new_dma_3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_dma_3_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 3 order')
        # endregion

        # region Check child DMA order on venue ITG
        self.dma_4_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_4_order.change_parameters(dict(OrderQty=self.qty_child, Price=self.price, Instrument=self.instrument, TimeInForce=self.tif_fok))
        self.dma_4_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message(self.dma_4_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA 4 order')

        time.sleep(2)

        pending_dma_4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_4_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_4_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 4 order')

        new_dma_4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_4_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_dma_4_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 4 order')
        # endregion

        # region Check child DMA order on venue TURQUOISE DARKPOOL EU
        self.dma_5_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_5_order.change_parameters(dict(OrderQty=self.qty_child, Price=self.price, Instrument=self.instrument, TimeInForce=self.tif_fok))
        self.dma_5_order.add_tag(dict(MinQty=self.minQty))
        self.fix_verifier_buy.check_fix_message(self.dma_5_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA 5 order')

        time.sleep(2)

        pending_dma_5_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_5_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_5_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 5 order')

        new_dma_5_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_5_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_dma_5_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 5 order')
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
        cancel_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_dma_1_order, self.key_params, self.ToQuod, "Buy Side ExecReport Cancel first DMA 1 order")
        # endregion

        # region check cancel second dma child order
        cancel_dma_2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_dma_2_order, self.key_params, self.ToQuod, "Buy Side ExecReport Cancel child DMA 2 order")
        # endregion

        # region check cancel third dma child order
        cancel_dma_3_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_dma_3_order, self.key_params, self.ToQuod, "Buy Side ExecReport Cancel child DMA 3 order")
        # endregion

        # TODO check cancel, not eliminate

        # region check cancel fourth dma child order
        cancel_dma_4_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_4_order, self.gateway_side_buy, self.status_eliminate)
        self.fix_verifier_buy.check_fix_message(cancel_dma_4_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate child DMA 4 order")
        # endregion

        # region check cancel fifth dma child order
        cancel_dma_5_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_5_order, self.gateway_side_buy, self.status_eliminate)
        self.fix_verifier_buy.check_fix_message(cancel_dma_5_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate child DMA 5 order")
        # endregion


        RuleManager.remove_rules(self.rule_list)











