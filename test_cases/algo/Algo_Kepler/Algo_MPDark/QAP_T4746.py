import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.algo_formulas_manager import AlgoFormulasManager
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


class QAP_T4746(TestCase):
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
        self.qty = 1000000
        self.price = 20
        self.weight_bats = 4
        self.weight_chix = 6
        self.qty_chix_child, self.qty_bats_child = AlgoFormulasManager.get_child_qty_on_venue_weights(self.qty, None, self.weight_chix, self.weight_bats)
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
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_6")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_chixlis = self.data_set.get_mic_by_name("mic_12")
        self.ex_destination_trql = self.data_set.get_mic_by_name("mic_13")
        self.ex_destination_bats_dark = self.data_set.get_mic_by_name("mic_4")
        self.ex_destination_chix_dark = self.data_set.get_mic_by_name("mic_5")


        self.client = self.data_set.get_client_by_name("client_4")
        self.client_bats_dark = self.data_set.get_client_by_name("client_5")
        self.client_chix_delta = self.data_set.get_client_by_name("client_6")

        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_with_ex_destination = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):

        rule_manager = RuleManager()
        new_order_single_BATD = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.client_bats_dark, self.ex_destination_bats_dark, self.price)
        new_order_single_CHID = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.client_chix_delta, self.ex_destination_chix_dark, self.price)
        cancel_rule_BATD = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.client_bats_dark, self.ex_destination_bats_dark, True)
        cancel_rule_CHID = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.client_chix_delta, self.ex_destination_chix_dark, True)
        self.rule_list = [new_order_single_BATD, new_order_single_CHID, cancel_rule_BATD, cancel_rule_CHID]

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.MP_Dark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MPDark_params()
        self.MP_Dark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.MP_Dark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, ClientAlgoPolicyID="QA_Auto_MPDark9"))
        response = self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order, case_id_1)[0]
        expectedtime = (datetime.strptime(response.get_parameter("header")['SendingTime'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(milliseconds=700)).isoformat()

        time.sleep(5)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.MP_Dark_order, key_parameters=self.key_params_NOS_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        case_id_2 = bca.create_event("Create RFQ on buy side", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_2)

        # region check that RFQ send to CHIX LIS UK
        nos_chixlis_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.qty, ExDestination=self.ex_destination_chixlis, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(nos_chixlis_order, key_parameters=self.key_params_with_ex_destination, message_name='Buy side RFQ on CHIXLIS')
        # endregion

        # region check that RFQ send to TURQUOISE LIS
        nos_trql_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.qty, ExDestination=self.ex_destination_trql, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(nos_trql_order, key_parameters=self.key_params_with_ex_destination, message_name='Buy side RFQ on TQLIS')
        # endregion

        # region dark orders sended on market
        self.fix_verifier_buy.set_case_id(bca.create_event("After timeout algo generate child orders on Dark venues", self.test_id))
        # CHIXDELTA
        self.dma_chix_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_params()
        self.dma_chix_order.change_parameters(dict(Account=self.client_chix_delta, ExDestination=self.ex_destination_chix_dark, OrderQty=self.qty_chix_child, TransactTime="!>" + expectedtime))
        self.fix_verifier_buy.check_fix_message(self.dma_chix_order, key_parameters=self.key_params_with_ex_destination, message_name='Buy side NewOrderSingle dark child on chix_delta')

        er_pending_new_dma_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chix_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_chix_order_params.change_parameters(dict(ExDestination=self.ex_destination_chix_dark))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_chix_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew dark child on chix_delta')

        er_new_dma_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chix_order, self.gateway_side_buy, self.status_new)
        er_new_dma_chix_order_params.change_parameters(dict(ExDestination=self.ex_destination_chix_dark))
        self.fix_verifier_buy.check_fix_message(er_new_dma_chix_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New dark child on chix_delta')

        # BATSDARK
        self.dma_bats_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_params()
        self.dma_bats_order.change_parameters(dict(Account=self.client_bats_dark, ExDestination=self.ex_destination_bats_dark, OrderQty=self.qty_bats_child, TransactTime="!>" + expectedtime))
        self.fix_verifier_buy.check_fix_message(self.dma_bats_order, key_parameters=self.key_params_with_ex_destination, message_name='Buy side NewOrderSingle dark child on bats_dark')

        er_pending_new_dma_bats_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_bats_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_bats_order_params.change_parameters(dict(ExDestination=self.ex_destination_bats_dark))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_bats_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew dark child on bats_dark')

        er_new_dma_bats_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_bats_order, self.gateway_side_buy, self.status_new)
        er_new_dma_bats_order_params.change_parameters(dict(ExDestination=self.ex_destination_bats_dark))
        self.fix_verifier_buy.check_fix_message(er_new_dma_bats_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport dark child on bats_dark')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        cancel_request_MP_Dark_order = FixMessageOrderCancelRequest(self.MP_Dark_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_MP_Dark_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_MP_Dark_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        er_cancel_mp_dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_mp_dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager()
        rule_manager.remove_rules(self.rule_list)