import os
import time
from copy import deepcopy
from pathlib import Path

from test_framework.algo_formulas_manager import AlgoFormulasManager
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets import constants
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRequestAlgo import FixMessageOrderCancelRequestAlgo
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager


class QAP_T10528(TestCase):
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
        # endregion

        # region order parameters
        self.qty = 3000000
        self.trade_qty = 5000
        self.price = 20
        self.qty_after_trade = self.qty - self.trade_qty
        self.delay_for_trade = 0
        # The delay for rfq can be 10000 (links to the delays on the sim)
        self.delay_for_rfq = 7000
        self.algopolicy = constants.ClientAlgoPolicy.qa_mpdark_rr_1.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_partial_fill = Status.PartialFill
        self.status_cancel = Status.Cancel
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_37")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_chixlis = self.data_set.get_mic_by_name("mic_12")
        self.ex_destination_trql = self.data_set.get_mic_by_name("mic_13")
        self.ex_destination_trqx = self.data_set.get_mic_by_name("mic_2")
        self.ex_destination_chixdelta = self.data_set.get_mic_by_name("mic_5")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account_chixdelta = self.data_set.get_client_by_name("client_6")
        # endregion
        
        # region Key parameters
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_NOS_LIS = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_RFQ")
        self.key_params_ER_FQ = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_RFQ")
        # endregion

        self.new_reply = True
        self.restated_reply = True
        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_chixdelta, self.ex_destination_chixdelta, self.price)
        nos_trade_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(self.fix_env1.buy_side, self.account_chixdelta, self.ex_destination_chixdelta, self.price, self.price, self.qty, self.trade_qty, self.delay_for_trade)
        rfq_rule = rule_manager.add_NewOrdSingleRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_chixlis, self.qty, self.qty, self.new_reply, self.restated_reply, self.delay_for_rfq)
        rfq_cancel_rule = rule_manager.add_OrderCancelRequestRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_trqx, True)
        ocr_1_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_chixdelta, self.ex_destination_chixdelta, True)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.client, self.ex_destination_chixlis, self.price)
        ocr_2_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.client, self.ex_destination_chixlis, True)

        self.rule_list = [nos_1_rule, nos_trade_rule, rfq_rule, rfq_cancel_rule, ocr_1_rule, nos_2_rule, ocr_2_rule]
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.MP_Dark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MPDark_Kepler_params()
        self.MP_Dark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.MP_Dark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty,  Price=self.price, ClientAlgoPolicyID=self.algopolicy, Instrument=self.instrument))
        self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order, case_id_1)

        time.sleep(15)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.MP_Dark_order, key_parameters=self.key_params_NOS_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check RFQs
        case_id_2 = bca.create_event("Create RFQs on buy side", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_2)

        # region check that RFQ send to CHIX LIS UK
        nos_chixlis_rfq = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.qty, ExDestination=self.ex_destination_chixlis, Instrument='*'))
        self.fix_verifier_buy.check_fix_message_kepler(nos_chixlis_rfq, key_parameters=self.key_params_NOS_child, message_name='Buy side RFQ on CHIXLIS', direction=self.FromQuod)
        # endregion

        # region check that RFQ send to TURQUOISE LIS
        nos_trql_rfq = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.qty, ExDestination=self.ex_destination_trql, Instrument='*'))
        self.fix_verifier_buy.check_fix_message_kepler(nos_trql_rfq, key_parameters=self.key_params_NOS_child, message_name='Buy side RFQ on TQLIS')
        # endregion

        # region Check the dark DMA child
        self.fix_verifier_buy.set_case_id(bca.create_event("After LIS time is over the algo generates a child order on Dark venue", self.test_id))

        self.dma_chixdelta_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_chixdelta_order.change_parameters(dict(Account=self.account_chixdelta, ExDestination=self.ex_destination_chixdelta, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_chixdelta_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle dark child DMA order on the CHIXDELTA')

        er_pending_new_dma_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chixdelta_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew dark child on chixdelta')

        er_new_dma_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chixdelta_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New dark child DMA order on the CHIXDELTA')

        er_partial_fill_dma_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chixdelta_order, self.gateway_side_buy, self.status_partial_fill)
        self.fix_verifier_buy.check_fix_message_kepler(er_partial_fill_dma_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Partial fill dark child DMA order on the CHIXDELTA')
        # endregion
        
        # region Check that the CHIXLIS rfq accepted
        self.fix_verifier_buy.set_case_id(bca.create_event("RFQ accepted on the CHIXLIS", self.test_id))

        er_rfq_new = FixMessageExecutionReportAlgo().set_RFQ_accept_params_new(nos_chixlis_rfq)
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_new, key_parameters=self.key_params_ER_FQ, message_name='Buy side RFQ reply NEW on CHIXLIS', direction=self.ToQuod)

        er_rfq_restated = FixMessageExecutionReportAlgo().set_RFQ_accept_params_restated(er_rfq_new).change_parameters({"OrderQty": self.qty})
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_restated, key_parameters=self.key_params_ER_FQ, message_name='Buy side RFQ reply RESTATED on CHIXLIS', direction=self.ToQuod)
        # endregion

        # region Check that the RFQ canceled on the TRQL
        case_id_4 = bca.create_event("RFQ cancel on the TRQL", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_4)

        ocr_rfq_canceled = FixMessageOrderCancelRequestAlgo().set_cancel_RFQ(nos_trql_rfq).change_parameter("ExDestination", self.ex_destination_trqx)
        self.fix_verifier_buy.check_fix_message_kepler(ocr_rfq_canceled, key_parameters=self.key_params_NOS_child, message_name='Buy side cancel RFQ on TRQX', direction=self.FromQuod)

        er_rfq_cancel_accepted = FixMessageExecutionReportAlgo().set_RFQ_cancel_accepted(nos_trql_rfq).change_parameter("ExDestination", self.ex_destination_trqx)
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_cancel_accepted, key_parameters=self.key_params_ER_FQ, message_name='Buy side cancel RFQ accepted on TRQX', direction=self.ToQuod)
        # endregion

        # region Check cancel dark DMA child order
        self.fix_verifier_buy.set_case_id(bca.create_event("Dark venue orders canceled", self.test_id))
        er_cancel_chixdelta_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chixdelta_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_chixdelta_order, self.key_params_ER_child, self.ToQuod, 'Buy Side ExecReport Cancel dark child DMA order on the CHIXDELTA')
        # endregion

        time.sleep(3)

        # region Check the child DMA order on the CHIXLIS
        case_id_5 = bca.create_event("Child DMA order on the CHIXLIS", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_5)

        self.nos_chixlis_order = FixMessageNewOrderSingleAlgo().set_DMA_after_RFQ_params().change_parameters(dict(ExDestination=self.ex_destination_chixlis, OrderQty=self.qty_after_trade, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.nos_chixlis_order, key_parameters=self.key_params_NOS_LIS, message_name='Buy side send child order on the CHIXLIS', direction=self.FromQuod)

        er_pending_new_dma_chixlis_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.nos_chixlis_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_chixlis_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA order on the CHIXLIS')

        er_new_dma_chixlis_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.nos_chixlis_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_chixlis_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA order on the CHIXLIS')
        # endregion

        # region Check that the parent order partially filled
        er_partial_fill_mp_dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_partial_fill)
        self.fix_verifier_sell.check_fix_message(er_partial_fill_mp_dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Partial fill')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        cancel_request_MP_Dark_order = FixMessageOrderCancelRequest(self.MP_Dark_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_MP_Dark_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_MP_Dark_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(3)
        
        # region Check that the child order on the CHIXLIS was canceled
        er_cancel_dma_chixlis_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.nos_chixlis_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_chixlis_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA order on the CHIXLIS')
        # endregion
        
        er_cancel_mp_dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_mp_dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
