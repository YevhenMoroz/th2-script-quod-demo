import logging

from th2_grpc_hand import rhbatch_pb2

from custom.basic_custom_actions import timestamps
from test_cases.wrapper import eq_wrappers
from test_framework.old_wrappers.eq_wrappers import *
from stubs import Stubs
from win_gui_modules.utils import call, get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP_TEST"
    seconds, nanos = timestamps()  # Store case start time
    case_id = create_event(case_name, report_id)
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "20"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    order_type = "Limit"
    recipient = 'vskulinec'
    recipient_user = 'vskulinec'
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    session_id2 = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    #  endregion
    # region create CO
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity('100')
    order_ticket.set_care_order(recipient, True)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    order_ticket.set_tif(tif='Day')
    order_ticket.set_limit(price)
    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)  # VETO
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    order_ticket_service = Stubs.win_act_order_ticket
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(sell_connectivity,
                                                                             client + "_PARIS", "XPAR", int(price))
        call(order_ticket_service.placeOrder, new_order_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail create_order')
    finally:
        rule_manager.remove_rule(nos_rule)

    # endregion
