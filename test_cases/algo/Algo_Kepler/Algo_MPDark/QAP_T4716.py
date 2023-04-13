import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets import constants
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRequestAlgo import FixMessageOrderCancelRequestAlgo


class QAP_T4716(TestCase):
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
        self.delay = 3000
        self.algopolicy = constants.ClientAlgoPolicy.qa_mpdark_11.value
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
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_6")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_chixlis = self.data_set.get_mic_by_name("mic_12")
        self.ex_destination_trql = self.data_set.get_mic_by_name("mic_13")
        self.ex_destination_trqx = self.data_set.get_mic_by_name("mic_2")
        self.client = self.data_set.get_client_by_name("client_4")
        self.listing_id_xpar = self.data_set.get_listing_id_by_name("listing_35")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_with_ex_destination = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        self.key_params_RFQ = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_RFQ")
        self.key_params_RFQ_MO = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_RFQ")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

        self.pre_filter = self.data_set.get_pre_filter("pre_filer_equal_D")

        self.new_reply = True
        self.restated_reply = True
        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        rfq_1_rule = rule_manager.add_NewOrdSingleRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_chixlis, self.qty, self.qty, self.new_reply, self.restated_reply)
        rfq_2_rule = rule_manager.add_NewOrdSingleRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_trql, self.qty, self.qty, self.new_reply, self.restated_reply, 4000)
        nos_1_reject_rule = rule_manager.add_NewOrderSingle_ExecutionReport_RejectWithReason(self.fix_env1.buy_side, self.client, self.ex_destination_chixlis, self.price, self.reason)
        nos_2_reject_rule = rule_manager.add_NewOrderSingle_ExecutionReport_RejectWithReason(self.fix_env1.buy_side, self.client, self.ex_destination_trql, self.price, self.reason)
        self.rule_list = [rfq_1_rule, rfq_2_rule, nos_1_reject_rule, nos_2_reject_rule]
        self.rfq_cancel_rule = rule_manager.add_OrderCancelRequestRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_trqx, True)
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.MP_Dark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MPDark_Kepler_params()
        self.MP_Dark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.MP_Dark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, ClientAlgoPolicyID=self.algopolicy))
        self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order, case_id_1)

        time.sleep(4)
        rule_manager.remove_rule(self.rfq_cancel_rule)
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
        self.fix_verifier_buy.check_fix_message_kepler(ocr_rfq_canceled, key_parameters=self.key_params_with_ex_destination, message_name='Buy side cancel RFQ on TRQX', direction=self.FromQuod)

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

        time.sleep(3)

        # region Check that parent order is Eliminated
        er_eliminate_mp_dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_eliminate)
        self.fix_verifier_sell.check_fix_message(er_eliminate_mp_dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Eliminate')
        # endregion

        # region Check RFQs
        case_id_2 = bca.create_event("Check that 3 RFQs was received", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_2)
        self.fix_verifier_buy.check_fix_message_sequence([nos_chixlis_rfq, nos_trql_rfq, self.nos_chixlis_order, nos_trql_rfq], key_parameters_list=[None, None, None, None], direction=self.FromQuod, pre_filter=self.pre_filter)
        # endregion

        time.sleep(6)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
