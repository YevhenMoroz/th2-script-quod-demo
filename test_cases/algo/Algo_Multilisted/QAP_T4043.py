import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, StrategyParameterType
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T4043(TestCase):
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
        self.qty_ask = 150
        self.qty_bid = 100
        self.price_bid = 13
        self.price_ask_1 = 15
        self.price_ask_2 = 16
        self.qty = 150
        self.price = 17
        self.min_qty = 100
        self.tif_fok = constants.TimeInForce.FillOrKill.value
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.venue_qlv1 = "QLVENUE1" # without IOC support
        self.venue_qlv2 = "QLVENUE2" # without FOK support
        self.string_type = StrategyParameterType.String.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_partial_fill = Status.PartialFill
        self.status_fill = Status.Fill
        self.status_eliminate = Status.Eliminate
        self.status_cancel = Status.Cancel
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_36")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_42")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_23")
        self.listing_qlv1 = self.data_set.get_listing_id_by_name("listing_53")
        self.listing_qlv2 = self.data_set.get_listing_id_by_name("listing_54")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

        # region SSH
        self.config_sats = "client_sats.xml"
        self.config_ors = "client_ors.xml"
        self.mod_tifAliasing_value = "true"
        self.def_tifAliasing_value = "false"
        self.xpath_sats = ".//sats/tifAliasing"
        self.xpath_ors = ".//ors/tifAliasing"
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Prepare SATS configuration
        self.ssh_client.get_and_update_file(self.config_ors, {self.xpath_ors: self.mod_tifAliasing_value})
        self.ssh_client.get_and_update_file(self.config_sats, {self.xpath_sats: self.mod_tifAliasing_value})
        self.ssh_client.send_command("qrestart SATS ORS")
        time.sleep(65)
        # endregion

        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, True, self.qty_ask, self.price_ask_1, 3000)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [nos_ioc_rule, ocr_rule]
        # endregion

        # region Send_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data QLVENUE2", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_qlv2, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_1, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data QLVENUE1", self.test_id))
        market_data_snap_shot_trqx = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_qlv1, self.fix_env1.feed_handler)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_2, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_trqx)
        # endregion

        time.sleep(3)

        # region Send NewOrderSingle (35=D) for Multilisting order
        case_id_1 = bca.create_event("Create Multilisting Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.Multilisting_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_params()
        self.Multilisting_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Multilisting_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, TimeInForce=self.tif_fok))
        self.Multilisting_order.add_fields_into_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='AllowedVenues', StrategyParameterType=self.string_type, StrategyParameterValue=f'{self.venue_qlv1}/{self.venue_qlv2}')])

        self.fix_manager_sell.send_message_and_receive_response(self.Multilisting_order, case_id_1)
        # endregion

        time.sleep(1)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.Multilisting_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_Multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Multilisting_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_Multilisting_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_Multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Multilisting_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_Multilisting_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Send_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data PARIS", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_qlv2, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=0, MDEntrySize=0)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=0, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        time.sleep(2)

        # region Check child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.dma_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_1, OrderQty=self.qty, Price=self.price_ask_1, Instrument='*', TimeInForce=self.tif_ioc, MinQty=self.qty_ask))

        self.fix_verifier_buy.check_fix_message(self.dma_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA order')

        er_pending_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_dma_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA order')

        er_new_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA order')

        er_fill_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_fill)
        er_fill_dma_order_params.change_parameters(dict(CumQty=self.qty_ask))
        self.fix_verifier_buy.check_fix_message(er_fill_dma_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Fill Child DMA order')
        # endregion

        # region Check fill Multilisting algo order
        er_partial_fill_Multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Multilisting_order, self.gateway_side_sell, self.status_fill)
        self.fix_verifier_sell.check_fix_message(er_partial_fill_Multilisting_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Fill')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        RuleManager(Simulators.algo).remove_rules(self.rule_list)

        # region postcondition: Change SATS configuration to default
        self.ssh_client.get_and_update_file(self.config_ors, {self.xpath_ors: self.def_tifAliasing_value})
        self.ssh_client.get_and_update_file(self.config_sats, {self.xpath_sats: self.def_tifAliasing_value})
        self.ssh_client.send_command("qrestart SATS ORS")
        time.sleep(60)
        # endregion
