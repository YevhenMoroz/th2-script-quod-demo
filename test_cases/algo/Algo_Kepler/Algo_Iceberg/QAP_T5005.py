import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.read_log_wrappers.algo.ReadLogVerifierAlgo import ReadLogVerifierAlgo
from test_framework.read_log_wrappers.algo_messages.ReadLogMessageAlgo import ReadLogMessageAlgo


class QAP_T5005(TestCase):
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
        self.party_id = constants.PartyID.party_id_2.value
        self.party_id_source = constants.PartyIDSource.party_id_source_1.value
        self.party_role = constants.PartyRole.party_role_24.value

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
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
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

        # region Read log verifier params
        self.log_verifier_by_name_1 = constants.ReadLogVerifiers.log319_check_party_info_for_the_one_group_sell_side.value
        self.read_log_verifier_1 = ReadLogVerifierAlgo(self.log_verifier_by_name_1, report_id)
        self.log_verifier_by_name_2 = constants.ReadLogVerifiers.log319_check_party_info_for_the_one_group_buy_side.value
        self.read_log_verifier_2 = ReadLogVerifierAlgo(self.log_verifier_by_name_2, report_id)
        # endregion

        # region Read log verifier params
        # self.log_verifier_by_name = constants.ReadLogVerifiers.log_319_check_mapping_on_sell_side.value
        # self.read_log_verifier = ReadLogVerifierAlgo(self.log_verifier_by_name, report_id)
        # self.key_params_read_log = self.data_set.get_verifier_key_parameters_by_name("key_params_log_319_check_mapping_on_sell_side")
        # endregion

        # region Compare message parameters
        self.party_id_source_map = constants.PartyIDSourceMap.proprietary.value
        self.party_role_map = constants.PartyRoleMap.customer_account.value
        # endregion

        # region Compare message parameters
        # self.param1 = constants.ReadLogParams.party_id.value
        # self.param2 = constants.ReadLogParams.party_id_source.value
        # self.param3 = constants.ReadLogParams.party_role.value
        # self.param4 = constants.ReadLogParams.cl_ord_id.value
        # self.party_id_source_map = constants.PartyIDSourceMap.proprietary.value
        # self.party_role_map = constants.PartyRoleMap.customer_account.value
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_xpar, self.price)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_xpar, True)
        self.rule_list = [nos_rule, ocr_rule]
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

        self.Iceberg_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_LitDark_Iceberg_params_with_PartyInfo()
        self.Iceberg_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.ClOrdId = self.Iceberg_order.get_parameter('ClOrdID')
        self.Iceberg_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, DisplayInstruction=dict(DisplayQty=self.display_qty))).update_repeating_group('NoParty', self.no_party)

        self.fix_manager_sell.send_message_and_receive_response(self.Iceberg_order, case_id_1)
        # endregion

        # region Check Read log
        time.sleep(70)

        compare_message_1 = ReadLogMessageAlgo().set_compare_message_for_check_party_info_for_the_one_group_sell_side()
        compare_message_1.change_parameters(dict(PartyID=self.party_id, PartyIDSource=self.party_id_source_map, PartyRole=self.party_role_map, ClOrdID=self.ClOrdId))

        compare_message_2 = ReadLogMessageAlgo().set_compare_message_for_check_party_info_for_the_one_group_buy_side()
        compare_message_2.change_parameters(dict(PartyID=self.party_id, PartyIDSource=self.party_id_source_map, PartyRole=self.party_role_map))

        self.read_log_verifier_1.set_case_id(bca.create_event("ReadLog: Sell-side", self.test_id))
        self.read_log_verifier_1.check_read_log_message(compare_message_1)

        self.read_log_verifier_2.set_case_id(bca.create_event("ReadLog: Buy-side", self.test_id))
        self.read_log_verifier_2.check_read_log_message(compare_message_2)

        # compare_message = ReadLogMessageAlgo().set_compare_message_for_check_mapping_on_sell_side()
        # compare_message.change_parameters(dict(Parameter1=self.param1, Value1=self.party_id, Parameter2=self.param2, Value2=self.party_id_source_map, Parameter3=self.param3, Value3=self.party_role_map, Parameter4=self.param4, Value4=self.ClOrdId))
        #
        # self.read_log_verifier.set_case_id(bca.create_event("ReadLog: Sell-side", self.test_id))
        # self.read_log_verifier.check_read_log_message(compare_message, self.key_params_read_log)
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
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.dma_xpar_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_child_of_LitDark_Iceberg_params_with_PartyInfo()
        self.dma_xpar_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_xpar, OrderQty=self.display_qty, Price=self.price, Instrument=self.instrument)).update_repeating_group('NoParty', self.no_party).add_tag(dict(AlgoCst03=self.party_id))
        self.fix_verifier_buy.check_fix_message(self.dma_xpar_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_xpar_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_xpar_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        time.sleep(10)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_Iceberg_order = FixMessageOrderCancelRequest(self.Iceberg_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_Iceberg_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_Iceberg_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel Iceberg child order
        er_cancel_dma_xpar_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_xpar_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_xpar_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child Iceberg order")
        # endregion

        er_cancel_Iceberg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Iceberg_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_Iceberg_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)