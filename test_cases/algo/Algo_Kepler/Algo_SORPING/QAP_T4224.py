import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.algo_formulas_manager import AlgoFormulasManager
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets import constants
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase


class QAP_T4224(TestCase):
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
        self.price = 20
        self.price_ask = 40
        self.price_bid = 30
        self.qty_bid = self.qty_ask = 10000
        self.delay = 3000
        self.tif_gtd = constants.TimeInForce.GoodTillDate.value
        self.party_id_1 = constants.PartyID.party_id_6.value
        self.party_id_2 = constants.PartyID.party_id_7.value
        self.party_id_source = constants.PartyIDSource.party_id_source_2.value
        self.party_role_1 = constants.PartyRole.party_role_12.value
        self.party_role_2 = constants.PartyRole.party_role_3.value

        self.no_party = [
            {'PartyID': self.party_id_1, 'PartyIDSource': self.party_id_source,
             'PartyRole': self.party_role_1},
            {'PartyID': self.party_id_2, 'PartyIDSource': self.party_id_source,
             'PartyRole': self.party_role_2},
           ]

        now = datetime.today() - timedelta(hours=3)
        delta = 4
        expire_date = (now + timedelta(days=delta))
        self.ExpireDate_for_sending = expire_date.strftime("%Y%m%d")
        shift = AlgoFormulasManager.make_expire_date_friday_if_it_is_on_weekend(expire_date)
        self.ExpireDate = (expire_date - timedelta(days=shift)).strftime("%Y%m%d")
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_eliminate = Status.Eliminate
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
        self.ex_destination_qdl11 = self.data_set.get_mic_by_name("mic_28")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account_qdl11 = self.data_set.get_account_by_name("account_9")
        self.listing_id_qdl11 = self.data_set.get_listing_id_by_name("listing_27")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        self.key_params_ER_eliminate_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_cancel_reject_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_eliminate_rule = rule_manager.add_NewOrderSingle_ExecutionReport_Eliminate(self.fix_env1.buy_side, self.account_qdl11, self.ex_destination_qdl11, self.price, self.delay)
        self.rule_list = [nos_eliminate_rule]
        # endregion

        # region Send_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl11 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl11, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl11.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_qdl11.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl11)
        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create Synthetic TIF Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.Synthetic_TIF_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Kepler_DMA_params()
        self.Synthetic_TIF_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Synthetic_TIF_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_qdl11, TimeInForce=self.tif_gtd)).add_fields_into_repeating_group('NoParty', self.no_party).add_tag(dict(ExpireDate=self.ExpireDate_for_sending))

        self.fix_manager_sell.send_message_and_receive_response(self.Synthetic_TIF_order, case_id_1)
        # endregion
        
        # region Cancel Synthetic TIF order
        case_id_2 = bca.create_event("Cancel Synthetic TIF Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_Synthetic_TIF_order = FixMessageOrderCancelRequest(self.Synthetic_TIF_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_Synthetic_TIF_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_Synthetic_TIF_order, direction=self.ToQuod, message_name='Sell side Cancel Request')
        # endregion

        time.sleep(3)

        # region Check Sell side
        self.fix_verifier_sell.set_case_id(bca.create_event("Check Synthetic TIF order", self.test_id))

        self.fix_verifier_sell.check_fix_message(self.Synthetic_TIF_order, self.key_params_NOS_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_Synthetic_TIF_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single_for_Kepler_DMA(self.Synthetic_TIF_order, self.status_pending)
        er_pending_new_Synthetic_TIF_order_params.change_parameters(dict(ExpireDate=self.ExpireDate))
        self.fix_verifier_sell.check_fix_message(er_pending_new_Synthetic_TIF_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_Synthetic_TIF_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single_for_Kepler_DMA(self.Synthetic_TIF_order, self.status_new)
        er_new_Synthetic_TIF_order_params.add_tag(dict(TargetStrategy='*')).change_parameters(dict(ExpireDate=self.ExpireDate))
        self.fix_verifier_sell.check_fix_message(er_new_Synthetic_TIF_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check Lit child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.dma_qdl11_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Kepler_DMA_child_params()
        self.dma_qdl11_order.change_parameters(dict(Account=self.account_qdl11, ExDestination=self.ex_destination_qdl11, OrderQty=self.qty, Price=self.price, Instrument=self.instrument)).add_fields_into_repeating_group('NoParty', self.no_party)
        self.fix_verifier_buy.check_fix_message(self.dma_qdl11_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')
        # endregion

        time.sleep(2)
        
        # region Check eliminate child DMA order
        er_eliminate_dma_qdl11_order_params = FixMessageExecutionReportAlgo().set_params_for_nos_eliminate_rule(self.dma_qdl11_order)
        self.fix_verifier_buy.check_fix_message(er_eliminate_dma_qdl11_order_params, key_parameters=self.key_params_ER_eliminate_child, direction=self.ToQuod, message_name='Buy side ExecReport Eliminate Child DMA 1 order')
        # endregion
        
        # region Check that Synthetic TIF order was canceled
        er_cancel_Synthetic_TIF_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single_for_Kepler_DMA(self.Synthetic_TIF_order, self.status_cancel)
        er_cancel_Synthetic_TIF_order_params.add_tag(dict(TargetStrategy='*')).change_parameters(dict(ExpireDate=self.ExpireDate))
        self.fix_verifier_sell.check_fix_message(er_cancel_Synthetic_TIF_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion
        
    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
