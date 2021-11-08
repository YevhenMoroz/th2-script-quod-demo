import logging
import os
from datetime import datetime
from posixpath import expanduser
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import message_to_grpc, convert_to_request
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
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
    return [nos_rule, nos_rule2, trade, trade2, ocr_rule]



def execute(report_id):
    try:
        rule_list = rule_creation()

        ss = FixMessageNewOrderSingleAlgo().set_TWAP_Navigator_Guard().add_ClordId((os.path.basename(__file__)[:-3]))
        fixmanager = FixManager("fix-sell-side-316-gnmd-rb", report_id)

        fixmanager.send_message_and_receive_response(ss)


    except:
        logging.error("Error execution", exc_info=True)
    finally:
        RuleManager.rule_destroyer(rule_list)
