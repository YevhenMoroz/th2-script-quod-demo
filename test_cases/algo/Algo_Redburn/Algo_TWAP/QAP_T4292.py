import logging
import os
import time

from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.DataSet import DirectionEnum, Connectivity, GatewaySide, Status
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from rule_management import RuleManager, Simulators

timeouts = True

instrument = {
    'Symbol': 'FR0000064578_EUR',
    'SecurityID': 'FR0000064578',
    'SecurityIDSource': '4',
    'SecurityExchange': 'XPAR'
}

s_par = '555'
connectivity_buy_side = "fix-buy-side-316-ganymede"
connectivity_sell_side = "fix-sell-side-310-ganymede-redburn"
connectivity_fh = DataSet.Connectivity.Ganymede_316_Feed_Handler.value
account = "XPAR_CLIENT1"
ex_destination_1 = "XPAR"
price = 30
price2 = 31
price3 = 29.995
price4 = 30.5


def rule_creation():
    rule_manager = RuleManager(Simulators.algo)
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account,
                                                                         ex_destination_1, price)
    nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account,
                                                                          ex_destination_1, price2)
    nos_rule3 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account,
                                                                          ex_destination_1, price3)
    nos_rule4 = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, account,
                                                                          ex_destination_1, True, 1000, 31)
    nos_rule5 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account,
                                                                          ex_destination_1, price4)
    nos_rule6 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account,
                                                                          ex_destination_1, 30.4975)
    trade = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1,
                                                                      price3, price3, 20000, 1000, 0)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)

    ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(connectivity_buy_side, account, ex_destination_1, True)
    return [nos_rule, nos_rule2, nos_rule3, nos_rule4, nos_rule5,nos_rule6, trade, ocrr_rule, ocr_rule]


def execute(report_id):
    try:
        #TODO add checks
        rule_list = rule_creation()

        fix_manager = FixManager(Connectivity.Ganymede_316_Redburn.value, report_id)
        fix_verifier = FixVerifier(Connectivity.Ganymede_316_Redburn.value, report_id)
        fix_manager_fh = FixManager(connectivity_fh, report_id)

        new_order_single = FixMessageNewOrderSingleAlgo().set_TWAP_Navigator_Guard_params().add_ClordId((os.path.basename(__file__)[:-3]))
        new_order_single.change_parameters(dict(OrderQty=100000))
        new_order_single.change_parameters(dict(Price=31))
        new_order_single.update_fields_in_component("QuodFlatParameters", dict(TriggerPriceRed=31))
        # new_order_single.change_parameter("Instrument", instrument)

        fix_manager.send_message_and_receive_response(new_order_single)
        fix_verifier.check_fix_message(new_order_single, direction=DirectionEnum.ToQuod)

        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        fix_manager_fh.send_message(market_data_snap_shot)

        execution_report = FixMessageExecutionReportAlgo().set_params_from_new_order_single(new_order_single, GatewaySide.Sell, Status.Pending)
        fix_verifier.check_fix_message(execution_report)

        execution_report2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(new_order_single, GatewaySide.Sell, Status.New)
        fix_verifier.check_fix_message(execution_report2)

        market_data_snap_shot_2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
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
        fix_manager_fh.send_message(market_data_snap_shot_2)

        time.sleep(1)
        market_data_snap_shot_3 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
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
        fix_manager_fh.send_message(market_data_snap_shot_3)

        time.sleep(15)
        order_cancel = FixMessageOrderCancelRequest(new_order_single)
        fix_manager.send_message_and_receive_response(order_cancel)
    except:
        logging.error("Error execution", exc_info=True)
    finally:
        RuleManager.remove_rules(rule_list)
