import logging

from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_fix_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4649"
    # region Declarations
    client = "CLIENT_YMOROZ"
    account = "CLIENT_YMOROZ_SA1"
    qty = "900"
    price = "10"
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    # endregion
    # region Create order list
    no_allocs =  [{'AllocAccount': account, 'AllocQty': qty}]
    no_order = [eq_fix_wrappers.set_fix_order_detail(3, 1, client, 2, qty, 0, price, ListSeqNo=1,no_allocs=no_allocs),
                eq_fix_wrappers.set_fix_order_detail(3, 2, client, 2, qty, 0, price, ListSeqNo=2,no_allocs=no_allocs)]
    fix_message = eq_fix_wrappers.create_order_list_via_fix(case_id, no_order)
    response = fix_message.pop('response')

    # endregion
    # region Verify
    params = {
        'NoRpts': '*',
        'ListID': response.response_messages_list[0].fields['ListID'].simple_value,
        'RptSeq': '*',
        'ListStatusType': '*',
        'TotNoOrders': '*',
        'ListOrderStatus': '3',
        'OrdListStatGrp': {'NoOrders': [{
            'AvgPx': '0',
            'CumQty': '0',
            'ClOrdID': no_order[0]['ClOrdID'],
            'LeavesQty': '900',
        }, {
            'AvgPx': '0',
            'CumQty': '0',
            'ClOrdID': no_order[1]['ClOrdID'],
            'LeavesQty': '900',
        }
        ]}
    }

    fix_verifier_ss = FixVerifier(eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckListStatus(params, response)
    # endregion
    # region Cancel order
    eq_fix_wrappers.cancel_order_via_fix(case_id, no_order[0]['ClOrdID'], no_order[0]['ClOrdID'], client, 1)
    # endregion
    # region Check values after Cancel
    params = {
        'Account': client,
        'OrderQtyData': {'OrderQty': qty},
        'ExecType': '4',
        'OrdStatus': '4',
        'Side': '1',
        'Price': price,
        'TimeInForce': '0',
        'ClOrdID': no_order[0]['ClOrdID'],
        'OrigClOrdID': no_order[0]['ClOrdID'],
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'Parties': '*',
        'AvgPx': '*',
        'CxlQty': qty,
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SettlDate': '*',
        'SettlType': '*',
        'Instrument': '*',
        'header': '*',
        'ExpireDate': '*',
    }
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ExecType'])
    # endregion
    # region Cancel order list
    eq_fix_wrappers.cancel_order_list_via_fix(case_id,
                                              response.response_messages_list[0].fields['ListID'].simple_value)
    # endregion
    # region Verify list status
    params = {
        'NoRpts': '*',
        'ListID': response.response_messages_list[0].fields['ListID'].simple_value,
        'RptSeq': '*',
        'ListStatusType': '*',
        'TotNoOrders': '*',
        'ListOrderStatus': '4',
        'OrdListStatGrp': {'NoOrders': [{
            'AvgPx': '0',
            'CumQty': '0',
            'ClOrdID': no_order[0]['ClOrdID'],
            'LeavesQty': '900',
        }, {
            'AvgPx': '0',
            'CumQty': '0',
            'ClOrdID': no_order[1]['ClOrdID'],
            'LeavesQty': '900',
        }
        ]}
    }
    fix_verifier_ss.CheckListStatus(params, response)
    # endregion
