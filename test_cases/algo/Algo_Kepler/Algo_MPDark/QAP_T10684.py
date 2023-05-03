import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRejectReportAlgo import FixMessageOrderCancelRejectReportAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRequestAlgo import FixMessageOrderCancelRequestAlgo


class QAP_T10684(TestCase):
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
        self.qty = 400000
        self.price = 20
        self.delay_for_rfq = 30000
        self.algopolicy = constants.ClientAlgoPolicy.qa_mpdark_rr_1.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
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
        self.ex_destination_tqlis = self.data_set.get_mic_by_name("mic_20")
        self.ex_destination_chix = self.data_set.get_mic_by_name("mic_5")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account_chix = self.data_set.get_account_by_name("account_8")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        self.key_params_OCR_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_OCR_child")
        self.key_params_ER_cancel_reject_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_cancel_reject_parent")
        self.key_params_ER_RFQ = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_RFQ")
        self.key_params_rfq_cancel = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_RFQ_canceled")
        self.key_params_ER_RFQ = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_RFQ")
        # endregion

        self.new_reply = True
        self.restated_reply = True
        self.rule_list = []

        self.pre_filter = self.data_set.get_pre_filter('pre_filer_equal_D')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_chix, self.ex_destination_chix, self.price)
        rfq_rule_chix_lis = rule_manager.add_NewOrdSingleRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_chixlis, self.qty, self.qty, self.new_reply, self.restated_reply, self.delay_for_rfq)
        rfq_rule_trqx = rule_manager.add_NewOrdSingleRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_trql, self.qty, self.qty, self.new_reply, self.restated_reply, self.delay_for_rfq)
        self.rule_list = [nos_1_rule, rfq_rule_chix_lis, rfq_rule_trqx]
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.MP_Dark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MPDark_Kepler_params()
        self.MP_Dark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.MP_Dark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, ClientAlgoPolicyID=self.algopolicy, Instrument=self.instrument))

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

        # region Check RFQs
        case_id_2 = bca.create_event("Create RFQs on buy side", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_2)

        # region Check that the RFQ send to CHIX LIS UK
        nos_chixlis_rfq = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.qty, ExDestination=self.ex_destination_chixlis, Instrument='*'))
        self.fix_verifier_buy.check_fix_message_kepler(nos_chixlis_rfq, key_parameters=self.key_params_NOS_child, message_name='Buy side RFQ on CHIXLIS', direction=self.FromQuod)
        # endregion

        # region Check that the RFQ send to TURQUOISE LIS
        nos_trql_rfq = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.qty, ExDestination=self.ex_destination_trql, Instrument='*'))
        self.fix_verifier_buy.check_fix_message_kepler(nos_trql_rfq, key_parameters=self.key_params_NOS_child, message_name='Buy side RFQ on TQLIS')
        # endregion

        # region Check 1 child DMA order on venue CHIX DARKPOOL UK
        self.fix_verifier_buy.set_case_id(bca.create_event("Dark child DMA orders", self.test_id))

        self.dma_chix_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_chix_order.change_parameters(dict(Account=self.account_chix, ExDestination=self.ex_destination_chix, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_chix_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        time.sleep(5)

        er_pending_new_dma_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chix_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_chix_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chix_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_chix_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        time.sleep(30)

        # region Check that the 1st child expires
        order_cancel_request_dma_chix_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_chix_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_chix_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 1 order')
        # endregion

        # region Check the Cancel requests on the RFQs
        self.fix_verifier_buy.set_case_id(bca.create_event(" Check the Cancel requests on the RFQs", self.test_id))

        # TRQX received cancel rfq
        ocr_rfq_canceled_trqx = FixMessageOrderCancelRequestAlgo().set_cancel_RFQ(nos_trql_rfq).change_parameter("ExDestination", self.ex_destination_trqx).add_header().add_DeliverToCompID(self.ex_destination_tqlis)
        self.fix_verifier_buy.check_fix_message_kepler(ocr_rfq_canceled_trqx, key_parameters=self.key_params_rfq_cancel, message_name='Buy side cancel RFQ on TRQX', direction=self.FromQuod, ignored_fields=['trailer'])

        # CHIXLIS received cancel rfq
        ocr_rfq_canceled_chix = FixMessageOrderCancelRequestAlgo().set_cancel_RFQ(nos_chixlis_rfq).change_parameter("ExDestination", self.ex_destination_trqx).add_header().add_DeliverToCompID(self.ex_destination_chixlis)
        self.fix_verifier_buy.check_fix_message_kepler(ocr_rfq_canceled_chix, key_parameters=self.key_params_NOS_child, message_name='Buy side cancel RFQ on LISX', direction=self.FromQuod)
        # endregion

        # region Check that the Cancel request on child is timed out
        self.fix_verifier_buy.set_case_id(bca.create_event("Check that the Cancel request on child is timed out", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([er_pending_new_dma_chix_order_params, er_new_dma_chix_order_params], [self.key_params_ER_child, self.key_params_ER_child], self.ToQuod, pre_filter=None)
        # endregion

        # region Check that the CHIXLIS RFQ accepted
        self.fix_verifier_buy.set_case_id(bca.create_event("RFQ accepted on CHIXLIS", self.test_id))

        er_rfq_new_chixlis = FixMessageExecutionReportAlgo().set_RFQ_accept_params_new(nos_chixlis_rfq)
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_new_chixlis, key_parameters=self.key_params_ER_RFQ, message_name='Buy side RFQ reply NEW on CHIXLIS', direction=self.ToQuod)

        er_rfq_restated_chixlis = FixMessageExecutionReportAlgo().set_RFQ_accept_params_restated(er_rfq_new_chixlis).change_parameters({"OrderQty": self.qty})
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_restated_chixlis, key_parameters=self.key_params_ER_RFQ, message_name='Buy side RFQ reply RESTATED on CHIXLIS', direction=self.ToQuod)
        # endregion

        # region Check that the TRQL RFQ accepted
        self.fix_verifier_buy.set_case_id(bca.create_event("RFQ accepted on TRQX LIS", self.test_id))

        er_rfq_new_trql = FixMessageExecutionReportAlgo().set_RFQ_accept_params_new(nos_trql_rfq)
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_new_trql, key_parameters=self.key_params_ER_RFQ, message_name='Buy side RFQ reply NEW on TRQL', direction=self.ToQuod)

        er_rfq_restated_trql = FixMessageExecutionReportAlgo().set_RFQ_accept_params_restated(er_rfq_new_trql).change_parameters({"OrderQty": self.qty})
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_restated_trql, key_parameters=self.key_params_ER_RFQ, message_name='Buy side RFQ reply RESTATED on TRQL', direction=self.ToQuod)
        # endregion

        # region Check that there are no LIS childs
        self.fix_verifier_buy.set_case_id(bca.create_event("Check that there are no LIS childs", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([nos_chixlis_rfq, nos_trql_rfq, self.dma_chix_order], [self.key_params_NOS_child, self.key_params_NOS_child, self.key_params_NOS_child], self.FromQuod, pre_filter=self.pre_filter)
        # endregion

        time.sleep(10)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)















