import logging
from datetime import datetime
from posixpath import expanduser
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import message_to_grpc, convert_to_request
from rule_management import RuleManager
from stubs import Stubs

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
price2 = 29.995


def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account,
                                                                         ex_destination_1, price)
    nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account,
                                                                          ex_destination_1, price2)
    trade = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1,
                                                                      31, 31, 50000, 500, 0)
    trade2 = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1,
                                                                      29.995, 29.985, 20000, 1000, 0)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)
    return [ ocr_rule]


def rule_destroyer(list_rules):
    rule_manager = RuleManager()
    for rule in list_rules:
        rule_manager.remove_rule(rule)


def execute(report_id):
    try:
        rule_creation()
        # new_order_single_params = {
        #     # 'header': {
        #     #     'OnBehalfOfCompID': 'kames_ul_DCOI'
        #     # },
        #     'Account': "CLIENT1",
        #     'ClOrdID': bca.client_orderid(9),
        #     'HandlInst': 2,
        #     'Side': 1,
        #     'OrderQty': 10000000,
        #     'TimeInForce': 0,
        #     'Price': 117,
        #     'OrdType': 2,
        #     'TransactTime': datetime.utcnow().isoformat(),
        #     'Instrument': instrument,
        #     'OrderCapacity': 'A',
        #     'Currency': "GBX",
        #     'TargetStrategy': 1005,
        #     'ExDestination': 'XPAR',
        #     # 'QuodFlatParameters': {
        #     #     'NavigatorPercentage': '100',
        #     #     'NavigatorExecution': '1',
        #     #     'NavigatorInitialSweepTime': '5',
        #     #     'NavGuard': '0',
        #     #     'AllowedVenues': 'XLON'
        #     # }
        # }
        #
        # Stubs.fix_act.sendMessage(request=convert_to_request(
        #     'Send NewOrderSingle',
        #     "fix-sell-side-316-ganymede",
        #     report_id,
        #     message_to_grpc('NewOrderSingle', new_order_single_params,
        #                     "fix-sell-side-316-ganymede")
        # ))
    except:
        logging.error("Error execution", exc_info=True)
