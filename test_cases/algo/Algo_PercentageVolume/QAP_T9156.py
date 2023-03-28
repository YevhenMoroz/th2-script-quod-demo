import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.algo_formulas_manager import AlgoFormulasManager
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T9156(TestCase):
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
        self.price = 25
        self.volume = 0.1
        self.md_entry_px_incr_r = 0
        self.md_entry_size_incr_r = 1000
        self.price_bid_1 = 22.005
        self.price_bid_2 = 20
        self.qty_bid = 1000
        self.child_qty = AlgoFormulasManager.get_pov_child_qty_on_ltq(self.volume, self.md_entry_size_incr_r, self.qty)

        self.no_strategy = [
            {'StrategyParameterName': 'PercentageVolume', 'StrategyParameterType': '6',
             'StrategyParameterValue': '0.1'},
            {'StrategyParameterName': 'AnticipativePostingOffset', 'StrategyParameterType': '1',
             'StrategyParameterValue': '60'}
        ]
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_fill = Status.Fill
        self.statulisting_id_xpartial_fill = Status.PartialFill
        self.status_cancel = Status.Cancel
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_2")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_xpar = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.listing_id_xpar = self.data_set.get_listing_id_by_name("listing_1")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

        # region SSH
        self.config_file = "client_sats.xml"
        self.mod_bpsOffs_value = "true"
        self.mod_levels_value = "4"
        self.def_bpsOffs_value = "false"
        self.def_levels_value = "5"
        self.xpath_bpsOffs = ".//Participate/bpsOffsets"
        self.xpath_levels = ".//Participate/levels"
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        # endregion

        self.pre_filter = self.data_set.get_pre_filter("pre_filer_equal_D")

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Prepare SATS configuration
        self.ssh_client.get_and_update_file(self.config_file, {self.xpath_bpsOffs: self.mod_bpsOffs_value, self.xpath_levels: self.mod_levels_value})
        self.ssh_client.send_command("qrestart SATS")
        time.sleep(35)
        # endregion

        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_xpar, self.price_bid_1)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_xpar, True)
        self.rule_list = [nos_1_rule, ocr_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_xpar = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_xpar, self.fix_env1.feed_handler)
        market_data_snap_shot_xpar.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_1, MDEntrySize=self.qty_bid)
        market_data_snap_shot_xpar.add_fields_into_repeating_group('NoMDEntries', [dict(MDEntryType=0, MDEntryPx=self.price_bid_2, MDEntrySize=self.qty_bid, MDEntryPositionNo=2)])
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_xpar)

        market_data_snap_shot_xpar = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_xpar, self.fix_env1.feed_handler)
        market_data_snap_shot_xpar.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=0, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_xpar)

        time.sleep(3)

        # region Send NewOrderSingle (35=D) for POV order
        case_id_1 = bca.create_event("Create POV Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.POV_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_params()
        self.POV_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.POV_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_xpar)).update_repeating_group('NoStrategyParameters', self.no_strategy)

        self.fix_manager_sell.send_message_and_receive_response(self.POV_order, case_id_1)

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_xpar = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_xpar, self.fix_env1.feed_handler)
        market_data_snap_shot_xpar.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_1, MDEntrySize=self.qty_bid)
        market_data_snap_shot_xpar.add_fields_into_repeating_group('NoMDEntries', [dict(MDEntryType=0, MDEntryPx=self.price_bid_2, MDEntrySize=self.qty_bid, MDEntryPositionNo=2)])
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_xpar)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.POV_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_POV_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_POV_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check first child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.dma_1_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_xpar, OrderQty=self.child_qty, Price=self.price_bid_1, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(self.dma_1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_dma_1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        # region Check that is only one child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Check that only one child DMA order is generated", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([self.dma_1_order], [None], self.FromQuod, pre_filter=self.pre_filter)
        # endregion

        time.sleep(15)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        cancel_request_POV_order = FixMessageOrderCancelRequest(self.POV_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_POV_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_POV_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel second dma child order
        cancel_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_dma_1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 1 order")
        # endregion

        cancel_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_POV_order_params, key_parameters=self.key_params_ER_child, message_name='Sell side ExecReport Cancel')
        # endregion

        # region postcondition: Change SATS configuration to default
        self.ssh_client.get_and_update_file(self.config_file, {self.xpath_bpsOffs: self.def_bpsOffs_value, self.xpath_levels: self.def_levels_value})
        self.ssh_client.send_command("qrestart SATS")
        time.sleep(35)
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
