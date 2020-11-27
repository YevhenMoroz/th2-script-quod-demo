import logging
import time
from datetime import datetime
import copy
from custom import basic_custom_actions as bca
from grpc_modules import infra_pb2, verifier_pb2
from grpc_modules.act_fix_pb2_grpc import ActFixStub
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.verifier_pb2_grpc import VerifierStub

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = ActFixStub(case_params['act'])
    event_store = EventStoreServiceStub(case_params['event-store'])
    verifier = VerifierStub(case_params['verifier'])

    seconds, nanos = bca.timestamps()  # Store case start time

    # Create sub-report for case
    event_request_1 = bca.create_store_event_request(case_name, case_params['case_id'], report_id)
    event_store.StoreEvent(event_request_1)

    pre_filter = verifier_pb2.PreFilter(
        fields={
            'header': infra_pb2.ValueFilter(
                message_filter=infra_pb2.MessageFilter(
                    fields={
                        'MsgType': infra_pb2.ValueFilter(simple_filter='0',
                                                         operation=infra_pb2.FilterOperation.NOT_EQUAL),
                        'SenderCompID': infra_pb2.ValueFilter(simple_filter=case_params['SenderCompID']),
                        'TargetCompID': infra_pb2.ValueFilter(simple_filter=case_params['TargetCompID'])
                    }
                )
            )
        }
    )
    # Send order to BUY side
    order_1_params = {
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': 1,
        'OrderQty': case_params['OrderQty'],
        'TimeInForce': case_params['TimeInForce'],
        'Price': case_params['Price'],
        'OrdType': case_params['OrdType'],
        'ClOrdID': bca.client_orderid(9),
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': case_params['Instrument'],
        'OrderCapacity': 'A',
        'Currency': 'SEK'
    }
    logger.debug("Send new order with ClOrdID = {}".format(order_1_params['ClOrdID']))
    order_1 = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', order_1_params)
        ))
    checkpoint_1 = order_1.checkpoint_id
    execution_report1_params = {
        'ClOrdID': order_1_params['ClOrdID'],
        'OrderID': order_1.response_message.fields['OrderID'].simple_value,
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': order_1_params['OrderQty'],
        'Instrument': case_params['Instrument']
    }
    logger.debug("Verify received Execution Report (OrderID = {}, ExecType = {}, OrdStatus = {})".format(
        execution_report1_params['OrderID'], "Pending", "Pending")
    )
    er1 = bca.filter_to_grpc("ExecutionReport", execution_report1_params, ['ClOrdID', 'OrdStatus'])
    checkrule_1 = bca.create_check_rule("Receive Execution Report Pending", er1, checkpoint_1,
                                        case_params['TraderConnectivity'], case_params['case_id'])
    verifier.submitCheckRule(checkrule_1)

    execution_report2_params = copy.deepcopy(execution_report1_params)
    execution_report2_params['OrdStatus'] = execution_report2_params['ExecType'] = '0'
    logger.debug("Verify received Execution Report (OrderID = {}, ExecType = {}, OrdStatus = {})".format(
        execution_report1_params['OrderID'], "New", "New")
    )
    er2 = bca.filter_to_grpc("ExecutionReport", execution_report2_params, ['ClOrdID', 'OrdStatus'])
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report New", er2, order_1.checkpoint_id, case_params['TraderConnectivity'],
            case_params['case_id']
        )
    )

    # Send order to SELL side

    order_2_params = {
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': 2,
        'OrderQty': case_params['OrderQty'],
        'TimeInForce': case_params['TimeInForce'],
        'Price': case_params['Price'],
        'OrdType': case_params['OrdType'],
        'ClOrdID': bca.client_orderid(9),
        'TransactTime': (datetime.utcnow().isoformat()),
        'Instrument': case_params['Instrument'],
        'OrderCapacity': 'A',
        'Currency': 'SEK'
    }
    logger.debug("Send new order with ClOrdID = {}".format(order_2_params['ClOrdID']))
    order_2 = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder 2',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', order_2_params)
        ))

    # Prepare system output
    execution_report3_params = copy.deepcopy(execution_report1_params)
    execution_report3_params['ClOrdID'] = order_2_params['ClOrdID']
    execution_report3_params['OrderID'] = order_2.response_message.fields['OrderID'].simple_value
    execution_report3_params['LeavesQty'] = order_2_params['OrderQty']
    logger.debug("Verify received Execution Report (OrderID = {}, ExecType = {}, OrdStatus = {})".format(
        execution_report3_params['OrderID'], "Pending", "Pending")
    )
    er3 = bca.filter_to_grpc("ExecutionReport", execution_report3_params, ['ClOrdID', 'OrdStatus'])
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report", er3, order_2.checkpoint_id, case_params['TraderConnectivity'],
            case_params['case_id']
        )
    )

    execution_report4_params = copy.deepcopy(execution_report2_params)
    execution_report4_params['OrderID'] = '*'
    execution_report4_params['ClOrdID'] = order_2_params['ClOrdID']
    execution_report4_params['LeavesQty'] = order_2_params['OrderQty']
    logger.debug("Verify received Execution Report (OrderID = {}, ExecType = {}, OrdStatus = {})".format(
        execution_report3_params['OrderID'], "New", "New")
    )
    er4 = bca.filter_to_grpc("ExecutionReport", execution_report4_params, ['ClOrdID', 'OrdStatus'])
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report", er4, order_2.checkpoint_id, case_params['TraderConnectivity'],
            case_params['case_id']
        )
    )

    execution_report5_params = copy.deepcopy(execution_report2_params)
    execution_report5_params['CumQty'] = order_1_params['OrderQty']
    execution_report5_params['LastPx'] = order_1_params['Price']
    execution_report5_params['LastQty'] = order_1_params['OrderQty']
    execution_report5_params['AvgPx'] = order_1_params['Price']
    execution_report5_params['OrdStatus'] = 2
    execution_report5_params['ExecType'] = 'F'
    execution_report5_params['LeavesQty'] = 0
    logger.debug("Verify received Execution Report (OrderID = {}, ExecType = {}, OrdStatus = {})".format(
        execution_report5_params['OrderID'], "Trade", "Filled")
    )
    er5 = bca.filter_to_grpc("ExecutionReport", execution_report5_params, ['ClOrdID', 'OrdStatus'])
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report ord1 Filled", er5, order_2.checkpoint_id,
            case_params['TraderConnectivity'], case_params['case_id']
        )
    )

    execution_report6_params = copy.deepcopy(execution_report5_params)
    execution_report6_params['ClOrdID'] = order_2_params['ClOrdID']
    execution_report6_params['OrderID'] = '*'
    logger.debug("Verify received Execution Report (OrderID = {}, ExecType = {}, OrdStatus = {})".format(
        execution_report6_params['OrderID'], "Trade", "Filled")
    )
    er6 = bca.filter_to_grpc("ExecutionReport", execution_report6_params, ['ClOrdID', 'OrdStatus'])
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report Filled", er6, order_2.checkpoint_id, case_params['TraderConnectivity'],
            case_params['case_id']
        )
    )

    message_filters = [er1, er2, er3, er4, er5, er6]
    logger.debug("Verify a sequence of Execution Report messages")
    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            "Receive Execution Reports", pre_filter, message_filters, checkpoint_1,
            case_params['TraderConnectivity'], case_params['case_id']
        )
    )

    if timeouts:
        time.sleep(5)
    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
