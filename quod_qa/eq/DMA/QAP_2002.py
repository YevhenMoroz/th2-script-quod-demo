import logging
import os
from datetime import datetime

from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs

from quod_qa.wrapper.fix_verifier import FixVerifier
from test_cases.QAP_2864 import simulator
from win_gui_modules.order_book_wrappers import OrdersDetails

from custom.basic_custom_actions import create_event, timestamps
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-2002"
    seconds, nanos = timestamps()  # Store case start time
    # region Declaration
    seconds, nanos = timestamps()  # Store case start time
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = 900
    client = "CLIENT1"
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    # endregion

    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_MarketNewOrdSingle_FOK(eq_wrappers.get_buy_connectivity(), 'XPAR_'+client, 'XPAR',
                                                           float(1), True)
        fix_message = eq_wrappers.create_order_via_fix(case_id, 2, 2, client, 1, qty, 4)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(nos_rule)

        # endregion

        # region Check values in OrderBook
    params = {
        'OrderQty': qty,
        'ExecType': 'F',
        'OrdStatus': '2',
        'Account': 'CLIENT1',
        'Side': 2,
        'Text': '*',
        'TimeInForce': 4,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'LastExecutionPolicy': '*',
        'TradeDate': '*',
        'AvgPx': '*',
        'ExpireDate': '*',
        'SettlDate': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'SettlType': '*',
        'OrdType': '*',
        'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SecondaryOrderID': '*',
        'NoParty': '*',
        'Instrument': '*',
        'SecondaryExecID': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*'
    }

    fix_verifier_ss = FixVerifier(eq_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'OrdStatus','TimeInForce'])

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
