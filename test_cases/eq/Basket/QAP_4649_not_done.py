import logging

from custom.basic_custom_actions import create_event
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_cases.wrapper import eq_fix_wrappers
from test_cases.wrapper.fix_verifier import FixVerifier
from stubs import Stubs
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4649"
    # region Declarations
    client = "CLIENT_YMOROZ"
    account = "CLIENT4_SA1"
    qty = "900"
    price = "10"
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    no_allocs = {"NoAllocs": [{'AllocAccount': account, 'AllocQty': qty}]}
    ord_book = OMSOrderBook(case_id, session_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion
    ord_book.open_fe(session_id, report_id, work_dir, username, password)
    # region Create order list
    no_order = [eq_fix_wrappers.set_fix_order_detail(3, 1, client, 2, qty, 0, price, ListSeqNo=1),
                eq_fix_wrappers.set_fix_order_detail(3, 2, client, 2, qty, 0, price, ListSeqNo=2)]
    fix_message = eq_fix_wrappers.create_order_list_via_fix(case_id, no_order)
    response = fix_message.pop('response')
    #time.sleep(5)
    cl_inbox = OMSClientInbox(case_id, session_id)
    cl_inbox.accept_order("VETO", qty, price)
    cl_inbox.accept_order("VETO", qty, price)
    # endregion
    # region Verify
    params = {
        'ClOrdID': response.response_messages_list[0].fields['ListID'].simple_value,
    }

    fix_verifier_ss = FixVerifier(eq_fix_wrappers.get_buy_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params', key_parameters=['ListID'],
                                          )
    fix_verifier_ss.CheckListStatusRequest(params, response, message_name='Check params',  key_parameters=['ListID'])
    fix_verifier_ss = FixVerifier(eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckListStatusRequest(params, response, message_name='Check params',  key_parameters=['ListID'],
                                           direction="SECOND")
    fix_verifier_ss.CheckListStatusRequest(params, response, message_name='Check params',  key_parameters=['ListID'])
    # endregion
    # region Cancel order


    # endregion
    # region Check values after Cancel
    params = {
        'OrderQty': qty,
        'ExecType': '4',
        'OrdStatus': '4',
        'Side': '2',
        'Price': price,
        'TimeInForce': '6',
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'SettlDate': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SettlDate': '*',
        # 'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*',
        'ExpireDate': '*',
    }
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ExecType'])
    # endregion
    # region Cancel order list
    eq_fix_wrappers.cancel_order_list_via_fix(case_id,
                                              response.response_messages_list[0].fields['ClOrdID'].simple_value)
    # endregion
    # region Verify list status
    params = {
        'ListID': qty,
        'ListStatusType': '*',
        'NoRpts': '*',
        'ListOrderStatus': '*',
        'RptSeq': price,
        'ListStatusText': '*',
        'TransactTime': '*',
        'TotNoOrders': '*',
        'LastFragment': '*',
        'NoOrders': [
            {'ClOrdID': '*',
             'SecondaryClOrdID': '*',
             'CumQty': '*',
             'OrdStatus': '*',
             'WorkingIndicator': '*',
             'LeavesQty': '*',
             'CxlQty': '*',
             'AvgPx': '*',
             'Text': '*'},
            {'ClOrdID': '*',
             'SecondaryClOrdID': '*',
             'CumQty': '*',
             'OrdStatus': '*',
             'WorkingIndicator': '*',
             'LeavesQty': '*',
             'CxlQty': '*',
             'AvgPx': '*',
             'Text': '*'}
        ]
    }
    fix_verifier_ss.CheckListStatusRequest(params, response, message_name='Check params',
                                           key_parameters=['ExecType'])
    # endregion
