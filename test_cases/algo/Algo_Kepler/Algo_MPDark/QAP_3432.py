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


class QAP_3432(TestCase):
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
        # weights BATS = 60, CHIX = 30, CBOE = 10
        self.qty = 1000000
        self.qty_1_child = 6000
        self.qty_2_child = 3000
        self.qty_3_child = 1000
        self.child_price = 20
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
        self.client = self.data_set.get_client_by_name("client_4")
        self.account_bats = self.data_set.get_account_by_name("account_7")
        self.account_chix = self.data_set.get_account_by_name("account_8")
        self.account_cboe = self.data_set.get_account_by_name("account_9")
        # endregion

        # region Key parameters
        self.key_params_without_cl_ord_id_with_cl_ord_id = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_without_cl_ord_id = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        self.key_params_with_ex_destination = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager()
        # nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side,
        #                                                                        self.account_bats,
        #                                                                        self.ex_destination_bats,
        #                                                                        self.child_price)
        # nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side,
        #                                                                        self.account_chix,
        #                                                                        self.ex_destination_chix,
        #                                                                        self.child_price)
        # nos_3_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side,
        #                                                                        self.account_cboe,
        #                                                                        self.ex_destination_cboe,
        #                                                                        self.child_price)
        # ocr_1_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_bats,
        #                                                  self.ex_destination_bats, True)
        # ocr_2_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_chix,
        #                                                  self.ex_destination_chix, True)
        # ocr_3_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_cboe,
        #                                                  self.ex_destination_cboe, True)
        # self.rule_list = [nos_1_rule, nos_2_rule, nos_3_rule, ocr_1_rule, ocr_2_rule, ocr_3_rule]
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.MP_Dark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MPDark_params()
        self.MP_Dark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.MP_Dark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, ClientAlgoPolicyID="QA_MPDark"))
        self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order, case_id_1)

        time.sleep(3)
        # endregion

        # TODO
        # # region Check Sell side
        # self.fix_verifier_sell.check_fix_message(self.MP_Dark_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')
        #
        # er_pending_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_pending)
        # self.fix_verifier_sell.check_fix_message(er_pending_new_MP_Dark_order_params, key_parameters=self.key_params_with_cl_ord_id, message_name='Sell side ExecReport PendingNew')
        #
        # er_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_new)
        # self.fix_verifier_sell.check_fix_message(er_new_MP_Dark_order_params, key_parameters=self.key_params_with_cl_ord_id, message_name='Sell side ExecReport New')
        # # endregion

        # region check that RFQ send to CHIXLIS
        nos_chixlis_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.qty, ExDestination=self.ex_destination_chixlis))
        self.fix_verifier_buy.check_fix_message(nos_chixlis_order, key_parameters=self.key_params_with_ex_destination, message_name='Buy side RFQ on CHIXLIS')
        # end region

        # region check that RFQ send to TQLIS
        nos_trql_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_RFQ_params().change_parameters(dict(Account=self.client, OrderQty=self.qty, ExDestination=self.ex_destination_trql))
        self.fix_verifier_buy.check_fix_message(nos_trql_order, key_parameters=self.key_params_with_ex_destination, message_name='Buy side RFQ on CHIXLIS')
        # end region

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        RuleManager.remove_rules(self.rule_list)