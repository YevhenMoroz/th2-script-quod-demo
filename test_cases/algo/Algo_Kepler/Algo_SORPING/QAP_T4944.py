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
from test_framework.read_log_wrappers.algo_messages.ReadLogMessageAlgo import ReadLogMessageAlgo
from test_framework.read_log_wrappers.algo.ReadLogVerifierAlgo import ReadLogVerifierAlgo


class QAP_T4944(TestCase):
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
        self.qty = 5
        self.price = 281
        self.price_ask = 40
        self.price_bid = 1
        self.qty_bid = self.qty_ask = 1000000
        self.tif_gtc = constants.TimeInForce.GoodTillCancel.value
        self.tif_gtd = constants.TimeInForce.GoodTillDate.value
        self.algopolicy = constants.ClientAlgoPolicy.qa_multiple_y.value
        self.party_id = constants.PartyID.party_id_5.value
        self.party_id_source = constants.PartyIDSource.party_id_source_1.value
        self.party_role = constants.PartyRole.party_role_12.value

        now = datetime.today() - timedelta(hours=3)
        self.ExpireDate=(now + timedelta(days=365)).strftime("%Y%m%d")

        self.no_party = [
            {'PartyID': self.party_id, 'PartyIDSource': self.party_id_source,
             'PartyRole': self.party_role}
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
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_19")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_xams = self.data_set.get_mic_by_name("mic_31")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.account_xams = self.data_set.get_account_by_name("account_14")
        self.listing_id_xams = self.data_set.get_listing_id_by_name("listing_30")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

        # region Read log verifier params
        self.log_verifier_by_name = constants.ReadLogVerifiers.log_319_check_primary_listing.value
        self.read_log_verifier = ReadLogVerifierAlgo(self.log_verifier_by_name, report_id)
        # endregion

        self.pre_filter = self.data_set.get_pre_filter("pre_filter_primary_listing_id")
        self.pre_filter['PrimaryListingID'] = (self.listing_id_xams, "EQUAL")
        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_xams, self.ex_destination_xams, self.price)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_xams, self.ex_destination_xams, True)
        self.rule_list = [nos_rule, ocr_rule]
        # endregion

        # region Send_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_xams = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_xams, self.fix_env1.feed_handler)
        market_data_snap_shot_xams.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_xams.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_xams)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for SynthMinQty order
        case_id_1 = bca.create_event("Create SORPING GTC Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.SORPING_GTC_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multiple_Emulation_params()
        self.SORPING_GTC_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.SORPING_GTC_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ClientAlgoPolicyID=self.algopolicy, TimeInForce=self.tif_gtc)).add_fields_into_repeating_group('NoParty', self.no_party).add_tag(dict(ComplianceID='FX5', AlgoOrderStrategy='2146849719'))

        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_GTC_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.SORPING_GTC_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_SORPING_GTC_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_GTC_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_SORPING_GTC_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_SORPING_GTC_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_GTC_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_SORPING_GTC_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.dma_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_Multiple_Emulation_params()
        self.dma_order.change_parameters(dict(Account=self.account_xams, ExDestination=self.ex_destination_xams, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, TimeInForce=self.tif_gtd)).add_tag(dict(ExpireDate=self.ExpireDate)).add_fields_into_repeating_group('NoParty', self.no_party)
        self.fix_verifier_buy.check_fix_message(self.dma_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        # region Check Read log
        time.sleep(70)

        compare_message = ReadLogMessageAlgo().set_compare_message_for_check_primary_listing()
        compare_message.change_parameters(dict(PrimaryListingID=self.listing_id_xams))

        self.read_log_verifier.set_case_id(bca.create_event("ReadLog", self.test_id))
        self.read_log_verifier.check_read_log_message_sequence([compare_message, compare_message, compare_message], [None, None, None], pre_filter=self.pre_filter)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_4 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_4)
        cancel_request_SORPING_GTC_order = FixMessageOrderCancelRequest(self.SORPING_GTC_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_SORPING_GTC_order, case_id_4)
        self.fix_verifier_sell.check_fix_message(cancel_request_SORPING_GTC_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel first dma child order
        er_cancel_dma_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA 1 order")

        er_cancel_SORPING_GTC_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_GTC_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_SORPING_GTC_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
