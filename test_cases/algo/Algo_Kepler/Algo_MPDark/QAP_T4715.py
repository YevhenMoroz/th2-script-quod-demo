import os
import time
from pathlib import Path

from test_framework.algo_formulas_manager import AlgoFormulasManager
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets import constants
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRequestAlgo import FixMessageOrderCancelRequestAlgo
from test_framework.read_log_wrappers.algo_messages.ReadLogMessageAlgo import ReadLogMessageAlgo
from test_framework.read_log_wrappers.algo.ReadLogVerifierAlgo import ReadLogVerifierAlgo
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager


class QAP_T4715(TestCase):
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
        self.qty = 100000
        self.price = 20
        self.reason = 99
        self.weight_chix = 6
        self.weight_bats = 4
        self.qty_chix_child, self.qty_bats_child = AlgoFormulasManager.get_child_qty_on_venue_weights(self.qty, None, self.weight_chix, self.weight_bats)
        self.algopolicy = constants.ClientAlgoPolicy.qa_mpdark_15.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
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
        self.ex_destination_chixlis = self.data_set.get_mic_by_name("mic_12")
        self.ex_destination_trql = self.data_set.get_mic_by_name("mic_13")
        self.ex_destination_bats = self.data_set.get_mic_by_name("mic_4")
        self.ex_destination_chix = self.data_set.get_mic_by_name("mic_5")
        self.ex_destination_trqx = self.data_set.get_mic_by_name("mic_2")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account_bats = self.data_set.get_account_by_name("account_7")
        self.account_chix = self.data_set.get_account_by_name("account_8")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        self.key_params_RFQ = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_RFQ")
        self.key_params_RFQ_MO = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_RFQ")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

        self.new_reply = True
        self.restated_reply = True
        self.rule_list = []

        self.pre_filter = self.data_set.get_pre_filter("pre_filer_equal_D")

        # region Read log verifier params
        self.log_verifier_by_name = constants.ReadLogVerifiers.log_319_check_order_event.value
        self.read_log_verifier = ReadLogVerifierAlgo(self.log_verifier_by_name, report_id)
        self.key_params_readlog = self.data_set.get_verifier_key_parameters_by_name("key_params_log_319_check_order_event")
        # endregion

        # region Compare message params
        self.text = "skipping LIS phase"
        # endregion
        
    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        rfq_1_rule = rule_manager.add_NewOrdSingleRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_chixlis, self.qty, self.qty, self.new_reply, self.restated_reply)
        rfq_2_rule = rule_manager.add_NewOrdSingleRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_trql, self.qty, self.qty, self.new_reply, self.restated_reply)
        nos_1_reject_rule = rule_manager.add_NewOrderSingle_ExecutionReport_RejectWithReason(self.fix_env1.buy_side, self.client, self.ex_destination_chixlis, self.price, self.reason)
        nos_2_reject_rule = rule_manager.add_NewOrderSingle_ExecutionReport_RejectWithReason(self.fix_env1.buy_side, self.client, self.ex_destination_trql, self.price, self.reason)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_chix, self.ex_destination_chix, self.price)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_bats, self.ex_destination_bats, self.price)
        ocr_1_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_chix, self.ex_destination_chix, True)
        ocr_2_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_bats, self.ex_destination_bats, True)
        self.rule_list = [rfq_1_rule, rfq_2_rule, nos_1_reject_rule, nos_2_reject_rule, nos_1_rule, nos_2_rule, ocr_1_rule, ocr_2_rule]
        self.rfq_cancel_rule = rule_manager.add_OrderCancelRequestRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_trqx, True)
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.MP_Dark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MPDark_Kepler_params()
        self.MP_Dark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.MP_Dark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, ClientAlgoPolicyID=self.algopolicy))
        
        responce = self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order, case_id_1)

        time.sleep(4)
        rule_manager.remove_rule(self.rfq_cancel_rule)

        parent_MP_Dark_order_id = responce[0].get_parameter('ExecID')
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.MP_Dark_order, key_parameters=self.key_params_NOS_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region RFQ send to CHIX LIS UK
        nos_chixlis_rfq = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.qty, ExDestination=self.ex_destination_chixlis, Instrument='*'))
        # endregion

        # region RFQ send to TURQUOISE LIS
        nos_trql_rfq = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.qty, ExDestination=self.ex_destination_trql, Instrument='*'))
        # endregion

        # region chixlist rfq accepted
        case_id_3 = bca.create_event("RFQ accepted on CHIXLIS", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_3)

        er_rfq_new_trqxlis_chixlis = FixMessageExecutionReportAlgo().set_RFQ_accept_params_new(nos_chixlis_rfq)
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_new_trqxlis_chixlis, key_parameters=self.key_params_RFQ, message_name='Buy side RFQ reply NEW on CHIXLIS', direction=self.ToQuod)

        er_rfq_restated_trqxlis_chixlis = FixMessageExecutionReportAlgo().set_RFQ_accept_params_restated(er_rfq_new_trqxlis_chixlis).change_parameters({"OrderQty": self.qty})
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_restated_trqxlis_chixlis, key_parameters=self.key_params_RFQ, message_name='Buy side RFQ reply RESTATED on CHIXLIS', direction=self.ToQuod)
        # endregion

        # region quote canceled on TRQX
        case_id_4 = bca.create_event("RFQ cancel on TRQX", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_4)

        ocr_rfq_canceled = FixMessageOrderCancelRequestAlgo().set_cancel_RFQ(nos_trql_rfq).change_parameter("ExDestination", "TRQX")
        self.fix_verifier_buy.check_fix_message_kepler(ocr_rfq_canceled, key_parameters=self.key_params_NOS_child, message_name='Buy side cancel RFQ on TRQX', direction=self.FromQuod)

        # TRQX accepted cancel rfq
        er_rfq_cancel_accepted = FixMessageExecutionReportAlgo().set_RFQ_cancel_accepted(nos_trql_rfq).change_parameter("ExDestination", "TRQX")
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_cancel_accepted, key_parameters=self.key_params_RFQ, message_name='Buy side cancel RFQ accepted on TRQX', direction=self.ToQuod)
        # endregion

        # region MO on Venue ChixLis
        case_id_5 = bca.create_event("MO order on CHIXLIS", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_5)

        self.nos_chixlis_order = FixMessageNewOrderSingleAlgo().set_DMA_after_RFQ_params()
        self.nos_chixlis_order.change_parameters(dict(OrderQty=self.qty))
        self.fix_verifier_buy.check_fix_message_kepler(self.nos_chixlis_order, key_parameters=self.key_params_RFQ_MO, message_name='Buy side send MO on CHIXLIS', direction=self.FromQuod)

        er_reject_dma_chixlis_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.nos_chixlis_order, self.gateway_side_buy, self.status_reject)
        self.fix_verifier_buy.check_fix_message_kepler(er_reject_dma_chixlis_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Reject child DMA order on venue CHIXLIS")
        # endregion

        # region trql rfq accepted
        case_id_3 = bca.create_event("RFQ accepted on TRQXLIS", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_3)

        er_rfq_new_trqxlis = FixMessageExecutionReportAlgo().set_RFQ_accept_params_new(nos_trql_rfq)
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_new_trqxlis, key_parameters=self.key_params_RFQ, message_name='Buy side RFQ reply NEW on TRQXLIS', direction=self.ToQuod)

        er_rfq_restated_trqxlis = FixMessageExecutionReportAlgo().set_RFQ_accept_params_restated(er_rfq_new_trqxlis).change_parameters({"OrderQty": self.qty})
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_restated_trqxlis, key_parameters=self.key_params_RFQ, message_name='Buy side RFQ reply RESTATED on TRQXLIS', direction=self.ToQuod)
        # endregion

        # region MO on Venue TRQXLIS
        case_id_5 = bca.create_event("MO order on TRQXLIS", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_5)

        self.nos_trqxlis_order = FixMessageNewOrderSingleAlgo().set_DMA_after_RFQ_params()
        self.nos_trqxlis_order.change_parameters(dict(OrderQty=self.qty))
        self.fix_verifier_buy.check_fix_message_kepler(self.nos_trqxlis_order, key_parameters=self.key_params_RFQ_MO, message_name='Buy side send MO on TRQXLIS', direction=self.FromQuod)

        er_reject_dma_trqxlis_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.nos_trqxlis_order, self.gateway_side_buy, self.status_reject)
        self.fix_verifier_buy.check_fix_message_kepler(er_reject_dma_trqxlis_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Reject child DMA order on venue TRQXLIS")
        # endregion

        # region Check Read log
        time.sleep(70)

        compare_message = ReadLogMessageAlgo().set_compare_message_for_check_order_event()
        compare_message.change_parameters(dict(OrderId=parent_MP_Dark_order_id, Text=self.text))

        self.read_log_verifier.set_case_id(bca.create_event("Check that LIS phase is skipping", self.test_id))
        self.read_log_verifier.check_read_log_message(compare_message, self.key_params_readlog)
        # endregion

        # region Check 1 child DMA order on venue CHIX DARKPOOL UK
        self.fix_verifier_buy.set_case_id(bca.create_event("Dark child DMA orders", self.test_id))

        self.dma_chix_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_chix_order.change_parameters(dict(Account=self.account_chix, ExDestination=self.ex_destination_chix, OrderQty=self.qty_chix_child))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_chix_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order on venue CHIX DARKPOOL UK')

        er_pending_new_dma_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chix_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_chix_order_params.change_parameters(dict(ExDestination=self.ex_destination_chix))
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_chix_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order on venue CHIX DARKPOOL UK')

        er_new_dma_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chix_order, self.gateway_side_buy, self.status_new)
        er_new_dma_chix_order_params.change_parameters(dict(ExDestination=self.ex_destination_chix))
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_chix_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order on venue CHIX DARKPOOL UK')
        # endregion

        # region Check 1 child DMA order on venue BATS DARKPOOL UK
        self.dma_bats_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_bats_order.change_parameters(dict(Account=self.account_bats, ExDestination=self.ex_destination_bats, OrderQty=self.qty_bats_child))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_bats_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 2 order on venue BATS DARKPOOL UK')

        er_pending_new_dma_bats_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_bats_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_bats_order_params.change_parameters(dict(ExDestination=self.ex_destination_bats))
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_bats_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 2 order on venue BATS DARKPOOL UK')

        er_new_dma_bats_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_bats_order, self.gateway_side_buy, self.status_new)
        er_new_dma_bats_order_params.change_parameters(dict(ExDestination=self.ex_destination_bats))
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_bats_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 2 order on venue BATS DARKPOOL UK')
        # endregion

        # region Check RFQs
        case_id_2 = bca.create_event("Check that 3 RFQs was received", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_2)
        self.fix_verifier_buy.check_fix_message_sequence_kepler([nos_chixlis_rfq, nos_trql_rfq, self.nos_chixlis_order, nos_trql_rfq], key_parameters_list=[None, None, None, None], direction=self.FromQuod, pre_filter=self.pre_filter)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        cancel_request_MP_Dark_order = FixMessageOrderCancelRequest(self.MP_Dark_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_MP_Dark_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_MP_Dark_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel first dma child order
        er_cancel_dma_chix_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chix_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_chix_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 1 order on venue CHIX DARKPOOL UK")
        # endregion

        # region check cancel second dma child order
        er_cancel_dma_bats_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_bats_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_bats_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 2 order on venue BATS DARKPOOL UK")
        # endregion

        er_cancel_mp_dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_mp_dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        time.sleep(5)

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
