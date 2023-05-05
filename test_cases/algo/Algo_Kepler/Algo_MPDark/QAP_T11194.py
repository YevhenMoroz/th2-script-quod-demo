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
from test_framework.read_log_wrappers.algo_messages.ReadLogMessageAlgo import ReadLogMessageAlgo


class QAP_T11194(TestCase):
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
        self.qty = 100
        self.price = 20
        self.algopolicy = constants.ClientAlgoPolicy.qa_mpdark_rr_4.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        self.status_eliminate = Status.Eliminate
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_23")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_batsdark = self.data_set.get_mic_by_name("mic_4")
        self.ex_destination_cboeeudark = self.data_set.get_mic_by_name("mic_6")
        self.ex_destination_batsperiodic = self.data_set.get_mic_by_name("mic_57")
        self.ex_destination_liquidnet = self.data_set.get_mic_by_name("mic_54")
        self.ex_destination_tqlitaquctioneu = self.data_set.get_mic_by_name("mic_62")
        self.ex_destination_ubsperiodic = self.data_set.get_mic_by_name("mic_48")
        self.ex_destination_cboeeuperiodic = self.data_set.get_mic_by_name("mic_49")
        self.ex_destination_itg = self.data_set.get_mic_by_name("mic_7")
        self.ex_destination_tqdarkeu = self.data_set.get_mic_by_name("mic_8")
        self.ex_destination_helsinkipa = self.data_set.get_mic_by_name("mic_50")
        self.ex_destination_helsinkidark = self.data_set.get_mic_by_name("mic_58")
        self.ex_destination_stockholmpa = self.data_set.get_mic_by_name("mic_51")
        self.ex_destination_itgipa = self.data_set.get_mic_by_name("mic_52")
        self.ex_destination_copenhagenpa = self.data_set.get_mic_by_name("mic_53")
        self.ex_destination_liquidneteu = self.data_set.get_mic_by_name("mic_55")
        self.ex_destination_sigmaxeu = self.data_set.get_mic_by_name("mic_56")
        self.ex_destination_sigmaxpaeu = self.data_set.get_mic_by_name("mic_59")
        self.ex_destination_copenhagendark = self.data_set.get_mic_by_name("mic_60")
        self.ex_destination_stockholmdark = self.data_set.get_mic_by_name("mic_61")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account_batsdark_kepler = self.data_set.get_account_by_name("account_7")
        self.account_kepler = self.data_set.get_account_by_name("account_9")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        self.key_params_OCR_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_OCR_child")
        # endregion

        # region Read log verifier params
        self.log_verifier_by_name = constants.ReadLogVerifiers.log319_check_resident_time_calculation.value
        self.read_log_verifier = ReadLogVerifierAlgo(self.log_verifier_by_name, report_id)
        # endregion

        # region Compare message params
        resident_time = 150
        count_of_pools = 19
        temp_allotted_time = resident_time / count_of_pools / 1000
        self.allotted_time = round(temp_allotted_time, 7)
        # endregion

        self.pre_filter = self.data_set.get_pre_filter("pre_filer_equal_D")
        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_chixdelta, self.ex_destination_chixdelta, self.price)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_batsdark_kepler, self.ex_destination_batsdark, self.price)
        nos_3_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_cboeeudark, self.ex_destination_cboeeudark, self.price)
        ocr_1_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_chixdelta, self.ex_destination_chixdelta, True)
        ocr_2_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_batsdark_kepler, self.ex_destination_batsdark, True)
        ocr_3_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_cboeeudark, self.ex_destination_cboeeudark, True)
        self.rule_list = [nos_1_rule, nos_2_rule, nos_3_rule, ocr_1_rule, ocr_2_rule, ocr_3_rule]
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create MP Dark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.MP_Dark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MPDark_Kepler_params()
        self.MP_Dark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.MP_Dark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, ClientAlgoPolicyID=self.algopolicy, Instrument=self.instrument))

        responce = self.fix_manager_sell.send_message_and_receive_response(self.MP_Dark_order, case_id_1)

        parent_MP_Dark_order_id = responce[0].get_parameter('ExecID')

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.MP_Dark_order, self.key_params_NOS_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_MP_Dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_MP_Dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        time.sleep(5)

        # region Check child DMA order on venue chixdelta DARKPOOL UK
        self.fix_verifier_buy.set_case_id(bca.create_event("Dark child DMA orders", self.test_id))

        self.dma_chixdelta_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_chixdelta_order.change_parameters(dict(Account=self.account_chixdelta, ExDestination=self.ex_destination_chixdelta, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_chixdelta_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chixdelta_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chixdelta_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        time.sleep(7)

        # region Check that the 1st child expires
        order_cancel_request_dma_chixdelta_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_chixdelta_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_chixdelta_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 1 order')

        er_cancel_dma_chixdelta_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_chixdelta_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_chixdelta_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 1 order')
        # endregion

        # region Check child DMA order on venue batsdark DARKPOOL UK
        self.dma_batsdark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_batsdark_order.change_parameters(dict(Account=self.account_batsdark_kepler, ExDestination=self.ex_destination_batsdark, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_batsdark_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 2 order')

        er_pending_new_dma_batsdark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_batsdark_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_batsdark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 2 order')

        er_new_dma_batsdark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_batsdark_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_batsdark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 2 order')
        # endregion

        # region Check Read log
        time.sleep(70)

        compare_message = ReadLogMessageAlgo().set_compare_message_for_check_resident_time_calculation()
        compare_message.change_parameters(dict(ParentOrder=parent_MP_Dark_order_id, ChildOrder='*', AllottedTime=self.allotted_time))

        self.read_log_verifier.set_case_id(bca.create_event("ReadLog", self.test_id))
        self.read_log_verifier.check_read_log_message(compare_message)
        # endregion

        # region Check that the 2nd child expires
        order_cancel_request_dma_batsdark_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_batsdark_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_batsdark_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 2 order')

        er_cancel_dma_batsdark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_batsdark_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_batsdark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 2 order')
        # endregion

        # region Check child DMA order on venue cboeeudark DARKPOOL EU
        self.dma_cboeeudark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_cboeeudark_order.change_parameters(dict(Account=self.account_cboeeudark, ExDestination=self.ex_destination_cboeeudark, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_cboeeudark_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 3 order')

        er_pending_new_dma_cboeeudark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_cboeeudark_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_cboeeudark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 3 order')

        er_new_dma_cboeeudark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_cboeeudark_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_cboeeudark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 3 order')
        # endregion

        # region Check that the 3rd child expires
        order_cancel_request_dma_cboeeudark_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_cboeeudark_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_cboeeudark_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 3 order')

        er_cancel_dma_cboeeudark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_cboeeudark_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_cboeeudark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 3 order')
        # endregion

        # region Check those are no child orders on the venue which were discarded
        self.fix_verifier_buy.set_case_id(bca.create_event("Check those are no child orders on the venue which were discarded", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([self.dma_chixdelta_order, self.dma_batsdark_order, self.dma_cboeeudark_order], [self.key_params_NOS_child, self.key_params_NOS_child, self.key_params_NOS_child], self.FromQuod, pre_filter=self.pre_filter)
        # endregion

        # region Check that parent order eliminated
        er_eliminate_mp_dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_eliminate)
        self.fix_verifier_sell.check_fix_message(er_eliminate_mp_dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Eliminate')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

