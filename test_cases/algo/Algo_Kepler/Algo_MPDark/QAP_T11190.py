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


class QAP_T11190(TestCase):
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
        self.algopolicy = constants.ClientAlgoPolicy.qa_mpdark_rr_5.value
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
        resident_time = 3000
        count_of_pools = 19
        temp_allotted_time = resident_time / count_of_pools / 1000
        self.allotted_time = round(temp_allotted_time, 6)
        # endregion

        self.pre_filter = self.data_set.get_pre_filter("pre_filer_equal_D")
        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_batsdark_kepler, self.ex_destination_batsdark, self.price)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_batsperiodic, self.price)
        nos_3_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_cboeeudark, self.price)
        nos_4_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_cboeeuperiodic, self.price)
        nos_5_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_copenhagendark, self.price)
        nos_6_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_copenhagenpa, self.price)
        nos_7_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_helsinkidark, self.price)
        nos_8_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_helsinkipa, self.price)
        nos_9_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_itg, self.price)
        nos_10_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_itgipa, self.price)
        nos_11_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_liquidnet, self.price)
        nos_12_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_liquidneteu, self.price)
        nos_13_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_sigmaxeu, self.price)
        nos_14_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_sigmaxpaeu, self.price)
        nos_15_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_stockholmdark, self.price)
        nos_16_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_stockholmpa, self.price)
        nos_17_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_tqdarkeu, self.price)
        nos_18_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_tqlitaquctioneu, self.price)
        nos_19_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_ubsperiodic, self.price)
        ocr_1_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_batsdark_kepler, self.ex_destination_batsdark, True)
        ocr_2_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_batsperiodic, True)
        ocr_3_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_cboeeudark, True)
        ocr_4_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_cboeeuperiodic, True)
        ocr_5_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_copenhagendark, True)
        ocr_6_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_copenhagenpa, True)
        ocr_7_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_helsinkidark, True)
        ocr_8_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_helsinkipa, True)
        ocr_9_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_itg, True)
        ocr_10_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_itgipa, True)
        ocr_11_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_liquidnet, True)
        ocr_12_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_liquidneteu, True)
        ocr_13_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_sigmaxeu, True)
        ocr_14_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_sigmaxpaeu, True)
        ocr_15_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_stockholmdark, True)
        ocr_16_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_stockholmpa, True)
        ocr_17_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_tqdarkeu, True)
        ocr_18_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_tqlitaquctioneu, True)
        ocr_19_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_kepler, self.ex_destination_ubsperiodic, True)
        self.rule_list = [nos_1_rule, nos_2_rule, nos_3_rule, nos_4_rule, nos_5_rule, nos_6_rule, nos_7_rule, nos_8_rule, nos_9_rule, nos_10_rule, nos_11_rule, nos_12_rule, nos_13_rule, nos_14_rule, nos_15_rule, nos_16_rule, nos_17_rule, nos_18_rule, nos_19_rule, ocr_1_rule, ocr_2_rule, ocr_3_rule, ocr_4_rule, ocr_5_rule, ocr_6_rule, ocr_7_rule, ocr_8_rule, ocr_9_rule, ocr_10_rule, ocr_11_rule, ocr_12_rule, ocr_13_rule, ocr_14_rule, ocr_15_rule, ocr_16_rule, ocr_17_rule, ocr_18_rule, ocr_19_rule]
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

        # region Check child DMA order on venue BATS DARKPOOL UK
        self.fix_verifier_buy.set_case_id(bca.create_event("Dark child DMA orders", self.test_id))

        self.dma_batsdark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_batsdark_order.change_parameters(dict(Account=self.account_batsdark_kepler, ExDestination=self.ex_destination_batsdark, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_batsdark_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_batsdark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_batsdark_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_batsdark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_batsdark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_batsdark_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_batsdark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        time.sleep(7)

        # region Check that the 1st child expires
        order_cancel_request_dma_batsdark_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_batsdark_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_batsdark_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 1 order')

        er_cancel_dma_batsdark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_batsdark_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_batsdark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 1 order')
        # endregion

        # region Check child DMA order on venue BATS PERIODIC UK
        self.dma_batsperiodic_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_batsperiodic_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_batsperiodic, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_batsperiodic_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 2 order')

        er_pending_new_dma_batsperiodic_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_batsperiodic_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_batsperiodic_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 2 order')

        er_new_dma_batsperiodic_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_batsperiodic_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_batsperiodic_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 2 order')
        # endregion

        # region Check Read log
        time.sleep(70)

        compare_message = ReadLogMessageAlgo().set_compare_message_for_check_resident_time_calculation()
        compare_message.change_parameters(dict(ParentOrder=parent_MP_Dark_order_id, ChildOrder='*', AllottedTime=self.allotted_time))

        self.read_log_verifier.set_case_id(bca.create_event("ReadLog", self.test_id))
        self.read_log_verifier.check_read_log_message(compare_message)
        # endregion

        # region Check that the 2nd child expires
        order_cancel_request_dma_batsperiodic_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_batsperiodic_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_batsperiodic_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 2 order')

        er_cancel_dma_batsperiodic_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_batsperiodic_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_batsperiodic_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 2 order')
        # endregion

        # region Check child DMA order on venue CBOE DARKPOOL EU
        self.dma_cboeeudark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_cboeeudark_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_cboeeudark, OrderQty=self.qty, Instrument=self.instrument))
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

        # region Check child DMA order on venue CBOE PERIODIC EU
        self.dma_cboeeuperiodic_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_cboeeuperiodic_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_cboeeuperiodic, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_cboeeuperiodic_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 4 order')

        er_pending_new_dma_cboeeuperiodic_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_cboeeuperiodic_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_cboeeuperiodic_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 4 order')

        er_new_dma_cboeeuperiodic_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_cboeeuperiodic_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_cboeeuperiodic_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 4 order')
        # endregion

        # region Check that the 4th child expires
        order_cancel_request_dma_cboeeuperiodic_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_cboeeuperiodic_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_cboeeuperiodic_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 4 order')

        er_cancel_dma_cboeeuperiodic_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_cboeeuperiodic_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_cboeeuperiodic_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 4 order')
        # endregion

        # region Check child DMA order on venue UBS PERIODIC
        self.dma_ubsperiodic_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_ubsperiodic_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_ubsperiodic, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_ubsperiodic_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 5 order')

        er_pending_new_dma_ubsperiodic_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_ubsperiodic_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_ubsperiodic_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 5 order')

        er_new_dma_ubsperiodic_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_ubsperiodic_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_ubsperiodic_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 5 order')
        # endregion

        # region Check that the 5th child expires
        order_cancel_request_dma_ubsperiodic_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_ubsperiodic_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_ubsperiodic_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 5 order')

        er_cancel_dma_ubsperiodic_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_ubsperiodic_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_ubsperiodic_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 5 order')
        # endregion

        # region Check child DMA order on venue Helsinki Dark
        self.dma_helsinkidark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_helsinkidark_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_helsinkidark, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_helsinkidark_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 6 order')

        er_pending_new_dma_helsinkidark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_helsinkidark_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_helsinkidark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 6 order')

        er_new_dma_helsinkidark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_helsinkidark_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_helsinkidark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 6 order')
        # endregion

        # region Check that the 6th child expires
        order_cancel_request_dma_helsinkidark_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_helsinkidark_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_helsinkidark_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 6 order')

        er_cancel_dma_helsinkidark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_helsinkidark_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_helsinkidark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 6 order')
        # endregion

        # region Check child DMA order on venue Helsinki PA
        self.dma_helsinkipa_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_helsinkipa_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_helsinkipa, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_helsinkipa_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 7 order')

        er_pending_new_dma_helsinkipa_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_helsinkipa_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_helsinkipa_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 7 order')

        er_new_dma_helsinkipa_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_helsinkipa_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_helsinkipa_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 7 order')
        # endregion

        # region Check that the 7th child expires
        order_cancel_request_dma_helsinkipa_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_helsinkipa_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_helsinkipa_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 7 order')

        er_cancel_dma_helsinkipa_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_helsinkipa_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_helsinkipa_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 7 order')
        # endregion

        # region Check child DMA order on venue Stockholm Dark
        self.dma_stockholmdark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_stockholmdark_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_stockholmdark, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_stockholmdark_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 8 order')

        er_pending_new_dma_stockholmdark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_stockholmdark_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_stockholmdark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 8 order')

        er_new_dma_stockholmdark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_stockholmdark_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_stockholmdark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 8 order')
        # endregion

        # region Check that the 8th child expires
        order_cancel_request_dma_stockholmdark_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_stockholmdark_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_stockholmdark_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 8 order')

        er_cancel_dma_stockholmdark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_stockholmdark_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_stockholmdark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 8 order')
        # endregion

        # region Check child DMA order on venue Stockholm PA
        self.dma_stockholmpa_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_stockholmpa_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_stockholmpa, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_stockholmpa_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 9 order')

        er_pending_new_dma_stockholmpa_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_stockholmpa_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_stockholmpa_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 9 order')

        er_new_dma_stockholmpa_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_stockholmpa_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_stockholmpa_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 9 order')
        # endregion

        # region Check that the 9th child expires
        order_cancel_request_dma_stockholmpa_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_stockholmpa_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_stockholmpa_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 9 order')

        er_cancel_dma_stockholmpa_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_stockholmpa_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_stockholmpa_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 9 order')
        # endregion

        # region Check child DMA order on venue ITG
        self.dma_itg_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_itg_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_itg, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_itg_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 10 order')

        er_pending_new_dma_itg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_itg_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_itg_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 10 order')

        er_new_dma_itg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_itg_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_itg_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 10 order')
        # endregion

        # region Check that the 10th child expires
        order_cancel_request_dma_itg_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_itg_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_itg_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 10 order')

        er_cancel_dma_itg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_itg_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_itg_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 10 order')
        # endregion

        # region Check child DMA order on venue ITGIPA
        self.dma_itgipa_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_itgipa_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_itg, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_itgipa_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 11 order')

        er_pending_new_dma_itgipa_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_itgipa_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_itgipa_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 11 order')

        er_new_dma_itgipa_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_itgipa_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_itgipa_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 11 order')
        # endregion

        # region Check that the 11th child expires
        order_cancel_request_dma_itgipa_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_itgipa_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_itgipa_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 11 order')

        er_cancel_dma_itgipa_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_itgipa_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_itgipa_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 11 order')
        # endregion

        # region Check child DMA order on venue TQDARKEU
        self.dma_tqdarkeu_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_tqdarkeu_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_tqdarkeu, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_tqdarkeu_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 12 order')

        er_pending_new_dma_tqdarkeu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_tqdarkeu_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_tqdarkeu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 12 order')

        er_new_dma_tqdarkeu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_tqdarkeu_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_tqdarkeu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 12 order')
        # endregion

        # region Check that the 12th child expires
        order_cancel_request_dma_tqdarkeu_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_tqdarkeu_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_tqdarkeu_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 12 order')

        er_cancel_dma_tqdarkeu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_tqdarkeu_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_tqdarkeu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 12 order')
        # endregion

        # region Check child DMA order on venue TQLITAUCTION EU
        self.dma_tqlitauctioneu_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_tqlitauctioneu_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_tqlitaquctioneu, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_tqlitauctioneu_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 13 order')

        er_pending_new_dma_tqlitauctioneu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_tqlitauctioneu_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_tqlitauctioneu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 13 order')

        er_new_dma_tqlitauctioneu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_tqlitauctioneu_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_tqlitauctioneu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 13 order')
        # endregion

        # region Check that the 13th child expires
        order_cancel_request_dma_tqlitauctioneu_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_tqlitauctioneu_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_tqlitauctioneu_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 13 order')

        er_cancel_dma_tqlitauctioneu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_tqlitauctioneu_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_tqlitauctioneu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 13 order')
        # endregion

        # region Check child DMA order on venue Copenhagen Dark
        self.dma_copenhagendark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_copenhagendark_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_copenhagendark, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_copenhagendark_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 14 order')

        er_pending_new_dma_copenhagendark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_copenhagendark_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_copenhagendark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 14 order')

        er_new_dma_copenhagendark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_copenhagendark_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_copenhagendark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 14 order')
        # endregion

        # region Check that the 14th child expires
        order_cancel_request_dma_copenhagendark_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_copenhagendark_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_copenhagendark_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 14 order')

        er_cancel_dma_copenhagendark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_copenhagendark_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_copenhagendark_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 14 order')
        # endregion

        # region Check child DMA order on venue Copenhagen PA
        self.dma_copenhagenpa_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_copenhagenpa_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_copenhagenpa, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_copenhagenpa_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 15 order')

        er_pending_new_dma_copenhagenpa_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_copenhagenpa_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_copenhagenpa_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 15 order')

        er_new_dma_copenhagenpa_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_copenhagenpa_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_copenhagenpa_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 15 order')
        # endregion

        # region Check that the 15th child expires
        order_cancel_request_dma_copenhagenpa_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_copenhagenpa_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_copenhagenpa_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 15 order')

        er_cancel_dma_copenhagenpa_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_copenhagenpa_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_copenhagenpa_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 15 order')
        # endregion

        # region Check child DMA order on venue LIQUIDNET
        self.dma_liquidnet_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_liquidnet_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_liquidnet, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_liquidnet_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 16 order')

        er_pending_new_dma_liquidnet_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_liquidnet_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_liquidnet_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 16 order')

        er_new_dma_liquidnet_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_liquidnet_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_liquidnet_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 16 order')
        # endregion

        # region Check that the 16th child expires
        order_cancel_request_dma_liquidnet_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_liquidnet_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_liquidnet_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 16 order')

        er_cancel_dma_liquidnet_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_liquidnet_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_liquidnet_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 16 order')
        # endregion

        # region Check child DMA order on venue LIQUIDNET EU
        self.dma_liquidneteu_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_liquidneteu_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_liquidneteu, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_liquidneteu_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 17 order')

        er_pending_new_dma_liquidneteu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_liquidneteu_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_liquidneteu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 17 order')

        er_new_dma_liquidneteu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_liquidneteu_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_liquidneteu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 17 order')
        # endregion

        # region Check that the 17th child expires
        order_cancel_request_dma_liquidneteu_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_liquidneteu_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_liquidneteu_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 17 order')

        er_cancel_dma_liquidneteu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_liquidneteu_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_liquidneteu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 17 order')
        # endregion

        # region Check child DMA order on venue SIGMAX EU
        self.dma_sigmaxeu_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_sigmaxeu_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_sigmaxeu, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_sigmaxeu_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 18 order')

        er_pending_new_dma_sigmaxeu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_sigmaxeu_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_sigmaxeu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 18 order')

        er_new_dma_sigmaxeu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_sigmaxeu_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_sigmaxeu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 18 order')
        # endregion

        # region Check that the 18th child expires
        order_cancel_request_dma_sigmaxeu_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_sigmaxeu_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_sigmaxeu_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 18 order')

        er_cancel_dma_sigmaxeu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_sigmaxeu_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_sigmaxeu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 18 order')
        # endregion

        # region Check child DMA order on venue SIGMAX PA EU
        self.dma_sigmaxpaeu_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Dark_Child_Kepler_params()
        self.dma_sigmaxpaeu_order.change_parameters(dict(Account=self.account_kepler, ExDestination=self.ex_destination_sigmaxpaeu, OrderQty=self.qty, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_sigmaxpaeu_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 19 order')

        er_pending_new_dma_sigmaxpaeu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_sigmaxpaeu_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_sigmaxpaeu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 19 order')

        er_new_dma_sigmaxpaeu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_sigmaxpaeu_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_sigmaxpaeu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 19 order')
        # endregion

        # region Check that the 19th child expires
        order_cancel_request_dma_sigmaxpaeu_order = FixMessageOrderCancelRequestAlgo().set_cancel_params_for_child_kepler(self.dma_sigmaxpaeu_order)
        self.fix_verifier_buy.check_fix_message_kepler(order_cancel_request_dma_sigmaxpaeu_order, key_parameters=self.key_params_OCR_child, message_name='Buy side OrderCancelRequest Child DMA 19 order')

        er_cancel_dma_sigmaxpaeu_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_sigmaxpaeu_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_sigmaxpaeu_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA 19 order')
        # endregion

        # region Check that parent order eliminated
        er_eliminate_mp_dark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.MP_Dark_order, self.gateway_side_sell, self.status_eliminate)
        self.fix_verifier_sell.check_fix_message(er_eliminate_mp_dark_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Eliminate')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

