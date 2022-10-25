import logging
import os
import time
from test_framework.fix_wrappers.DataSet import DirectionEnum, Connectivity, GatewaySide, Status
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from rule_management import RuleManager, Simulators

timeouts = True

instrument = {
    'Symbol': 'FR0000062788_EUR',
    'SecurityID': 'FR0000062788',
    'SecurityIDSource': '4',
    'SecurityExchange': 'XPAR'
}

connectivity_buy_side = "fix-buy-side-316-ganymede"
connectivity_sell_side = "fix-sell-side-310-ganymede-redburn"
account = "XPAR_CLIENT1"
ex_destination_1 = "XPAR"
price = 30
price2 = 31
price3 = 29.995


def rule_creation():
    rule_manager = RuleManager(Simulators.algo)
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account,
                                                                         ex_destination_1, price)
    nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account,
                                                                          ex_destination_1, price2)
    nos_rule3 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account,
                                                                          ex_destination_1, price3)
    trade = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1,
                                                                      price3, price3, 20000, 1000, 0)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)
    return [nos_rule, nos_rule2, nos_rule3, trade, ocr_rule]


def execute(report_id):
    try:
        rule_list = rule_creation()

        fix_manager = FixManager(Connectivity.Ganymede_316_Redburn.value, report_id)
        fix_verifier = FixVerifier(Connectivity.Ganymede_316_Redburn.value, report_id)

        new_order_single = FixMessageNewOrderSingleAlgo().set_TWAP_Navigator_Guard_params().add_ClordId((os.path.basename(__file__)[:-3]))
        new_order_single.change_parameters(dict(OrderQty=100000))
        new_order_single.change_parameters(dict(Price=31))

        fix_manager.send_message_and_receive_response(new_order_single)
        fix_verifier.check_fix_message(new_order_single, direction=DirectionEnum.ToQuod)

        execution_report = FixMessageExecutionReportAlgo().set_params_from_new_order_single(new_order_single, GatewaySide.Sell, Status.Pending)
        fix_verifier.check_fix_message(execution_report)

        execution_report2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(new_order_single, GatewaySide.Sell, Status.New)
        fix_verifier.check_fix_message(execution_report2)



        time.sleep(15)
        order_cancel = FixMessageOrderCancelRequest(new_order_single)
        fix_manager.send_message_and_receive_response(order_cancel)
    except:
        logging.error("Error execution", exc_info=True)
    finally:
        RuleManager.remove_rules(rule_list)
