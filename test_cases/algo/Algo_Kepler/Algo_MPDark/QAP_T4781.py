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
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRequestAlgo import FixMessageOrderCancelRequestAlgo
from test_framework.read_log_wrappers.algo.ReadLogVerifierAlgo import ReadLogVerifierAlgo
from test_framework.read_log_wrappers.algo_messages.ReadLogMessageAlgo import ReadLogMessageAlgo


class QAP_T4781(TestCase):
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
        self.qty = 3000000
        self.traded_qty = 2995000
        self.inc_qty = 4000000
        self.qty_after_trade = self.qty - self.traded_qty
        self.new_leaves_qty = self.inc_qty - self.traded_qty
        self.price = 20
        self.delay_for_trade = 0
        self.delay_for_rfq = 10000
        self.algopolicy = constants.ClientAlgoPolicy.qa_mpdark_16.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        self.status_partial_fill = Status.PartialFill
        self.status_cancel_replace = Status.CancelReplace
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
        self.ex_destination_tqlis = self.data_set.get_mic_by_name("mic_20")
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
        self.key_params_ER_RFQ = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_RFQ")
        self.key_params_ER_RFQ_with_qty = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_RFQ_with_qty")
        self.key_params_rfq_cancel = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_RFQ_canceled")
        # endregion

        self.pre_filter = self.data_set.get_pre_filter("pre_filer_equal_F")
        self.pre_filter['header']['DeliverToCompID'] = (self.ex_destination_tqlis, "EQUAL")

        self.new_reply = True
        self.restated_reply = True
        self.rule_list = []

        # region Read log verifier params
        self.log_verifier_by_name = constants.ReadLogVerifiers.log_319_cancel_child.value
        self.read_log_verifier = ReadLogVerifierAlgo(self.log_verifier_by_name, report_id)
        # endregion

        # region Compare message params
        self.qty_canceling_child = 1
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_chixdelta, self.ex_destination_chixdelta, self.price)
        ocr_1_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_chixdelta, self.ex_destination_chixdelta, True)
        rfq_1_rule = rule_manager.add_NewOrdSingleRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_chixlis, self.qty, self.qty, self.new_reply, self.restated_reply, self.delay_for_rfq)
        rfq_cancel_rule = rule_manager.add_OrderCancelRequestRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_trqx, True)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.client, self.ex_destination_chixlis, self.price)
        nos_trade_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(self.fix_env1.buy_side, self.client, self.ex_destination_chixlis, self.price, self.price, self.qty, self.traded_qty, 0)
        ocr_2_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.client, self.ex_destination_chixlis, True)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(self.fix_env1.buy_side, False)
        rfq_2_rule = rule_manager.add_NewOrdSingleRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_chixlis, self.new_leaves_qty, self.new_leaves_qty, self.new_reply, self.restated_reply)
        self.rule_list = [nos_1_rule, rfq_1_rule, rfq_cancel_rule, ocr_1_rule, nos_2_rule, nos_trade_rule, ocr_2_rule, ocrr_rule, rfq_2_rule]
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.MP_Dark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MPDark_Kepler_params()
        self.MP_Dark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.MP_Dark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, ClientAlgoPolicyID=self.algopolicy, Instrument=self.instrument))

        responce = self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order, case_id_1)

        parent_MP_Dark_order_id = responce[0].get_parameter('ExecID')

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
        case_id_2 = bca.create_event("Create 1st RFQs on buy side", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_2)

        # region check that RFQ send to CHIX LIS UK
        nos_1_chixlis_rfq = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.qty, ExDestination=self.ex_destination_chixlis, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(nos_1_chixlis_rfq, key_parameters=self.key_params_NOS_child, message_name='Buy side 1st RFQ on CHIXLIS')
        # endregion

        # region check that RFQ send to TURQUOISE LIS
        nos_1_trql_rfq = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.qty, ExDestination=self.ex_destination_trql, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(nos_1_trql_rfq, key_parameters=self.key_params_NOS_child, message_name='Buy side 1st RFQ on TQLIS')
        # endregion

        # region Check the 1st dark child order
        self.fix_verifier_buy.set_case_id(bca.create_event("Algo generates a 1st child order on the Dark venue", self.test_id))

        self.dma_1_chixdelta_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_1_chixdelta_order.change_parameters(dict(Account=self.account_chixdelta, ExDestination=self.ex_destination_chixdelta, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(self.dma_1_chixdelta_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle 1st dark child on the CHIXDELTA')

        er_pending_new_dma_1_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_chixdelta_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_1_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew 1st dark child on the CHIXDELTA')

        er_new_dma_1_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_chixdelta_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_1_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New dark 1st child on the CHIXDELTA')
        # endregion

        # region Check that the rfq on the CHIXLIS was accepted
        case_id_3 = bca.create_event("1st RFQ accepted on CHIXLIS", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_3)

        er_1_rfq_chixlis_new = FixMessageExecutionReportAlgo().set_RFQ_accept_params_new(nos_1_chixlis_rfq)
        self.fix_verifier_buy.check_fix_message(er_1_rfq_chixlis_new, key_parameters=self.key_params_ER_RFQ, message_name='Buy side RFQ reply NEW on CHIXLIS', direction=self.ToQuod)

        er_1_rfq_chixlis_restated = FixMessageExecutionReportAlgo().set_RFQ_accept_params_restated(er_1_rfq_chixlis_new).change_parameters({"OrderQty": self.qty})
        self.fix_verifier_buy.check_fix_message(er_1_rfq_chixlis_restated, key_parameters=self.key_params_ER_RFQ, message_name='Buy side RFQ reply RESTATED on CHIXLIS', direction=self.ToQuod)
        # endregion

        # region Check that the rfq on the TRQL was canceled
        case_id_4 = bca.create_event("1st RFQ cancel on TRQX", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_4)

        self.ocr_1_rfq_trql_canceled = FixMessageOrderCancelRequestAlgo().set_cancel_RFQ(nos_1_trql_rfq).change_parameter("ExDestination", "TRQX")
        self.fix_verifier_buy.check_fix_message(self.ocr_1_rfq_trql_canceled, key_parameters=self.key_params_NOS_child, message_name='Buy side cancel RFQ on TRQX', direction=self.FromQuod)

        er_1_rfq_trql_cancel_accepted = FixMessageExecutionReportAlgo().set_RFQ_cancel_accepted(nos_1_trql_rfq).change_parameter("ExDestination", "TRQX")
        self.fix_verifier_buy.check_fix_message(er_1_rfq_trql_cancel_accepted, key_parameters=self.key_params_ER_RFQ, message_name='Buy side cancel RFQ accepted on TRQX', direction=self.ToQuod)
        # endregion

        # region Check that the 1st dark child was cancelled
        self.fix_verifier_buy.set_case_id(bca.create_event("1st dark child was cancelled on the CHIXDELTA", self.test_id))

        er_cancel_dma_1_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_chixdelta_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_1_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel dark 1st child on the CHIXDELTA')
        # endregion

        # region Check the 1st child order on the CHIXLIS
        case_id_5 = bca.create_event("Algo generates a 1st child order on the LIS venue", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_5)

        dma_1_chixlis_order = FixMessageNewOrderSingleAlgo().set_DMA_after_RFQ_params()
        dma_1_chixlis_order.change_parameters(dict(ExDestination=self.ex_destination_chixlis, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(dma_1_chixlis_order, key_parameters=self.key_params_NOS_LIS, message_name='Buy side NewOrderSingle 1st LIS child order on the CHIXLIS', direction=self.FromQuod)

        er_pending_new_dma_1_chixlis_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_chixlis_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_1_chixlis_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew 1st Child order on the CHIXLIS')

        er_new_dma_1_chixlis_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_chixlis_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_1_chixlis_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New 1st Child order on the CHIXLIS')

        er_partial_fill_dma_1_chixlis_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_chixlis_order, self.gateway_side_buy, self.status_partial_fill)
        self.fix_verifier_buy.check_fix_message(er_partial_fill_dma_1_chixlis_order, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Partial fill 1st LIS Child order on the CHIXLIS')

        time.sleep(2)

        er_cancel_dma_1_chixlis_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_chixlis_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_1_chixlis_order, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel 1st LIS Child order on the CHIXLIS')
        # endregion

        # region Check the 2nd dark child order
        self.fix_verifier_buy.set_case_id(bca.create_event("Algo generates a 2nd child order on the Dark venue", self.test_id))

        self.dma_2_chixdelta_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_2_chixdelta_order.change_parameters(dict(Account=self.account_chixdelta, ExDestination=self.ex_destination_chixdelta, OrderQty=self.qty_after_trade, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(self.dma_2_chixdelta_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle 2nd dark child on the CHIXDELTA')

        er_pending_new_dma_2_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_chixdelta_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_2_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew 2nd dark child on the CHIXDELTA')

        er_new_dma_2_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_chixdelta_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_2_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New dark 2nd child on the CHIXDELTA')
        # endregion

        # region Check Partial fill the parent order
        er_partial_fill_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_partial_fill)
        self.fix_verifier_sell.check_fix_message(er_partial_fill_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell Side ExecReport Partial fill')
        # endregion

        # region Modify parent qty
        case_id_3 = bca.create_event("Replace MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)

        self.MP_Dark_order_replace_params = FixMessageOrderCancelReplaceRequestAlgo(self.MP_Dark_order)
        self.MP_Dark_order_replace_params.change_parameters(dict(OrderQty=self.inc_qty))
        self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order_replace_params, case_id_3)

        time.sleep(2)

        self.fix_verifier_sell.check_fix_message(self.MP_Dark_order_replace_params, direction=self.ToQuod, message_name='Sell side OrderCancelReplaceRequest')

        er_replace_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.MP_Dark_order_replace_params, self.gateway_side_sell, self.status_cancel_replace).change_parameter("OrdStatus", "1")
        self.fix_verifier_sell.check_fix_message(er_replace_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell Side ExecReport Replace Request')
        # endregion

        # region Check cancel the 2nd dark child order
        self.fix_verifier_buy.set_case_id(bca.create_event(" Check cancel the 2nd dark child order", self.test_id))

        er_cancel_dma_2_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_chixdelta_order, self.gateway_side_buy, self.status_cancel)
        er_cancel_dma_2_chixdelta_order_params.change_parameters(dict(OrderQty=self.new_leaves_qty))
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_2_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel 2nd dark child on the CHIXDELTA')
        # endregion

        # region Check the 3rd  dark child order
        self.fix_verifier_buy.set_case_id(bca.create_event("Algo generates a 2nd child order on the Dark venue", self.test_id))

        self.dma_3_chixdelta_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_3_chixdelta_order.change_parameters(dict(Account=self.account_chixdelta, ExDestination=self.ex_destination_chixdelta, OrderQty=self.new_leaves_qty, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(self.dma_3_chixdelta_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle 2nd dark child on the CHIXDELTA')

        er_pending_new_dma_3_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_chixdelta_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_3_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew 2nd dark child on the CHIXDELTA')

        er_new_dma_3_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_chixdelta_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_3_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New dark 2nd child on the CHIXDELTA')
        # endregion

        # region Check the 2nd RFQs
        self.fix_verifier_buy.set_case_id(bca.create_event("Create 2nd RFQs on buy side", self.test_id))

        # region check that RFQ send to CHIX LIS UK
        nos_2_chixlis_rfq = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.new_leaves_qty, ExDestination=self.ex_destination_chixlis, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(nos_2_chixlis_rfq, key_parameters=self.key_params_NOS_child, message_name='Buy side 2nd RFQ on CHIXLIS')
        # endregion

        # region check that RFQ send to TURQUOISE LIS
        self.nos_2_trql_rfq = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.new_leaves_qty, ExDestination=self.ex_destination_trql, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(self.nos_2_trql_rfq, key_parameters=self.key_params_NOS_child, message_name='Buy side 2nd RFQ on TQLIS')
        # endregion

        # region Check that the 2nd rfq on the CHIXLIS was accepted
        case_id_3 = bca.create_event("2nd RFQ accepted on CHIXLIS", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_3)

        er_2_rfq_chixlis_new = FixMessageExecutionReportAlgo().set_RFQ_accept_params_new(nos_2_chixlis_rfq)
        self.fix_verifier_buy.check_fix_message(er_2_rfq_chixlis_new, key_parameters=self.key_params_ER_RFQ_with_qty, message_name='Buy side 2nd RFQ reply NEW on CHIXLIS', direction=self.ToQuod)

        er_2_rfq_chixlis_restated = FixMessageExecutionReportAlgo().set_RFQ_accept_params_restated(er_2_rfq_chixlis_new).change_parameters({"OrderQty": self.new_leaves_qty})
        self.fix_verifier_buy.check_fix_message(er_2_rfq_chixlis_restated, key_parameters=self.key_params_ER_RFQ_with_qty, message_name='Buy side 2nd RFQ reply RESTATED on CHIXLIS', direction=self.ToQuod)
        # endregion

        # region Check cancel 2nd RFQ on the TRQL
        self.fix_verifier_buy.set_case_id(bca.create_event("2nd RFQ canceled on TRQL", self.test_id))

        # TRQL accepted cancel rfq
        ocr_2_rfq_trql_canceled = FixMessageOrderCancelRequestAlgo().set_cancel_RFQ(self.nos_2_trql_rfq).change_parameter("ExDestination", self.ex_destination_trqx).add_header().add_DeliverToCompID(self.ex_destination_tqlis)

        er_2_rfq_trqx_cancel_accepted = FixMessageExecutionReportAlgo().set_RFQ_cancel_accepted(self.nos_2_trql_rfq).change_parameter("ExDestination", self.ex_destination_trqx)
        self.fix_verifier_buy.check_fix_message(er_2_rfq_trqx_cancel_accepted, key_parameters=self.key_params_ER_RFQ, message_name='Buy side cancel 2nd RFQ accepted on TRQX', direction=self.ToQuod)
        # endregion

        time.sleep(3)

        self.fix_verifier_buy.set_case_id(bca.create_event("Check that 2 rqf was canceled on trqx", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([self.ocr_1_rfq_trql_canceled, ocr_2_rfq_trql_canceled], key_parameters_list=[self.key_params_rfq_cancel, self.key_params_rfq_cancel], direction=self.FromQuod, pre_filter=self.pre_filter)
        # endregion

        # region Check that the 3rd dark child order was cancelled
        self.fix_verifier_buy.set_case_id(bca.create_event("heck that the 3rd dark child order was cancelled", self.test_id))

        er_cancel_dma_3_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_chixdelta_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_3_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel 3rd dark child on the CHIXDELTA')
        # endregion

        # region Check the 2nd child order on the CHIXLIS
        case_id_5 = bca.create_event("Algo generates a 2nd child order on the LIS venue", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_5)

        self.dma_2_chixlis_order = FixMessageNewOrderSingleAlgo().set_DMA_after_RFQ_params()
        self.dma_2_chixlis_order.change_parameters(dict(ExDestination=self.ex_destination_chixlis, Instrument=self.instrument, OrderQty=self.new_leaves_qty))
        self.fix_verifier_buy.check_fix_message(self.dma_2_chixlis_order, key_parameters=self.key_params_NOS_LIS, message_name='Buy side NewOrderSingle 2nd LIS child order on the CHIXLIS', direction=self.FromQuod)

        er_pending_new_dma_2_chixlis_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_chixlis_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_2_chixlis_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew 2nd Child order on the CHIXLIS')

        er_new_dma_2_chixlis_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_chixlis_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_2_chixlis_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New 2nd Child order on the CHIXLIS')
        # endregion

        # region Check Read log
        time.sleep(70)

        compare_message = ReadLogMessageAlgo().set_compare_message_for_check_cancel_child()
        compare_message.change_parameters(dict(OrderId=parent_MP_Dark_order_id, QtyCancelingChilds=self.qty_canceling_child))

        self.read_log_verifier.set_case_id(bca.create_event("ReadLog", self.test_id))
        self.read_log_verifier.check_read_log_message(compare_message)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        cancel_request_MP_Dark_order = FixMessageOrderCancelRequest(self.MP_Dark_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_MP_Dark_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_MP_Dark_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(2)

        # region Check that the 2nd LIS child was cancelled
        er_cancel_dma_2_chixlis_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_chixlis_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_2_chixlis_order, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel 2nd Child order on the CHIXLIS')
        # endregion

        er_cancel_mp_dark_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.MP_Dark_order_replace_params, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_mp_dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')

        # endregion
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
