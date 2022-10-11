import os
import time
from copy import deepcopy
from datetime import datetime, timedelta
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
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRequestAlgo import FixMessageOrderCancelRequestAlgo


class QAP_T4786(TestCase):
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
        self.inc_qty = 2000000
        self.price = 20
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
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
        self.ex_destination_lisx = self.data_set.get_mic_by_name("mic_12")
        self.ex_destination_trql = self.data_set.get_mic_by_name("mic_13")
        self.client = self.data_set.get_client_by_name("client_4")
        self.ex_destination_trqx = self.data_set.get_mic_by_name("mic_2")
        self.ex_destination_tqlis = self.data_set.get_mic_by_name("mic_20")
        self.ex_destination_chixlis = self.data_set.get_mic_by_name("mic_21")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_with_ex_destination = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        self.key_params_RFQ = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_RFQ")
        self.key_params_RFQ_MO = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_RFQ")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_rfq_cancel = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_RFQ_canceled")

        # endregion

        self.pre_filter = self.data_set.get_pre_filter("pre_filer_equal_F")
        self.pre_filter['header']['DeliverToCompID'] = (self.ex_destination_tqlis, "EQUAL")

        self.new_reply = True
        self.restated_reply = True
        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager()
        rfq_rule = rule_manager.add_NewOrdSingleRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_lisx, self.inc_qty, self.inc_qty, self.new_reply, self.restated_reply)
        rfq_cancel_rule = rule_manager.add_OrderCancelRequestRFQExecutionReport(self.fix_env1.buy_side, self.client, self.ex_destination_trqx, True)
        new_order_single = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.client, self.ex_destination_lisx, self.price)
        cancel_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.client, self.ex_destination_lisx, True)

        self.rule_list = [rfq_cancel_rule, new_order_single, cancel_rule, rfq_rule]
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.MP_Dark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MPDark_params()
        self.MP_Dark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.MP_Dark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price))
        self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.MP_Dark_order, key_parameters=self.key_params_NOS_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_pending)
        er_pending_new_MP_Dark_order_params.add_tag(dict(NoParty='*'))
        self.fix_verifier_sell.check_fix_message(er_pending_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_new)
        er_new_MP_Dark_order_params.add_tag(dict(NoParty='*'))
        self.fix_verifier_sell.check_fix_message(er_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        case_id_2 = bca.create_event("Create RFQ on buy side", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_2)

        # region check that RFQ send to CHIX LIS UK
        nos_chixlis_rfq = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.qty, ExDestination=self.ex_destination_lisx, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(nos_chixlis_rfq, key_parameters=self.key_params_with_ex_destination, message_name='Buy side RFQ on CHIXLIS')
        # endregion

        # region check that RFQ send to TURQUOISE LIS
        nos_trql_rfq = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.qty, ExDestination=self.ex_destination_trql, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(nos_trql_rfq, key_parameters=self.key_params_with_ex_destination, message_name='Buy side RFQ on TQLIS')
        # endregion

        # region Modify parent qty
        case_id_3 = bca.create_event("Replace MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)

        self.MP_Dark_order_replace_params = FixMessageOrderCancelReplaceRequestAlgo(self.MP_Dark_order)
        self.MP_Dark_order_replace_params.change_parameters(dict(OrderQty=self.inc_qty))
        response = self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order_replace_params, case_id_3)[0]
        expectedtime = (datetime.strptime(response.get_parameter("header")['SendingTime'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(seconds=1)).isoformat()

        time.sleep(1)

        self.fix_verifier_sell.check_fix_message(self.MP_Dark_order_replace_params, direction=self.ToQuod, message_name='Sell side OrderCancelReplaceRequest')

        er_replaced_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.MP_Dark_order_replace_params, self.gateway_side_sell, self.status_cancel_replace)
        self.fix_verifier_sell.check_fix_message(er_replaced_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell Side ExecReport Replace Request')
        # endregion


        # region quote canceled on Lis venues
        self.fix_verifier_buy.set_case_id(bca.create_event("1st RFQ canceled", self.test_id))

        # TRQX accepted cancel rfq
        ocr_rfq_canceled_trqx = FixMessageOrderCancelRequestAlgo().set_cancel_RFQ(nos_trql_rfq).change_parameter("ExDestination", self.ex_destination_trqx).add_header().add_DeliverToCompID(self.ex_destination_tqlis)
        self.fix_verifier_buy.check_fix_message(ocr_rfq_canceled_trqx, key_parameters=self.key_params_rfq_cancel, message_name='Buy side cancel RFQ on TRQX', direction=self.FromQuod, ignored_fields=['trailer'])

        er_rfq_trqx_cancel_accepted = FixMessageExecutionReportAlgo().set_RFQ_cancel_accepted(nos_trql_rfq).change_parameter("ExDestination", self.ex_destination_trqx)
        self.fix_verifier_buy.check_fix_message(er_rfq_trqx_cancel_accepted, key_parameters=self.key_params_RFQ, message_name='Buy side cancel RFQ accepted on TRQX', direction=self.ToQuod)

        # CHIXLIS accepted cancel rfq
        ocr_rfq_canceled_chix = FixMessageOrderCancelRequestAlgo().set_cancel_RFQ(nos_chixlis_rfq).change_parameter("ExDestination", self.ex_destination_trqx).add_header().add_DeliverToCompID(self.ex_destination_chixlis)
        self.fix_verifier_buy.check_fix_message(ocr_rfq_canceled_chix, key_parameters=self.key_params_with_ex_destination, message_name='Buy side cancel RFQ on LISX', direction=self.FromQuod)

        er_rfq_chix_cancel_accepted = FixMessageExecutionReportAlgo().set_RFQ_cancel_accepted(nos_chixlis_rfq).change_parameter("ExDestination", self.ex_destination_trqx)
        self.fix_verifier_buy.check_fix_message(er_rfq_chix_cancel_accepted, key_parameters=self.key_params_RFQ, message_name='Buy side cancel RFQ accepted on LISX', direction=self.ToQuod)
        # endregion



        self.fix_verifier_buy.set_case_id(bca.create_event("2st RFQ sended", self.test_id))

        # region check that second RFQ send to CHIX LIS UK
        nos_chixlis_rfq2 = deepcopy(nos_chixlis_rfq)
        nos_chixlis_rfq2.change_parameters(dict(OrderQty=self.inc_qty, TransactTime="<" + expectedtime))
        self.fix_verifier_buy.check_fix_message(nos_chixlis_rfq2, key_parameters=self.key_params_with_ex_destination, message_name='Buy side RFQ on CHIXLIS')
        # endregion

        # region check that second RFQ send to TURQUOISE LIS
        nos_trql_rfq2 = deepcopy(nos_trql_rfq)
        nos_trql_rfq2.change_parameters(dict(OrderQty=self.inc_qty, TransactTime="<" + expectedtime))
        self.fix_verifier_buy.check_fix_message(nos_trql_rfq2, key_parameters=self.key_params_with_ex_destination, message_name='Buy side RFQ on TQLIS')
        # endregion


        # region quote canceled on Lis venues second time
        self.fix_verifier_buy.set_case_id(bca.create_event("2nd RFQ canceled", self.test_id))

        # TRQX accepted cancel rfq
        ocr_rfq_canceled_trqx2 = FixMessageOrderCancelRequestAlgo().set_cancel_RFQ(nos_trql_rfq2).change_parameter("ExDestination", self.ex_destination_trqx).add_header().add_DeliverToCompID(self.ex_destination_tqlis)
        # can't check
        # self.fix_verifier_buy.check_fix_message(ocr_rfq_canceled_trqx2, key_parameters=self.key_params_rfq_cancel, message_name='Buy side cancel RFQ on TRQX', direction=self.FromQuod, ignored_fields=['trailer'])

        er_rfq_trqx_cancel_accepted2 = FixMessageExecutionReportAlgo().set_RFQ_cancel_accepted(nos_trql_rfq2).change_parameter("ExDestination", self.ex_destination_trqx)
        self.fix_verifier_buy.check_fix_message(er_rfq_trqx_cancel_accepted2, key_parameters=self.key_params_RFQ, message_name='Buy side cancel RFQ accepted on TRQX', direction=self.ToQuod)

        # CHIXLIS accepted cancel rfq
        ocr_rfq_canceled_chix2 = FixMessageOrderCancelRequestAlgo().set_cancel_RFQ(nos_chixlis_rfq2).change_parameter("ExDestination", self.ex_destination_trqx).add_header().add_DeliverToCompID(self.ex_destination_chixlis)
        self.fix_verifier_buy.check_fix_message(ocr_rfq_canceled_chix2, key_parameters=self.key_params_with_ex_destination, message_name='Buy side cancel RFQ on LISX', direction=self.FromQuod)

        er_rfq_chix_cancel_accepted2 = FixMessageExecutionReportAlgo().set_RFQ_cancel_accepted(nos_chixlis_rfq2).change_parameter("ExDestination", self.ex_destination_trqx)
        self.fix_verifier_buy.check_fix_message(er_rfq_chix_cancel_accepted2, key_parameters=self.key_params_RFQ, message_name='Buy side cancel RFQ accepted on LISX', direction=self.ToQuod)
        # endregion

        time.sleep(3)
        self.fix_verifier_buy.set_case_id(bca.create_event("Check that 2 rqf was canceled on trqx", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([ocr_rfq_canceled_trqx, ocr_rfq_canceled_trqx2], key_parameters_list=[self.key_params_rfq_cancel, self.key_params_rfq_cancel], direction=self.FromQuod,
                                                         pre_filter=self.pre_filter)

        # region MO on Venue ChixLis
        self.fix_verifier_buy.set_case_id(bca.create_event("MO order on chixlis", self.test_id))

        nos_chixlis_order = FixMessageNewOrderSingleAlgo().set_DMA_after_RFQ_params().change_parameter("OrderQty", self.inc_qty)
        self.fix_verifier_buy.check_fix_message(nos_chixlis_order, key_parameters=self.key_params_RFQ_MO, message_name='Buy side send MO on CHIXLIS', direction=self.FromQuod)

        er_pending_new_dma_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nos_chixlis_order, self.gateway_side_buy, self.status_pending)
        er_pending_new_dma_chix_order_params.change_parameters(dict(ExDestination=self.ex_destination_lisx))
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_chix_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child order')

        er_new_dma_chix_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nos_chixlis_order, self.gateway_side_buy, self.status_new)
        er_new_dma_chix_order_params.change_parameters(dict(ExDestination=self.ex_destination_lisx))
        self.fix_verifier_buy.check_fix_message(er_new_dma_chix_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child order')

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        cancel_request_MP_Dark_order = FixMessageOrderCancelRequest(self.MP_Dark_order)
        time.sleep(1)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_MP_Dark_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_MP_Dark_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        er_cancel_mp_dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_cancel)\
            .change_parameters(dict(CxlQty=self.inc_qty, OrderQty=self.inc_qty))
        er_cancel_mp_dark_order_params.add_tag(dict(SettlDate='*')).add_tag(dict(NoParty='*')).add_tag(dict(SettlType='B'))
        self.fix_verifier_sell.check_fix_message(er_cancel_mp_dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion
        rule_manager = RuleManager()
        rule_manager.remove_rules(self.rule_list)
