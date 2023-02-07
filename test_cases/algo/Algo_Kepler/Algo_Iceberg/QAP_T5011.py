import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T5011(TestCase):
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
        self.qty = 500
        self.price = 10
        self.display_qty = 250
        self.qty_for_md = 1000
        self.price_ask = 44
        self.price_bid = 30
        self.delay = 0
        self.party_id = constants.PartyID.party_id_8.value
        self.party_id_source = constants.PartyIDSource.party_id_source_1.value
        self.party_role = constants.PartyRole.party_role_3.value

        self.no_party = [
            {'PartyID': self.party_id, 'PartyIDSource': self.party_id_source,
             'PartyRole': self.party_role}
        ]

        self.no_party_for_report = [
            {'PartyID': self.party_id, 'PartyIDSource': self.party_id_source,
             'PartyRole': self.party_role},
            {'PartyID': '*', 'PartyIDSource': '*',
             'PartyRole': '*'}
        ]
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_partial_fill = Status.PartialFill
        self.status_fill = Status.Fill
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_9")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_xpar = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_xpar = self.data_set.get_listing_id_by_name("listing_6")
        self.listing_id_bats = self.data_set.get_listing_id_by_name("listing_32")
        self.listing_id_janestreet = self.data_set.get_listing_id_by_name("listing_34")
        self.listing_id_trqx = self.data_set.get_listing_id_by_name("listing_15")
        self.listing_id_chix = self.data_set.get_listing_id_by_name("listing_33")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_xpar, self.price)
        nos_trade_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(self.fix_env1.buy_side, self.account, self.ex_destination_xpar, self.price, self.price, self.display_qty, self.display_qty, self.delay)
        self.rule_list = [nos_rule, nos_trade_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_xpar = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_xpar, self.fix_env1.feed_handler)
        market_data_snap_shot_xpar.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_xpar.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_xpar)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_bats = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_bats, self.fix_env1.feed_handler)
        market_data_snap_shot_bats.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_bats.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_bats)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_janestreet = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_janestreet, self.fix_env1.feed_handler)
        market_data_snap_shot_janestreet.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_janestreet.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_janestreet)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_chix = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_chix, self.fix_env1.feed_handler)
        market_data_snap_shot_chix.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_chix.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_chix)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_trqx = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_trqx)
        # endregion

        # region Send NewOrderSingle (35=D) for SORPING order
        case_id_1 = bca.create_event("Create Iceberg Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.Iceberg_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_LitDark_Iceberg_Kepler_params_with_PartyInfo()
        self.Iceberg_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Iceberg_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, DisplayInstruction=dict(DisplayQty=self.display_qty))).update_repeating_group('NoParty', self.no_party)

        self.fix_manager_sell.send_message_and_receive_response(self.Iceberg_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side and PartyInfo in ERs PendingNew -> New
        self.fix_verifier_sell.check_fix_message(self.Iceberg_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_Iceberg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Iceberg_order, self.gateway_side_sell, self.status_pending)
        er_pending_new_Iceberg_order_params.remove_parameter('NoParty').add_fields_into_repeating_group('NoParty', self.no_party_for_report)
        self.fix_verifier_sell.check_fix_message(er_pending_new_Iceberg_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_Iceberg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Iceberg_order, self.gateway_side_sell, self.status_new)
        er_new_Iceberg_order_params.remove_parameter('NoParty').add_fields_into_repeating_group('NoParty', self.no_party_for_report)
        self.fix_verifier_sell.check_fix_message(er_new_Iceberg_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check 1st child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA orders", self.test_id))

        self.dma_1_xpar_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_child_of_LitDark_Iceberg_Kepler_params_with_PartyInfo()
        self.dma_1_xpar_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_xpar, OrderQty=self.display_qty, Price=self.price, Instrument=self.instrument)).update_repeating_group('NoParty', self.no_party)
        self.fix_verifier_buy.check_fix_message(self.dma_1_xpar_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_1_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_xpar_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_1_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_1_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_xpar_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_1_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')

        er_fill_dma_1_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_xpar_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(er_fill_dma_1_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Fill Child DMA 1 order')
        # endregion

        # region Check PartyInfo in the ER Partially fill parent
        er_partial_fill_Iceberg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Iceberg_order, self.gateway_side_sell, self.status_partial_fill)
        er_partial_fill_Iceberg_order_params.remove_parameter('NoParty').add_fields_into_repeating_group('NoParty', self.no_party_for_report)
        self.fix_verifier_sell.check_fix_message(er_partial_fill_Iceberg_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Partial fill')
        # endregion

        # region Check 2nd child DMA order
        self.dma_2_xpar_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_child_of_LitDark_Iceberg_Kepler_params_with_PartyInfo()
        self.dma_2_xpar_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_xpar, OrderQty=self.display_qty, Price=self.price, Instrument=self.instrument)).update_repeating_group('NoParty', self.no_party)
        self.fix_verifier_buy.check_fix_message(self.dma_2_xpar_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_2_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_xpar_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_2_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_2_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_xpar_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_2_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')

        er_fill_dma_2_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_xpar_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(er_fill_dma_2_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Fill Child DMA 1 order')
        # endregion

        # region Check PartyInfo in the ER Fill parent
        er_fill_Iceberg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Iceberg_order, self.gateway_side_sell, self.status_fill)
        er_fill_Iceberg_order_params.remove_parameter('NoParty').add_fields_into_repeating_group('NoParty', self.no_party_for_report)
        self.fix_verifier_sell.check_fix_message(er_fill_Iceberg_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Fill')
        # endregion

        time.sleep(10)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
