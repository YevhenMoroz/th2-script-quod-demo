import logging
import time

from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest

import quod_qa.wrapper.eq_fix_wrappers
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_wrappers
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3911"
    # region Declarations
    qty = "900"
    price = "20"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    # endregion
    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # # region create & trade DMA
    # try:
    #     rule_manager = RuleManager()
    #     nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
    #         quod_qa.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
    #         client + '_PARIS', "XPAR", float(price))
    #     nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
    #         quod_qa.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
    #         client + '_PARIS', 'XPAR',
    #         float(price), int(qty), 1)
    #     quod_qa.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 0, price)
    # except Exception:
    #     logger.error("Error execution", exc_info=True)
    # finally:
    #     time.sleep(1)
    #     rule_manager.remove_rule(nos_rule)
    #     rule_manager.remove_rule(nos_rule2)
    # exec_id = eq_wrappers.get_2nd_lvl_order_detail(base_request, "ExecID")
    # # endregion
    # # region create CO
    # quod_qa.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 1, qty, 0)
    # eq_wrappers.accept_order(lookup, qty, price)
    # co_order = eq_wrappers.get_order_id(base_request)
    # # endregion
    # region Manual Match
    exec_id='EX1211008155859460001'
    co_order='CO1211008155906403001'
    eq_wrappers.manual_match(base_request, qty, ["OrderId", co_order], ["ExecID", exec_id])
    co_exec = eq_wrappers.get_2nd_lvl_order_detail(base_request, "ExecID")
    # endregion
    # region Verify
    #eq_wrappers.verify_order_value(base_request, case_id, "UnmatchedQty", qty)
    #eq_wrappers.verify_order_value(base_request, case_id, "ExecSts", "Filled")
    # endregion
    # region JavaApi Un-match
    act_java_api = Stubs.act_java_api
    connectivity = '317_java_api'
    trade_params = {
        'SEND_SUBJECT': 'QUOD.CS.FE',
        'AuthenticationBlock': {'UserID': "ymoroz",
                                'RoleID': 'HeadOfSaleDealer',
                                'SessionKey': '45600000214'},
        'UnMatchingElements': {
            'UnMatchingBlock': [
                {'VirtualExecID': co_exec,
                 'UnMatchingQty': int(qty) / 2}
            ]
        },
    }

    act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
        message=bca.message_to_grpc('Order_UnMatching', trade_params, connectivity),
        parent_event_id=case_id))
    # endregion
    # region JavaApi 2nd Un-match
    co_exec2 = eq_wrappers.get_2nd_lvl_order_detail(base_request, "ExecID")
    new_params = {'UnMatchingBlock': [
        {'VirtualExecID': co_exec2,
         'UnMatchingQty': int(qty) / 2}
    ]}
    trade_params.update({'UnMatchingElements': new_params})
    act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
        message=bca.message_to_grpc('Order_UnMatching', trade_params, connectivity),
        parent_event_id=case_id))
    # endregion
