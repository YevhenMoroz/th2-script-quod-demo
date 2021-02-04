import logging
import time
from datetime import datetime
import copy
from custom import basic_custom_actions as bca
from th2_grpc_common.common_pb2 import ValueFilter, MessageFilter, FilterOperation
from th2_grpc_check1.check1_pb2 import PreFilter
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = Stubs.fix_act
    verifier = Stubs.verifier

    seconds, nanos = bca.timestamps()  # Store case start time

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    pre_filter = PreFilter(
        fields={
            'header': ValueFilter(
                message_filter=MessageFilter(
                    fields={
                        'MsgType': ValueFilter(simple_filter='8', operation=FilterOperation.EQUAL),
                        'SenderCompID': ValueFilter(simple_filter=case_params['SenderCompID']),
                        'TargetCompID': ValueFilter(simple_filter=case_params['TargetCompID'])
                    }
                )
            )
        }
    )
    # Send order to BUY side
    O1_params = {
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': 1,
        'OrderQty': case_params['OrderQty_ord1'],
        'TimeInForce': case_params['TimeInForce'],
        'Price': case_params['Price'],
        'OrdType': case_params['OrdType'],
        'ClOrdID': bca.client_orderid(9),
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': case_params['Instrument'],
        'OrderCapacity': 'A',
        'Currency': 'SEK'
    }

    logger.debug("Send new order with ClOrdID = {}".format(O1_params['ClOrdID']))

    order_1 = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder ord1',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('NewOrderSingle', O1_params, case_params['TraderConnectivity'])
        ))

    checkpoint_1 = order_1.checkpoint_id

    execution_report_O1_pending_params = {
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': 1,
        'OrderQty': case_params['OrderQty_ord1'],
        'CumQty': '0',
        'LastQty': '0',
        'LeavesQty': O1_params['OrderQty'],
        'QtyType': '0',
        'TimeInForce': case_params['TimeInForce'],
        'Price': case_params['Price'],
        'LastPx': '0',
        'AvgPx': '0',
        'OrdType': case_params['OrdType'],
        'ClOrdID': O1_params['ClOrdID'],
        'OrderID': order_1.response_message.fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Instrument': case_params['Instrument'],
        'OrderCapacity': 'A',
        'Currency': 'SEK',
        'OrdStatus': 'A',
        'ExecType': 'A',
    }

    logger.debug("Verify received Execution Report (OrderID = {}, ExecType = {}, OrdStatus = {})".format(
        execution_report_O1_pending_params['OrderID'], "Pending", "Pending")
    )
    er1 = bca.filter_to_grpc("ExecutionReport", execution_report_O1_pending_params, ['ClOrdID', 'OrdStatus'])
    checkrule_1 = bca.create_check_rule("Receive Execution Report ord1 Pending", er1, checkpoint_1,
                                        case_params['TraderConnectivity'], case_id)
    verifier.submitCheckRule(checkrule_1)

    execution_report_O1_new_params = copy.deepcopy(execution_report_O1_pending_params)
    execution_report_O1_new_params['OrdStatus'] = execution_report_O1_new_params['ExecType'] = '0'
    logger.debug("Verify received Execution Report (OrderID = {}, ExecType = {}, OrdStatus = {})".format(
        execution_report_O1_pending_params['OrderID'], "New", "New")
    )
    er2 = bca.filter_to_grpc("ExecutionReport", execution_report_O1_new_params, ['ClOrdID', 'OrdStatus'])
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report ord1 New", er2, order_1.checkpoint_id, case_params['TraderConnectivity'],
            case_id
        )
    )

    # Send order to SELL side
    O2_params = {
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': 2,
        'OrderQty': case_params['OrderQty_ord2'],
        'TimeInForce': case_params['TimeInForce'],
        'Price': case_params['Price'],
        'OrdType': case_params['OrdType'],
        'ClOrdID': bca.client_orderid(9),
        'TransactTime': (datetime.utcnow().isoformat()),
        'Instrument': case_params['Instrument'],
        'OrderCapacity': 'A',
        'Currency': 'SEK'
    }
    logger.debug("Send new order with ClOrdID = {}".format(O2_params['ClOrdID']))

    order_2 = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder ord2',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('NewOrderSingle', O2_params, case_params['TraderConnectivity'])
        ))

    execution_report_O2_pending_params = copy.deepcopy(execution_report_O1_pending_params)
    execution_report_O2_pending_params['ClOrdID'] = O2_params['ClOrdID']
    execution_report_O2_pending_params['OrderID'] = order_2.response_message.fields['OrderID'].simple_value
    execution_report_O2_pending_params['OrderQty'] = O2_params['OrderQty']
    execution_report_O2_pending_params['LeavesQty'] = O2_params['OrderQty']
    execution_report_O2_pending_params['Side'] = O2_params['Side']

    logger.debug("Verify received Execution Report (OrderID = {}, ExecType = {}, OrdStatus = {})".format(
        execution_report_O2_pending_params['OrderID'], "Pending", "Pending")
    )
    er3 = bca.filter_to_grpc("ExecutionReport", execution_report_O2_pending_params, ['ClOrdID', 'OrdStatus'])
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report ord2 Pending", er3, order_2.checkpoint_id, case_params['TraderConnectivity'],
            case_id
        )
    )

    execution_report_O2_new_params = copy.deepcopy(execution_report_O1_new_params)
    execution_report_O2_new_params['ClOrdID'] = O2_params['ClOrdID']
    execution_report_O2_new_params['OrderID'] = order_2.response_message.fields['OrderID'].simple_value
    execution_report_O2_new_params['OrderQty'] = O2_params['OrderQty']
    execution_report_O2_new_params['LeavesQty'] = O2_params['OrderQty']
    execution_report_O2_new_params['Side'] = O2_params['Side']

    logger.debug("Verify received Execution Report (OrderID = {}, ExecType = {}, OrdStatus = {})".format(
        execution_report_O2_pending_params['OrderID'], "New", "New")
    )
    er4 = bca.filter_to_grpc("ExecutionReport", execution_report_O2_new_params, ['ClOrdID', 'OrdStatus'])
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report ord2 New", er4, order_2.checkpoint_id, case_params['TraderConnectivity'],
            case_id
        )
    )

    execution_report_O1_partfilled_params = copy.deepcopy(execution_report_O1_new_params)
    execution_report_O1_partfilled_params['CumQty'] = O2_params['OrderQty']
    execution_report_O1_partfilled_params['LastQty'] = O2_params['OrderQty']
    execution_report_O1_partfilled_params['LeavesQty'] = O2_params['OrderQty']
    execution_report_O1_partfilled_params['LastPx'] = O1_params['Price']
    execution_report_O1_partfilled_params['AvgPx'] = O1_params['Price']
    execution_report_O1_partfilled_params['OrdStatus'] = 1
    execution_report_O1_partfilled_params['ExecType'] = 'F'
    
    logger.debug("Verify received Execution Report (OrderID = {}, ExecType = {}, OrdStatus = {})".format(
        execution_report_O1_partfilled_params['OrderID'], "Trade", "Filled")
    )
    er5 = bca.filter_to_grpc("ExecutionReport", execution_report_O1_partfilled_params, ['ClOrdID', 'OrdStatus'])
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report ord1 Part Filled", er5, order_2.checkpoint_id,
            case_params['TraderConnectivity'], case_id
        )
    )

    execution_report_O2_fullfilled_params = copy.deepcopy(execution_report_O1_partfilled_params)
    execution_report_O2_fullfilled_params['ClOrdID'] = O2_params['ClOrdID']
    execution_report_O2_fullfilled_params['OrderID'] = order_2.response_message.fields['OrderID'].simple_value
    execution_report_O2_fullfilled_params['OrderQty'] = O2_params['OrderQty']
    execution_report_O2_fullfilled_params['LeavesQty'] = 0
    execution_report_O2_fullfilled_params['OrdStatus'] = 2
    execution_report_O2_fullfilled_params['Side'] = O2_params['Side']

    logger.debug("Verify received Execution Report (OrderID = {}, ExecType = {}, OrdStatus = {})".format(
        execution_report_O2_fullfilled_params['OrderID'], "Trade", "Filled")
    )
    er6 = bca.filter_to_grpc("ExecutionReport", execution_report_O2_fullfilled_params, ['ClOrdID', 'OrdStatus'])
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report ord2 Filled", er6, order_2.checkpoint_id, case_params['TraderConnectivity'],
            case_id
        )
    )

    O1_cancel_params = {
        'OrigClOrdID': O1_params['ClOrdID'],
        'ClOrdID': str(int(O1_params['ClOrdID']) + 1),
        'Instrument': case_params['Instrument'],
        'ExDestination': 'QDL1',
        'Side': O1_params['Side'],
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrderQty': case_params['OrderQty_ord1'],
    }
    logger.debug("Cancel order with ClOrdID = {}".format(O1_params['ClOrdID']))
    cancel_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send CancelOrderRequest 1',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('OrderCancelRequest', O1_cancel_params, case_params['TraderConnectivity']),
        ))

    execution_report_O1_cancel_params = {
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': '1',
        'OrderQty': case_params['OrderQty_ord1'],
        'TimeInForce': case_params['TimeInForce'],
        'Price': case_params['Price'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': O1_params['Currency'],
        'ClOrdID': O1_cancel_params['ClOrdID'],
        'OrigClOrdID': O1_params['ClOrdID'],
        'OrderID': execution_report_O1_pending_params['OrderID'],
        'CumQty': O2_params['OrderQty'],
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': case_params['Price'],
        'OrdStatus': '4',
        'ExecType': '4',
        'LeavesQty': '0',
        'Instrument': case_params['Instrument'],
    }
    logger.debug("Verify received Execution Report (OrdStatus = Cancelled)")

    er7 = bca.filter_to_grpc("ExecutionReport", execution_report_O1_cancel_params, ['ClOrdID', 'OrdStatus'])
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive Execution Report ord1 Cancelled',
            er7,
            cancel_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_id
        )
    )

    message_filters = [er1, er2, er3, er4, er5, er6, er7]
    logger.debug("Verify a sequence of Execution Report messages")
    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            "Receive Execution Reports", pre_filter, message_filters, checkpoint_1,
            case_params['TraderConnectivity'], case_id
        )
    )
    
    if timeouts:
        time.sleep(5)
    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
