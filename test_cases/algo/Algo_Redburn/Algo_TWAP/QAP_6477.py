import logging
import os
import time

from test_framework.fix_wrappers import DataSet
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.DataSet import DirectionEnum, Connectivity, GatewaySide, Status
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from rule_management import RuleManager

timeouts = True

#venue param
ex_destination_1 = "XPAR"
client = "CLIENT2"
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '555'

#Gateway Side
gateway_side_buy = DataSet.GatewaySide.Buy
gateway_side_sell = DataSet.GatewaySide.Sell

#Status
status_pending = DataSet.Status.Pending
status_new = DataSet.Status.New
status_cancel = DataSet.Status.Cancel

#connectivity
case_name = os.path.basename(__file__)
instrument = DataSet.Instrument.BUI
FromQuod = DataSet.DirectionEnum.FromQuod
ToQuod = DataSet.DirectionEnum.ToQuod
connectivity_buy_side = DataSet.Connectivity.Ganymede_316_Buy_Side.value
connectivity_sell_side = DataSet.Connectivity.Ganymede_316_Redburn.value
connectivity_fh = DataSet.Connectivity.Ganymede_316_Feed_Handler.value

price = 30
price2 = 31
price3 = 29.995
price4 = 30.5


def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price2)
    nos_rule3 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price3)
    nos_rule4 = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, account, ex_destination_1, True, 1000, 31)
    nos_rule5 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price4)
    trade = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1, 31, 31, 25000, 25000, 0)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)
    ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(connectivity_buy_side, account, ex_destination_1, True)
    return [nos_rule, nos_rule2, nos_rule3, nos_rule4, nos_rule5, trade, ocrr_rule, ocr_rule]


def execute(report_id):
    try:
        rule_list = rule_creation()

        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

        fix_manager = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)
        fix_manager_fh = FixManager(connectivity_fh, case_id)

        new_order_single = FixMessageNewOrderSingleAlgo().set_TWAP_Navigator_params().add_ClordId((os.path.basename(__file__)[:-3]))
        new_order_single.change_parameters(dict(OrderQty=75000, Account=account, Price=31))
        new_order_single.update_fields_in_component("QuodFlatParameters", dict(TriggerPriceRed=31, NavigatorInitialSweepTime=15, Waves=2))
        # new_order_single.change_parameter("Instrument", instrument)

        fix_manager.send_message_and_receive_response(new_order_single)
        fix_verifier_ss.check_fix_message(new_order_single, direction=ToQuod)

        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        fix_manager_fh.send_message(market_data_snap_shot)

        execution_report = FixMessageExecutionReportAlgo().set_params_from_new_order_single(new_order_single, gateway_side_sell, status_pending)
        fix_verifier_ss.check_fix_message(execution_report)

        execution_report2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(new_order_single, gateway_side_sell, status_new)
        fix_verifier_ss.check_fix_message(execution_report2)
        time.sleep(5)
        market_data_snap_shot_2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        market_data_snap_shot_2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=30, MDEntrySize=1000000)
        market_data_snap_shot_2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=31, MDEntrySize=10000)

        fix_manager_fh.send_message(market_data_snap_shot_2)

        time.sleep(10)
        market_data_snap_shot_3 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        market_data_snap_shot_3.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=30, MDEntrySize=1000000)
        market_data_snap_shot_3.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=40, MDEntrySize=10000)
        fix_manager_fh.send_message(market_data_snap_shot_3)

        time.sleep(5)
        order_cancel = FixMessageOrderCancelRequest(new_order_single)
        fix_manager.send_message_and_receive_response(order_cancel)
    except:
        logging.error("Error execution", exc_info=True)
    finally:
        RuleManager.remove_rules(rule_list)
