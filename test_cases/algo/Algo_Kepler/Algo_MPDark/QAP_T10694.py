import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRequestAlgo import FixMessageOrderCancelRequestAlgo
from test_framework.read_log_wrappers.algo.ReadLogVerifierAlgo import ReadLogVerifierAlgo


class QAP_T10694(TestCase):
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
        self.qty = 4000000
        self.price = 20
        self.delay_for_rfq_accept = 14000
        self.delay_for_rfq_cancel = 7000
        self.reason = 99
        self.algopolicy = constants.ClientAlgoPolicy.qa_mpdark_rr_1.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_reject = Status.Reject
        self.status_eliminate = Status.Eliminate
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
        self.ex_destination_bats = self.data_set.get_mic_by_name("mic_4")
        self.ex_destination_chix = self.data_set.get_mic_by_name("mic_5")
        self.ex_destination_cboe = self.data_set.get_mic_by_name("mic_6")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account_bats = self.data_set.get_account_by_name("account_7")
        self.account_chix = self.data_set.get_account_by_name("account_8")
        self.account_cboe = self.data_set.get_account_by_name("account_9")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        self.key_params_OCR_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_OCR_child")
        self.key_params_ER_RFQ = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_RFQ")
        self.key_params_ER_reject_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_cancel_reject_child")
        # endregion

        # region Read log verifier params
        self.log_verifier_by_name = constants.ReadLogVerifiers.log_319_check_order_event.value
        self.read_log_verifier = ReadLogVerifierAlgo(self.log_verifier_by_name, report_id)
        self.key_params_readlog = self.data_set.get_verifier_key_parameters_by_name("key_params_log_319_check_order_event")
        # endregion

        self.pre_filter = self.data_set.get_pre_filter("pre_filer_equal_D")
        self.new_reply = True
        self.restated_reply = True
        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        rfq_rule = rule_manager.add_NewOrdSingleRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_chixlis, self.qty, self.qty, self.new_reply, self.restated_reply, self.delay_for_rfq_accept)
        rfq_ocr_rule = rule_manager.add_OrderCancelRequestRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_trqx, True, self.delay_for_rfq_cancel)
        nos_1_reject_rule = rule_manager.add_NewOrderSingle_ExecutionReport_RejectWithReason(self.fix_env1.buy_side, self.account_chix, self.ex_destination_chix, self.price, self.reason)
        nos_2_reject_rule = rule_manager.add_NewOrderSingle_ExecutionReport_RejectWithReason(self.fix_env1.buy_side, self.account_bats, self.ex_destination_bats, self.price, self.reason)
        nos_3_reject_rule = rule_manager.add_NewOrderSingle_ExecutionReport_RejectWithReason(self.fix_env1.buy_side, self.account_cboe, self.ex_destination_cboe, self.price, self.reason)
        self.rule_list = [rfq_rule, rfq_ocr_rule, nos_1_reject_rule, nos_2_reject_rule, nos_3_reject_rule]
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.MP_Dark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MPDark_Kepler_params()
        self.MP_Dark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.MP_Dark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, ClientAlgoPolicyID=self.algopolicy, Instrument=self.instrument))

        self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.MP_Dark_order, self.key_params_NOS_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        time.sleep(30)

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

        # region Check child DMA order on venue CHIX DARKPOOL UK
        self.fix_verifier_buy.set_case_id(bca.create_event("Dark child DMA orders", self.test_id))

        self.dma_chix_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_chix_order.change_parameters(dict(Account=self.account_chix, ExDestination=self.ex_destination_chix, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_chix_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_reject_dma_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chix_order, self.gateway_side_buy, self.status_reject)
        self.fix_verifier_buy.check_fix_message_kepler(er_reject_dma_chix_order_params, key_parameters=self.key_params_ER_reject_child, direction=self.ToQuod, message_name='Buy side ExecReport Reject Child DMA 1 order')
        # endregion

        # region Check child DMA order on venue BATS DARKPOOL UK
        self.dma_bats_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_bats_order.change_parameters(dict(Account=self.account_bats, ExDestination=self.ex_destination_bats, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_bats_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 2 order')

        er_reject_dma_bats_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_bats_order, self.gateway_side_buy, self.status_reject)
        self.fix_verifier_buy.check_fix_message_kepler(er_reject_dma_bats_order_params, key_parameters=self.key_params_ER_reject_child, direction=self.ToQuod, message_name='Buy side ExecReport Reject Child DMA 2 order')
        # endregion

        # region Check child DMA order on venue CBOE DARKPOOL EU
        self.dma_cboe_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_cboe_order.change_parameters(dict(Account=self.account_cboe, ExDestination=self.ex_destination_cboe, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_cboe_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 3 order')

        er_reject_dma_cboe_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_cboe_order, self.gateway_side_buy, self.status_reject)
        self.fix_verifier_buy.check_fix_message_kepler(er_reject_dma_cboe_order_params, key_parameters=self.key_params_ER_reject_child, direction=self.ToQuod, message_name='Buy side ExecReport Reject Child DMA 3 order')
        # endregion

        # region Check that parent order eliminated
        er_eliminate_mp_dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_eliminate)
        self.fix_verifier_sell.check_fix_message(er_eliminate_mp_dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Eliminate')
        # endregion

        # region Check that the chixlis rfq accepted
        case_id_3 = bca.create_event("RFQ accepted on CHIXLIS", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_3)

        er_rfq_new = FixMessageExecutionReportAlgo().set_RFQ_accept_params_new(nos_chixlis_rfq)
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_new, key_parameters=self.key_params_ER_RFQ, message_name='Buy side RFQ reply NEW on CHIXLIS', direction=self.ToQuod)

        er_rfq_restated = FixMessageExecutionReportAlgo().set_RFQ_accept_params_restated(er_rfq_new).change_parameters({"OrderQty": self.qty})
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_restated, key_parameters=self.key_params_ER_RFQ, message_name='Buy side RFQ reply RESTATED on CHIXLIS', direction=self.ToQuod)
        # endregion

        # region Check that the RFQ canceled on TRQX
        self.fix_verifier_buy.set_case_id(bca.create_event("RFQ cancel on TRQX", self.test_id))

        ocr_rfq_canceled = FixMessageOrderCancelRequestAlgo().set_cancel_RFQ(nos_trql_rfq).change_parameter("ExDestination", self.ex_destination_trqx)
        self.fix_verifier_buy.check_fix_message_kepler(ocr_rfq_canceled, key_parameters=self.key_params_NOS_child, message_name='Buy side cancel RFQ on TRQX', direction=self.FromQuod)

        er_rfq_cancel_accepted = FixMessageExecutionReportAlgo().set_RFQ_cancel_accepted(nos_trql_rfq).change_parameter("ExDestination", self.ex_destination_trqx)
        self.fix_verifier_buy.check_fix_message_kepler(er_rfq_cancel_accepted, key_parameters=self.key_params_ER_RFQ, message_name='Buy side cancel RFQ accepted on TRQX', direction=self.ToQuod)
        # endregion

        # region Check those are no unexpected childs
        self.fix_verifier_buy.set_case_id(bca.create_event("Check those are no unexpected childs", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([nos_chixlis_rfq, nos_trql_rfq, self.dma_chix_order, self.dma_bats_order, self.dma_cboe_order], [self.key_params_NOS_child, self.key_params_NOS_child, self.key_params_NOS_child, self.key_params_NOS_child, self.key_params_NOS_child],
                                                         self.FromQuod, pre_filter=self.pre_filter)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

