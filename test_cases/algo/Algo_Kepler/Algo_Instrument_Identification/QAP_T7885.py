import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T7885(TestCase):
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
        self.qty = 200
        self.price = 150
        self.qty_for_md = 1000
        self.price_ask = 40
        self.price_bid = 30
        self.px_for_incr = 0
        self.side = constants.OrderSide.Sell.value
        self.currency = self.data_set.get_currency_by_name("currency_4")
        self.algopolicy = constants.ClientAlgoPolicy.qa_sorping_13.value
        self.text_1 = constants.RejectMessages.no_listing_1.value
        self.text_2 = constants.RejectMessages.no_listing_10.value
        self.text_3 = constants.RejectMessages.no_listing_4.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_reject = Status.Reject
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_29")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_xetr = self.data_set.get_listing_id_by_name("listing_51")
        self.listing_id_cceu = self.data_set.get_listing_id_by_name("listing_52")
        # endregion

        # region Instrument parameters
        self.symbol = constants.Symbol.symbol_3.value
        self.sid = constants.SecurityID.security_id_4.value
        self.sids = constants.SecurityIDSource.sids_4.value
        self.sec_type = constants.SecurityType.cs.value
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_3")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_ER_eliminate_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_Reject_Eliminate_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_xetr = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_xetr, self.fix_env1.feed_handler)
        market_data_snap_shot_xetr.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_xetr.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_xetr)

        market_data_snap_shot_cceu = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_cceu, self.fix_env1.feed_handler)
        market_data_snap_shot_cceu.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_cceu.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_cceu)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for SORPING order
        case_id_1 = bca.create_event("Create SORPING Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.SORPING_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_SORPING_Kepler_params()
        self.SORPING_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.SORPING_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=dict(Symbol=self.symbol, SecurityID=self.sid, SecurityIDSource=self.sids, SecurityType=self.sec_type), Currency=self.currency, Side=self.side, ClientAlgoPolicyID=self.algopolicy))

        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.SORPING_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_reject_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_reject)
        er_reject_SORPING_order_params.remove_parameters(['SecondaryAlgoPolicyID', 'ExecRestatementReason']).add_tag(dict(OrdRejReason='*')).change_parameters(dict(Text=(self.text_1, self.text_2, self.text_3), Price='*'))
        self.fix_verifier_sell.check_fix_message(er_reject_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Reject')
