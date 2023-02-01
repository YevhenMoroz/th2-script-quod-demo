import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.DataSet import DirectionEnum, Connectivity, GatewaySide, Status
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

class QAP_T4292(TestCase):
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

        # order param
        self.avt = 10000  # average volume traded per minute
        self.ast = self.avt * 5  # 5 average traded
        self.qty = 100000
        self.waves = 5
        self.qty_twap_1 = int(self.qty / self.waves)
        self.first_reserve = max(self.ast, int(self.qty * (1 - 1)))
        self.reserve = max(self.first_reserve, int(self.qty_twap_1))
        self.qty_nav = self.qty - self.reserve

        self.price = 30
        self.price2 = 31
        self.price3 = 29.995
        self.price4 = 30.5


        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name('account_1')
        self.s_par = self.data_set.get_listing_id_by_name('listing_36')

        # Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_1')
        self.key_params = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_2')

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        self.status_reject = Status.Reject
        self.status_fill = Status.Fill
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        self.text_reject_navigator_limit_price = DataSet.FreeNotesReject.MissNavigatorLimitPrice.value

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price)
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price2)
        nos_rule3 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price3)
        nos_rule4 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, True, 1000, 31)
        nos_rule5 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price4)
        nos_rule6 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, 30.4975)
        trade = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price3, self.price3, 20000, 1000, 0)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [nos_rule, nos_rule2, nos_rule3, nos_rule4, nos_rule5, nos_rule6, trade, ocrr_rule, ocr_rule]

        start_time = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S")
        end_time = (datetime.utcnow() + timedelta(minutes=5)).strftime("%Y%m%d-%H:%M:%S")


        new_order_single = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_TWAP_Navigator_Guard_params().add_ClordId((os.path.basename(__file__)[:-3]))
        new_order_single.change_parameters(dict(OrderQty=100000))
        new_order_single.change_parameters(dict(Price=31))

        new_order_single.update_fields_in_component("QuodFlatParameters", dict(TriggerPriceRed=31, StartDate2=start_time, EndDate2=end_time))

        self.fix_manager_sell.send_message_and_receive_response(new_order_single)
        self.fix_verifier_sell.check_fix_message(new_order_single, direction=DirectionEnum.ToQuod)

        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot)

        execution_report = FixMessageExecutionReportAlgo().set_params_from_new_order_single(new_order_single, GatewaySide.Sell, Status.Pending)
        self.fix_verifier_sell.check_fix_message(execution_report)

        execution_report2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(new_order_single, GatewaySide.Sell, Status.New)
        self.fix_verifier_sell.check_fix_message(execution_report2)

        market_data_snap_shot_2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        data = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '30',
                'MDEntrySize': '1000000',
                'MDEntryPositionNo': '1',
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '31',
                'MDEntrySize': '81000',
                'MDEntryPositionNo': '1',
            }
        ]

        market_data_snap_shot_2.update_repeating_group("NoMDEntries", data)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_2)

        time.sleep(1)
        market_data_snap_shot_3 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        data = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '30',
                'MDEntrySize': '1000000',
                'MDEntryPositionNo': '1',
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '40',
                'MDEntrySize': '31000',
                'MDEntryPositionNo': '1',
            }
        ]

        market_data_snap_shot_2.update_repeating_group("NoMDEntries", data)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_3)

        time.sleep(15)
        order_cancel = FixMessageOrderCancelRequest(new_order_single)
        self.fix_manager_sell.send_message_and_receive_response(order_cancel)
    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):

        time.sleep(15)
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
