import os
import time
from pathlib import Path
from datetime import datetime, timedelta

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.algo_formulas_manager import AlgoFormulasManager
from test_framework.read_log_wrappers.algo.ReadLogVerifierAlgo import ReadLogVerifierAlgo
from test_framework.read_log_wrappers.algo_messages.ReadLogMessageAlgo import ReadLogMessageAlgo


class QAP_T4709(TestCase):
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
        self.qty = 1000
        self.price = 3.9
        self.price_ask = 40
        self.price_bid = 1
        self.qty_bid = self.qty_ask = 1000000
        self.tif_gtd = constants.TimeInForce.GoodTillDate.value

        now = datetime.today() - timedelta(hours=3)
        delta = 2
        expire_date = (now + timedelta(days=delta))
        shift_1 = AlgoFormulasManager.calculate_shift_for_settl_date_if_it_is_on_weekend(expire_date, delta)
        self.ExpireDate_for_sending = expire_date.strftime("%Y%m%d")
        expire_date = (now + timedelta(days=2))
        shift_2 = AlgoFormulasManager.make_expire_date_friday_if_it_is_on_weekend(expire_date)
        self.ExpireDate = (expire_date - timedelta(days=shift_2)).strftime("%Y%m%d")
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
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_17")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_quodlit11 = self.data_set.get_mic_by_name("mic_28")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_qdl11 = self.data_set.get_listing_id_by_name("listing_27")
        self.listing_id_qdl12 = self.data_set.get_listing_id_by_name("listing_28")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

        # region Read log verifier params
        self.log_verifier_by_name_1 = constants.ReadLogVerifiers.log_319_check_settl_date_part_1.value
        self.log_verifier_by_name_2 = constants.ReadLogVerifiers.log_319_check_settl_date_part_2.value
        self.log_verifier_by_name_3 = constants.ReadLogVerifiers.log_319_check_settl_date_part_3.value
        self.read_log_verifier_1 = ReadLogVerifierAlgo(self.log_verifier_by_name_1, report_id)
        self.read_log_verifier_2 = ReadLogVerifierAlgo(self.log_verifier_by_name_2, report_id)
        self.read_log_verifier_3 = ReadLogVerifierAlgo(self.log_verifier_by_name_3, report_id)
        self.key_params_read_log = self.data_set.get_verifier_key_parameters_by_name("key_params_log_319_check_settl_date_part_3")
        # endregion

        # region Compare message parameters
        self.child_settle_date_for_read_log = (now + timedelta(days=shift_1)).strftime("%Y-%b-%d")
        self.instr_type = 'Equity'
        self.count_of_days = 2
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit11, self.price)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit11, True)
        self.rule_list = [nos_rule, ocr_rule]
        # endregion

        # region Send_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl11 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl11, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl11.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_qdl11.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl11)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl12 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl12, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl12.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_qdl12.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl12)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for SynthMinQty order
        case_id_1 = bca.create_event("Create SORPING GTD Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.SORPING_GTD_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multiple_Emulation_Kepler_params()
        self.SORPING_GTD_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.SORPING_GTD_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, TimeInForce=self.tif_gtd)).add_tag(dict(ExpireDate=self.ExpireDate_for_sending))

        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_GTD_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.SORPING_GTD_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        self.SORPING_GTD_order.change_parameters(dict(ExpireDate=self.ExpireDate))

        er_pending_new_SORPING_GTD_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_GTD_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_SORPING_GTD_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_SORPING_GTD_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_GTD_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_SORPING_GTD_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.dma_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_Multiple_Emulation_Kepler_params()
        self.dma_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit11, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        # region Check Read log
        time.sleep(70)

        compare_message_1 = ReadLogMessageAlgo().set_compare_message_for_check_settl_date_part_1()
        compare_message_1.change_parameters(dict(InstrType=self.instr_type))

        compare_message_2 = ReadLogMessageAlgo().set_compare_message_for_check_settl_date_part_2()
        compare_message_2.change_parameters(dict(CountOfDays=self.count_of_days))

        compare_message_3 = ReadLogMessageAlgo().set_compare_message_for_check_settl_date_part_3()
        compare_message_3.change_parameters(dict(SettlDate=self.child_settle_date_for_read_log))

        self.read_log_verifier_1.set_case_id(bca.create_event("ReadLog", self.test_id))
        self.read_log_verifier_1.check_read_log_message(compare_message_1)

        self.read_log_verifier_2.set_case_id(bca.create_event("ReadLog", self.test_id))
        self.read_log_verifier_2.check_read_log_message(compare_message_2)

        self.read_log_verifier_3.set_case_id(bca.create_event("ReadLog", self.test_id))
        self.read_log_verifier_3.check_read_log_message(compare_message_3, self.key_params_read_log)
        # endregion

        time.sleep(10)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_4 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_4)
        cancel_request_SORPING_GTD_order = FixMessageOrderCancelRequest(self.SORPING_GTD_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_SORPING_GTD_order, case_id_4)
        self.fix_verifier_sell.check_fix_message(cancel_request_SORPING_GTD_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel first dma child order
        er_cancel_dma_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 1 order")

        er_cancel_SORPING_GTD_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_GTD_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_SORPING_GTD_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
