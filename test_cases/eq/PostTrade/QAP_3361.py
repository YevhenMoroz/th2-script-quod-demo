import logging
import time

from custom.basic_custom_actions import create_event
import test_framework.old_wrappers.eq_fix_wrappers
from test_cases.wrapper import eq_wrappers
from rule_management import RuleManager
from stubs import Stubs
# initialize logger
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def execute(report_id, session_id):
    # region Declarations
    case_name = "QAP-3361"
    qty = "100"
    price = "10"
    handl_inst = "2"
    side = "2"
    client = "MOClient6"
    ord_type = "2"
    tif = "0"
    venue = "XPAR"
    settlement_currency = "USD"
    exchange_rate = "2"
    exchange_rate_calc = "M"
    buy_connectivity = test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity()
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    # endregion

    # Open FE
    # eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)

    # region Create FIX DMA order
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(session=buy_connectivity,
                                                            account=client + "_PARIS", venue=venue, price=float(price))
        trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade(session=buy_connectivity,account=client + "_PARIS", venue=venue,
                                                                       price=float(price), traded_qty=int(qty), delay=0)
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id=case_id, handl_inst=handl_inst, side=side, client=client, ord_type=ord_type, qty=qty, tif=tif, price=price)
    except Exception:
        logger.error("Error during order creation", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(trade_rule)
    # endregion

    # region Book order
    # eq_wrappers.book_order(request=base_request, client=client, agreed_price=price, settlement_currency=settlement_currency,
    #                        exchange_rate=exchange_rate, exchange_rate_calc=exchange_rate_calc)
    # endregion