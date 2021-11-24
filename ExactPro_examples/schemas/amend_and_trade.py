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

    # Send order to BUY side
    order_1_params = {
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': 1,
        'OrderQty': case_params['OrderQty'],
        'TimeInForce': case_params['TimeInForce'],
        'Price': case_params['Price1'],
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
            case_id,
            bca.message_to_grpc('NewOrderSingle', order_1_params, case_params['TraderConnectivity'])
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
                                        case_params['TraderConnectivity'], case_id)
    verifier.submitCheckRule(checkrule_1)

    execution_report2_params = copy.deepcopy(execution_report1_params)
    execution_report2_params['OrdStatus'] = execution_report2_params['ExecType'] = '0'
    logger.debug("Verify received Execution Report (OrderID = {}, ExecType = {}, OrdStatus = {})".format(
        execution_report1_params['OrderID'], "New", "New")
    )
    er2 = bca.filter_to_grpc("ExecutionReport", execution_report2_params, ['ClOrdID', 'OrdStatus'])
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report New", er2, order_1.checkpoint_id, case_params['TraderConnectivity'], case_id
        )
    )
    # Send order to SELL side

    order_2_params = {
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': 2,
        'OrderQty': case_params['OrderQty'],
        'TimeInForce': case_params['TimeInForce'],
        'Price': case_params['Price2'],
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
            'Send NewSingleOrder 2', case_params['TraderConnectivity'], case_id,
            bca.message_to_grpc('NewOrderSingle', order_2_params, case_params['TraderConnectivity'])
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
            "Receive Execution Report", er3, order_2.checkpoint_id, case_params['TraderConnectivity'], case_id
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
            "Receive Execution Report", er4, order_2.checkpoint_id, case_params['TraderConnectivity'], case_id
        )
    )
    replace_order_params = {
        'OrigClOrdID': order_2_params['ClOrdID'],
        # 'ClOrdID': str(int(specific_order_params['ClOrdID']) + 1),
        'ClOrdID': bca.client_orderid(9),
        'Account': order_2_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Instrument': case_params['Instrument'],
        'Side': order_2_params['Side'],
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrdType': case_params['OrdType'],
        'OrderQty': case_params['OrderQty'],
        'Price': case_params['Price1'],
        'OrderCapacity': 'A',
    }
    logger.debug("Amend order with ClOrdID = {}".format(order_2_params['ClOrdID']))
    replace_order = act.placeOrderReplaceFIX(
        bca.convert_to_request(
            'Send OrderCancelRequest',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('OrderCancelReplaceRequest', replace_order_params, case_params['TraderConnectivity'])
        ))

    execution_report7_params = {
        **order_2_params,
        'ClOrdID': replace_order_params['ClOrdID'],
        'OrderID': execution_report4_params['OrderID'],
        'HandlInst': '1',
        'Side': '2',
        'ExecID': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': '0',
        'ExecType': '5',
        'LeavesQty': case_params['OrderQty'],
        'Instrument': case_params['Instrument'],
        'TransactTime': '*',
        # 'MaxFloor': order_2_params['DisplayInstruction']['DisplayQty'],
        # 'NoStrategyParameters': execution_report4_params['NoStrategyParameters'],
        # 'NoStrategyParameters': [
        #     {'StrategyParameterName': 'LowLiquidity', 'StrategyParameterType': '13', 'StrategyParameterValue': 'Y'}],
        # 'ExecRestatementReason': '4',
        'Price': case_params['Price1'],
        'OrderQty': case_params['OrderQty'],
    }
    er7 = bca.filter_to_grpc("ExecutionReport", execution_report7_params, ['ClOrdID', 'OrdStatus'])

    logger.debug("Verify received Execution Report (OrdStatus = New, ExecType = Replaced)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive Execution Report ord2 Amended',
            bca.filter_to_grpc('ExecutionReport', execution_report7_params, ["ClOrdID", "OrdStatus"]),
            replace_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_id
        )
    )

    execution_report5_params = copy.deepcopy(execution_report2_params)
    execution_report5_params['Account'] = order_1_params['Account']
    execution_report5_params['ExecID'] = '*'
    execution_report5_params['CumQty'] = order_1_params['OrderQty']
    execution_report5_params['OrderQty'] = order_1_params['OrderQty']
    execution_report5_params['Price'] = order_1_params['Price']
    execution_report5_params['Currency'] = order_1_params['Currency']
    execution_report5_params['TimeInForce'] = order_1_params['TimeInForce']
    execution_report5_params['HandlInst'] = '1'
    execution_report5_params['SecondaryOrderID'] = order_1.response_message.fields['SecondaryOrderID'].simple_value
    execution_report5_params['LastMkt'] = order_1.response_message.fields['LastMkt'].simple_value
    execution_report5_params['OrderCapacity'] = order_1.response_message.fields['OrderCapacity'].simple_value
    execution_report5_params['OrdType'] = order_1_params['OrdType']
    execution_report5_params['Side'] = order_1_params['Side']
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
            case_params['TraderConnectivity'], case_id
        )
    )

    execution_report6_params = copy.deepcopy(execution_report5_params)
    execution_report6_params['ClOrdID'] = execution_report7_params['ClOrdID']
    execution_report6_params['OrderID'] = '*'
    execution_report6_params['SecondaryOrderID'] = replace_order.response_message.fields['SecondaryOrderID'].simple_value
    execution_report6_params['Side'] = order_2_params['Side']
    logger.debug("Verify received Execution Report (OrderID = {}, ExecType = {}, OrdStatus = {})".format(
        execution_report6_params['OrderID'], "Trade", "Filled")
    )
    er6 = bca.filter_to_grpc("ExecutionReport", execution_report6_params, ['ClOrdID', 'OrdStatus'])
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report ord2 Filled", er6, order_2.checkpoint_id, case_params['TraderConnectivity'],
            case_id
        )
    )

    pre_filter = PreFilter(
        fields={
            'Instrument': ValueFilter(
                message_filter=MessageFilter(
                    fields={
                        'Symbol': ValueFilter(
                            simple_filter=execution_report1_params['Instrument']['Symbol']),
                        'SecurityID': ValueFilter(
                            simple_filter=execution_report1_params['Instrument']['SecurityID']),
                        'SecurityIDSource': ValueFilter(
                            simple_filter=execution_report1_params['Instrument']['SecurityIDSource']),
                        'SecurityExchange': ValueFilter(
                            simple_filter=execution_report1_params['Instrument']['SecurityExchange']),
                    }
                )
            ),
            'header': ValueFilter(
                message_filter=MessageFilter(
                    fields={
                        'MsgType': ValueFilter(simple_filter='0', operation=FilterOperation.NOT_EQUAL),
                        'SenderCompID': ValueFilter(simple_filter=case_params['SenderCompID']),
                        'TargetCompID': ValueFilter(simple_filter=case_params['TargetCompID'])
                    }
                )
            )
        }
    )

    message_filters = [er1, er2, er3, er4, er7, er5, er6]
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
