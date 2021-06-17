import time
import datetime

from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import create_event
from win_gui_modules.utils import set_session_id, get_base_request
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    case_name = "QAP-3349"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "50"
    client = "CLIENTYMOROZ"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)
    data = datetime.datetime.now()
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew('fix-buy-317ganymede-standard',
                                                                             'CLIENTYMOROZ_PARIS', "XPAR", int(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade('fix-buy-317ganymede-standard',
                                                                      'CLIENTYMOROZ_PARIS', 'XPAR',
                                                                      int(price), int(qty), 1)
        fix_message = eq_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 0, price)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion
    # region Book
    eq_wrappers.book_order(base_request, client, price, settlement_type="Regular", settlement_currency="USD",
                           pset="CREST", exchange_rate="2", exchange_rate_calc="Multiply")
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "ApprovalPending")
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Unmatched")
    eq_wrappers.verify_block_value(base_request, case_id, "SettlType", "Regular")
    eq_wrappers.verify_block_value(base_request, case_id, "SettlCurrency", "USD")
    eq_wrappers.verify_block_value(base_request, case_id, "SettlCurrFxRateCalc", "M")
    eq_wrappers.verify_block_value(base_request, case_id, "ExchangeRate", "2")
    eq_wrappers.verify_block_value(base_request, case_id, "SettlDate", data.strftime("%#m/%#d/%Y"))
    eq_wrappers.verify_block_value(base_request, case_id, "PSET", "CREST")
    eq_wrappers.verify_block_value(base_request, case_id, "PSET BIC", "CRSTGB22")
    # endregion
    # region Amend block
    data += datetime.timedelta(days=1)
    eq_wrappers.amend_block(base_request, settlement_currency="UAH",
                            settlement_date=data.strftime("%#m/%#d/%Y"), exchange_rate="3", exchange_rate_calc="Divide",
                            pset="EURO_CLEAR")
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "ApprovalPending")
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Unmatched")
    eq_wrappers.verify_block_value(base_request, case_id, "SettlCurrency", "UAH")
    eq_wrappers.verify_block_value(base_request, case_id, "SettlCurrFxRateCalc", "D")
    eq_wrappers.verify_block_value(base_request, case_id, "ExchangeRate", "3")
    eq_wrappers.verify_block_value(base_request, case_id, "SettlDate", data.strftime("%#m/%#d/%Y"))
    eq_wrappers.verify_block_value(base_request, case_id, "PSET", "EURO_CLEAR")
    eq_wrappers.verify_block_value(base_request, case_id, "PSET BIC", "MGTCBEBE")
    # endregion
