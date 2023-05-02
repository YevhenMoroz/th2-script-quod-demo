import os
import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators, Simulators

from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.algo_formulas_manager import AlgoFormulasManager
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import \
    FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.core.test_case import TestCase
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, Reference
from datetime import datetime, timedelta

from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T4679(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, data_set=None, environment=None):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.fix_env1 = self.environment.get_list_fix_environment()[0]
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        # region th2 components
        self.fix_manager_sell = FixManager(self.fix_env1.sell_side, self.test_id)
        self.fix_manager_feed_handler = FixManager(self.fix_env1.feed_handler, self.test_id)
        self.fix_verifier_sell = FixVerifier(self.fix_env1.sell_side, self.test_id)
        self.fix_verifier_buy = FixVerifier(self.fix_env1.buy_side, self.test_id)
        # endregion
        self.qty = 300
        self.price = 17
        self.price_child = 9.999
        self.algo = 'QuodTWAP'
        self.price_ask = 20
        self.price_bid = 10
        self.qty_ask = 100
        self.qty_bid = 100
        self.waves = 3
        self.neutral_price = 15

        self.passive_reference_price = Reference.Primary.value
        self.passive_offset = -1
        self.limit_price_reference = Reference.Mid.value
        self.limit_price_offset = -1
        self.qty_child = AlgoFormulasManager.get_next_twap_slice(self.qty, self.waves)

        self.last_trade_price = 17
        self.last_trade_qty = 100
        self.listing_id = self.data_set.get_listing_id_by_name("listing_36")

        self.neutral_reference_price = Reference.Mid.value


        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")

        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name('account_2')

        # Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_1')
        self.key_params = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_3')
        self.key_params_mkt = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_4')

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel_replace = Status.CancelReplace
        self.status_cancel = Status.Cancel
        self.status_reject = Status.Reject
        self.status_eliminate = Status.Eliminate
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion
        # region SSH
        # self.config_file = "client_sats.xml"
        # self.xpath = ".//bpsOffsets"
        # self.new_config_value = 'false'
        # self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        # self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user, self.ssh_client_env.password, self.ssh_client_env.su_user, self.ssh_client_env.su_password)
        # self.default_config_value = self.ssh_client.get_and_update_file(self.config_file, self.xpath, self.new_config_value)

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Prepare SATS configuration
        # self.ssh_client.send_command("qrestart SATS")
        # time.sleep(35)
        # endregion
        self.now = datetime.utcnow()
        self.end_date = (self.now + timedelta(minutes=3)).strftime("%Y%m%d-%H:%M:%S")
        self.start_date = self.now.strftime("%Y%m%d-%H:%M:%S")
        # region rules
        rule_manager = RuleManager(Simulators.algo)

        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price_child)
        ocrr = rule_manager.add_OCRR(self.fix_env1.buy_side)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)

        self.rule_list = [nos_rule, ocr_rule, ocrr]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        # endregion
        # region Send MarketDate
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.last_trade_qty).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.last_trade_price)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        # region Send NewOrderSingle (35=D)
        self.case_id_1 = bca.create_event("Create Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(self.case_id_1)

        self.twap_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_TWAP_Redburn_params()
        self.twap_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.twap_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_1))
        self.twap_order.update_fields_in_component('QuodFlatParameters', dict(Waves=self.waves, LimitPriceReference=self.limit_price_reference, LimitPriceOffset=self.limit_price_offset, Passive=self.passive_reference_price, PassiveOffset=self.passive_offset, Neutral=self.neutral_reference_price,  StartDate2=self.start_date, EndDate2=self.end_date))

        self.fix_manager_sell.send_message_and_receive_response(self.twap_order, self.case_id_1)

        time.sleep(5)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.twap_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_twap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_twap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        time.sleep(35)
        # endregion

        # region Check Buy side
        # Check TWAP child
        self.case_id_2 = bca.create_event("TWAP DMA child order", self.test_id)
        self.fix_verifier_buy.set_case_id(self.case_id_2)

        self.twap_child = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        #
        self.twap_child.change_parameters(dict(OrderQty=self.qty_child, Price=self.price_child, Account=self.account, Instrument='*', ExDestination=self.ex_destination_1))
        self.fix_verifier_buy.check_fix_message(self.twap_child, key_parameters=self.key_params, message_name='Buy side NewOrderSingle TWAP child')

        pending_twap_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_child, self.gateway_side_buy, self.status_pending)
        pending_twap_child_params.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_1))

        self.fix_verifier_buy.check_fix_message(pending_twap_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew TWAP child')

        new_twap_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_child, self.gateway_side_buy, self.status_new)

        self.fix_verifier_buy.check_fix_message(new_twap_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New TWAP child')

        # endregion

        neutral_twap_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_child, self.gateway_side_buy, self.status_cancel_replace)
        neutral_twap_child_params.change_parameters(dict(Price=self.neutral_price))
        self.fix_verifier_buy.check_fix_message(neutral_twap_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport neutral TWAP child')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region cancel Order

        self.case_id_cancel = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(self.case_id_cancel)
        cancel_request_twap_order = FixMessageOrderCancelRequest(self.twap_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_twap_order, self.case_id_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_request_twap_order, direction=ToQuod, message_name='Sell side Cancel Request')

        time.sleep(3)
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        # self.ssh_client.get_and_update_file(self.config_file, self.xpath, self.default_config_value)
        # self.ssh_client.send_command("qrestart SATS")
        # time.sleep(35)
        # self.ssh_client.close()

        self.fix_verifier_buy.set_case_id(self.case_id_cancel)
        cancel_twap_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_child, self.gateway_side_buy, self.status_cancel_replace)
        cancel_twap_child_params.change_parameter('Price', self.neutral_price)
        self.fix_verifier_buy.check_fix_message(cancel_twap_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Cancel TWAP child')

        cancel_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.twap_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_twap_order_params, key_parameters=self.key_params, message_name='Sell side ExecReport Cancel')
        # endregion
